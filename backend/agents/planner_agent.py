import os
import sys
import logging

# Ensure backend directory is in python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from src.gemini_llm import client, generate_content_with_retry

logger = logging.getLogger("PlannerAgent")

def run_planner_agent(query: str) -> dict:
    """
    Planner Agent: Creates a custom GATE CSE study plan.
    Does not require FAISS context as schedules are built based on user constraints
    and general GATE prep best practices.
    
    Returns:
    {
        "agent_used": "Planner Agent",
        "response": "...",
        "answer": "...",
        "sources": []
    }
    """
    logger.info(f"Running Planner Agent for query: {query}")
    
    prompt = f"""
You are the Planner Agent, an experienced personal preparation mentor for GATE CSE candidates.
Your goal is to design a realistic, high-quality, and highly structured study roadmap based on the student's constraints (e.g. total days/months, daily study hours).

Instructions:
1. Provide a comprehensive, encouraging, and highly structured schedule.
2. Break it down into clear stages or weeks/days:
   - Subjects Coverage Plan (Core GATE subjects like DS & Algo, OS, DBMS, CN, TOC, Compiler, COA, Digital Logic, Discrete Math, Engg Math, Aptitude)
   - Revision Cycles (Spaced repetition, mock tests)
   - Practice Questions strategy
   - Previous Year Question (PYQ) solving goals
3. Make sure the plan corresponds logically to the student's constraints in their query (e.g. if they say 90 days, provide a 90-day breakdown).

Student Query:
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
            "agent_used": "Planner Agent",
            "response": answer_text,
            "answer": answer_text,
            "sources": []
        }
    except Exception as e:
        logger.error(f"Error in Planner Agent execution: {str(e)}", exc_info=True)
        error_msg = f"An error occurred in Planner Agent: {str(e)}"
        return {
            "agent_used": "Planner Agent",
            "response": error_msg,
            "answer": error_msg,
            "sources": []
        }
