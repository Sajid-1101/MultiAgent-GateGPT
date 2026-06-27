import os
import sys
import logging

# Ensure backend directory is in python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from src.gemini_llm import client, generate_content_with_retry
from tools.retrieval_tool import get_context_and_sources

logger = logging.getLogger("ConceptAgent")

def run_concept_agent(query: str) -> dict:
    """
    Concept Agent: Acts as a GATE CSE tutor.
    Retrieves context using retrieval_tool and generates structured explanations.
    
    Returns:
    {
        "agent_used": "Concept Agent",
        "response": "...",
        "answer": "...",
        "sources": [...]
    }
    """
    logger.info(f"Running Concept Agent for query: {query}")
    context, sources = get_context_and_sources(query)
    
    prompt = f"""
You are the Concept Agent, an expert academic tutor for GATE Computer Science & Engineering (CSE) candidates.
Your role is to explain Computer Science concepts clearly, structured, and in an exam-focused manner using the provided study material.

Instructions:
1. Explain concepts in a beginner-friendly, structured layout.
2. Break down complex topics into:
   - Definition
   - Explanation
   - Important Points (e.g. key attributes, complexity, mechanisms)
   - Examples
   - Formulas (if any)
   - GATE Exam Perspective (relevance, how questions are asked)
3. Rely primarily on the provided context. If the context does not have sufficient information, explain using your general Computer Science knowledge but do NOT make up fake facts or fake previous year questions.

Context:
{context}

Question:
{query}

Response:
"""
    try:
        response = generate_content_with_retry(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer_text = response.text
        return {
            "agent_used": "Concept Agent",
            "response": answer_text,
            "answer": answer_text,
            "sources": sources
        }
    except Exception as e:
        logger.error(f"Error in Concept Agent execution: {str(e)}", exc_info=True)
        error_msg = f"An error occurred in Concept Agent: {str(e)}"
        return {
            "agent_used": "Concept Agent",
            "response": error_msg,
            "answer": error_msg,
            "sources": sources
        }
