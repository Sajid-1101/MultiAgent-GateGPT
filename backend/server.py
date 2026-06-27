import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("GateGPT-API")

# Ensure backend directory is in python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

# Import Agents and Tools
from agents.supervisor_agent import route_query
from agents.concept_agent import run_concept_agent
from agents.pyq_agent import run_pyq_agent
from agents.planner_agent import run_planner_agent
from agents.verifier_agent import run_verifier_agent
from tools.retrieval_tool import get_context_and_sources
from tools.pyq_tool import get_pyq_context_and_sources

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return {
        "message": "GATE CSE Agentic AI Mentor API Running"
    }

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "Question is required"}), 400

    logger.info(f"Received question: {question}")

    try:
        # 1. Routing via Supervisor Agent
        routing_res = route_query(question)
        selected_agent = routing_res.get("selected_agent", "Concept Agent")
        reason = routing_res.get("reason", "")
        logger.info(f"Supervisor routed query to: '{selected_agent}' | Reason: {reason}")

        # 2. Execute target Specialized Agent and retrieve associated context
        agent_res = None
        context = ""
        
        if selected_agent == "Concept Agent":
            # Fetch context to pass to Verification Agent
            context, _ = get_context_and_sources(question)
            agent_res = run_concept_agent(question)
            
        elif selected_agent == "PYQ Agent":
            # Fetch PYQ context to pass to Verification Agent
            context, _ = get_pyq_context_and_sources(question)
            agent_res = run_pyq_agent(question)
            
        elif selected_agent == "Planner Agent":
            # Planner Agent generates study schedules and does not retrieve PDF content
            context = ""
            agent_res = run_planner_agent(question)
            
        else:
            # Fallback
            context, _ = get_context_and_sources(question)
            agent_res = run_concept_agent(question)

        # 3. Fact verification via Verification Agent
        original_response = agent_res.get("response", "")
        verified_response = run_verifier_agent(question, selected_agent, original_response, context)
        
        # If verification indicates insufficient context or out-of-scope, alter response
        if verified_response == "The available knowledge base does not contain enough information.":
            agent_res["response"] = verified_response
            agent_res["answer"] = verified_response
            agent_res["sources"] = []

        # 4. JSON Response (maintain "answer" key for frontend, add "agent_used", "response", "sources" for agent requirement)
        response_data = {
            "answer": agent_res.get("response", ""),
            "agent_used": agent_res.get("agent_used", selected_agent),
            "response": agent_res.get("response", ""),
            "sources": agent_res.get("sources", [])
        }
        
        logger.info(f"Successfully processed query. Agent used: {response_data['agent_used']}")
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error handling chat request: {str(e)}", exc_info=True)
        return jsonify({
            "answer": "An internal error occurred. Please try again.",
            "agent_used": "System",
            "response": "An internal error occurred. Please try again.",
            "sources": []
        }), 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )