import os
import sys
import json
import logging

# Ensure backend directory is in python path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from src.gemini_llm import client, generate_content_with_retry

logger = logging.getLogger("SupervisorAgent")

def route_query(query: str) -> dict:
    """
    Analyzes the user's query and routes it to one of:
    - Concept Agent
    - PYQ Agent
    - Planner Agent
    
    Returns a dict with:
    {
        "selected_agent": "Concept Agent" | "PYQ Agent" | "Planner Agent",
        "reason": "..."
    }
    """
    prompt = f"""
You are the Supervisor Agent for GateGPT, an autonomous AI-powered GATE Computer Science preparation mentor.
Your job is to understand the user's intent and choose the specialized agent to handle the query.

Available Agents:
1. Concept Agent: Used for explaining Computer Science academic concepts, terms, definitions, algorithms, TCP/IP layers, formulas, database normalization, deadlock, process scheduling, page tables, etc.
   Examples: "Explain deadlock", "What is TCP congestion control?", "Explain normalization", "What is Big O notation?"
2. PYQ Agent: Handles all Previous Year Question (PYQ) related queries.

If the user asks to show, provide, retrieve, or list previous year questions, route to the PYQ Agent to return the original PYQs exactly as stored in the knowledge base.
If the user asks for analysis, trends, weightage, important topics, exam patterns, or preparation strategy based on PYQs, route to the PYQ Agent for analytical insights.
If the user requests both retrieval and analysis, the PYQ Agent should first display the original PYQs, followed by the analysis.

Examples (Retrieval):

"Give DBMS PYQs"
"Show Operating System previous year questions"
"Provide GATE 2021 CN questions"
"List TOC PYQs"

Examples (Analysis):

"Analyze DBMS PYQs"
"Important DBMS topics"
"OS weightage in GATE"
"Exam pattern of Compiler Design"
"What should I focus on for DBMS?"
3. Planner Agent: Used for making study schedules, roadmaps, planning preparation time, daily/weekly goals.
   Examples: "Make 90 day GATE plan", "I have 5 hours daily", "100 day study schedule"

You must respond with a JSON object containing exactly these two keys:
- "selected_agent": Must be exactly one of: "Concept Agent", "PYQ Agent", or "Planner Agent"
- "reason": A brief, professional explanation for selecting this agent.

User Query: "{query}"

JSON Response:
"""
    try:
        logger.info(f"Routing query: {query}")
        response = generate_content_with_retry(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        
        result = json.loads(response.text.strip())
        selected = result.get("selected_agent")
        
        valid_agents = ["Concept Agent", "PYQ Agent", "Planner Agent"]
        if selected not in valid_agents:
            logger.warning(f"Invalid agent '{selected}' returned. Falling back.")
            # Simple keyword matching fallback
            query_lower = query.lower()
            if any(w in query_lower for w in ["plan", "schedule", "routine", "day", "month", "hour"]):
                result["selected_agent"] = "Planner Agent"
            elif any(w in query_lower for w in ["pyq", "previous year", "important topic", "weightage", "trend"]):
                result["selected_agent"] = "PYQ Agent"
            else:
                result["selected_agent"] = "Concept Agent"
                
        logger.info(f"Routed to: {result['selected_agent']} because: {result.get('reason')}")
        return result
        
    except Exception as e:
        logger.error(f"Error in Supervisor Agent routing: {str(e)}", exc_info=True)
        # Fallback routing
        query_lower = query.lower()
        if any(w in query_lower for w in ["plan", "schedule", "routine", "day", "month", "hour"]):
            agent = "Planner Agent"
        elif any(w in query_lower for w in ["pyq", "previous year", "important topic", "weightage", "trend"]):
            agent = "PYQ Agent"
        else:
            agent = "Concept Agent"
        return {
            "selected_agent": agent,
            "reason": f"Fallback routing used due to error: {str(e)}"
        }
