import json
import os
import time

from router.router import Router
from agents.rag_agent import RAGAgent
from agents.sql_agent import SQLAgent
from core.retriever import Retriever
from core.llm_generator import LLMGenerator
from evals.evals_engine import EvalsEngine


def save_result(record):

    os.makedirs("results", exist_ok=True)

    file_path = "results/results.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(record)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def run(question):

    router = Router()
    evaluator = EvalsEngine()

    decision = router.route(question)

    if decision == "sql_agent":

        sql_agent = SQLAgent("data/sample_db.sqlite")

        sql, result = sql_agent.run(question)

        print("\nAgent:", decision)
        print("Query:", sql)
        print("Answer:", result)

        record = {
            "timestamp": time.time(),
            "question": question,
            "agent": decision,
            "query": sql,
            "answer": result,
            "hallucinated": None
        }

        save_result(record)

    else:

        retriever = Retriever()
        llm = LLMGenerator()

        rag_agent = RAGAgent(retriever, llm)

        answer, context = rag_agent.run(question)

        eval_result = evaluator.evaluate(
            question,
            answer,
            context
        )

        hallucinated = eval_result.get("is_hallucinated", None)

        print("\nAgent:", decision)
        print("Query: N/A")
        print("Answer:", answer)

        record = {
            "timestamp": time.time(),
            "question": question,
            "agent": decision,
            "query": None,
            "answer": answer,
            "context": context,
            "hallucinated": hallucinated
        }

        save_result(record)


if __name__ == "__main__":

    question = input("\nAsk a question: ")

    run(question)