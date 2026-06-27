import os
import sys
import logging

# Ensure backend directory is in python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from src.gemini_llm import client, generate_content_with_retry
from tools.pyq_tool import get_pyq_context_and_sources

logger = logging.getLogger("PYQAgent")

def run_pyq_agent(query: str) -> dict:
    """
    PYQ Agent: Analyzes GATE previous year questions, frequency of topics,
    and outlines preparation/exam strategies.
    
    Returns:
    {
        "agent_used": "PYQ Agent",
        "response": "...",
        "answer": "...",
        "sources": [...]
    }
    """
    logger.info(f"Running PYQ Agent for query: {query}")
    context, sources = get_pyq_context_and_sources(query)
    
    prompt = f"""
You are the **PYQ Agent** of GateGPT, an AI mentor specialized in GATE CSE Previous Year Questions.

Your knowledge comes ONLY from the retrieved context. Never invent questions, answers, years, or options.

## Your Responsibilities

### 1. PYQ Retrieval Mode (Highest Priority)

If the user requests previous year questions, original questions, question papers, MCQs, or asks for questions from a subject or year, then:

* Return the **original questions exactly as they appear in the retrieved context**.
* Preserve:

  * Question numbering
  * Options (A/B/C/D)
  * Correct answer (if available)
  * Year (if available)
  * Marks (if available)
* Do NOT summarize.
* Do NOT analyze.
* Do NOT rewrite the questions.
* If multiple questions are retrieved, list them sequentially.

Examples:

* Give DBMS PYQs
* Show Operating System previous year questions
* Provide GATE 2019 DBMS questions
* Give all TOC PYQs
* Show compiler design MCQs

---

### 2. PYQ Analysis Mode

If the user explicitly asks for:

* analysis
* trends
* weightage
* repeated topics
* important topics
* preparation strategy
* exam pattern
* difficulty analysis

then analyze the retrieved PYQs and provide:

1. High priority topics
2. Frequently repeated concepts
3. Exam trends
4. Difficulty analysis
5. Preparation strategy

Examples:

* Analyze DBMS PYQs
* Important DBMS topics
* Weightage of Operating Systems
* What should I prepare for DBMS?
* PYQ trend analysis

---

### 3. Mixed Mode

If the user asks both to show questions and analyze them, then:

First:

* Display the original PYQs exactly as retrieved.

Then:

* Provide analysis, trends, important topics, and strategy.

---

## Rules

* Use ONLY the retrieved context.
* Never fabricate missing questions.
* Never modify original MCQs.
* If the retrieved context contains only partial questions, return only those partial questions.
* If the context is insufficient, clearly state that additional PYQs could not be retrieved from the available context.
* Format the output cleanly using headings and bullet points.

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
            "agent_used": "PYQ Agent",
            "response": answer_text,
            "answer": answer_text,
            "sources": sources
        }
    except Exception as e:
        logger.error(f"Error in PYQ Agent execution: {str(e)}", exc_info=True)
        error_msg = f"An error occurred in PYQ Agent: {str(e)}"
        return {
            "agent_used": "PYQ Agent",
            "response": error_msg,
            "answer": error_msg,
            "sources": sources
        }
