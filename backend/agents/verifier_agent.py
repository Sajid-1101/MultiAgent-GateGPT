import os
import sys
import logging

# Ensure backend directory is in python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from src.gemini_llm import client, generate_content_with_retry

logger = logging.getLogger("VerifierAgent")

def run_verifier_agent(query: str, agent_used: str, agent_response: str, context: str) -> str:
    """
    Verification Agent: Reduces hallucination by verifying the response
    against the retrieved context.
    
    If the agent used is "Planner Agent", or the query is a greeting/casual talk,
    it skips context verification and returns the response.
    
    If the response is determined to be unsupported by the context, it returns:
    "The available knowledge base does not contain enough information."
    
    Otherwise, returns the original response.
    """
    logger.info(f"Running Verifier Agent for query: {query}. Agent to verify: {agent_used}")
    
    # 1. Skip verification for Planner Agent as it's a personalized planner
    if agent_used == "Planner Agent":
        logger.info("Planner Agent response. Skipping verification.")
        return agent_response
        
    # 2. Skip verification for simple greetings or casual conversation
    query_lower = query.strip().lower()
    if query_lower in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening", "how are you", "who are you"]:
        logger.info("Greeting/casual query. Skipping verification.")
        return agent_response
        
    # 3. Verify concept or PYQ answers against retrieved context
    prompt = f"""
You are the Verification Agent for GateGPT.

Your task is ONLY to detect obvious hallucinations.

The retrieved context may be incomplete because it is only the top search results from the knowledge base.

Therefore:

- Do NOT reject a response simply because every detail is not present.
- Assume the retrieved context is only a partial view of the knowledge base.
- If the generated response is generally consistent with the retrieved context and does not invent contradictory academic facts, reply:

SUPPORTED

- Reply UNSUPPORTED only if the response clearly fabricates information or directly contradicts the retrieved context.

Return ONLY one word:

SUPPORTED

or

UNSUPPORTED

Retrieved Context:
{context}

Generated Response:
{agent_response}
"""
    try:
        response = generate_content_with_retry(
            model="gemini-2.5-flash",
            contents=prompt
        )
        verified_text = response.text.strip().upper().split()[0]

        if verified_text.startswith("UNSUPPORTED"):
            logger.warning("Verification failed.")
            return "The available knowledge base does not contain enough information."

        logger.info("Verification passed.")
        return agent_response

        # Fallback: if the verifier returns something unexpected,
        # don't block the user.
        logger.warning(
            f"Unexpected verifier output: {verified_text}. Returning original response."
        )
        return agent_response
        
    except Exception as e:
        logger.error(f"Error in Verifier Agent: {str(e)}. Defaulting to original response to prevent breakage.", exc_info=True)
        return agent_response
