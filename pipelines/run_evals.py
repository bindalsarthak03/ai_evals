import json
import os
import time

from router.router import Router
from agents.rag_agent import RAGAgent
from agents.sql_agent import SQLAgent
from evals.evals_engine import EvalsEngine
from core.retriever import Retriever
from core.llm_generator import LLMGenerator


def run_evaluation(dataset_path):

    with open(dataset_path, "r") as f:
        dataset = json.load(f)

    router = Router()
    retriever = Retriever()
    llm = LLMGenerator()
    rag_agent = RAGAgent(retriever, llm)
    sql_agent = SQLAgent("data/sample_db.sqlite")

    evaluator = EvalsEngine()

    results = []

    for item in dataset:

        question = item["question"]

        decision = router.route(question)

        if decision == "sql_agent":

            sql, result = sql_agent.run(question)

            record = {
                "question": question,
                "agent": "sql_agent",
                "sql": sql,
                "result": result
            }

        else:

            answer, context = rag_agent.run(question)

            eval_result = evaluator.evaluate(
                question,
                answer,
                context
            )

            record = {
                "question": question,
                "agent": "rag_agent",
                "answer": answer,
                "context": context,
                "evaluation": eval_result
            }

        results.append(record)

        print("\nProcessed:", question)

        time.sleep(2)  # avoid Gemini rate limit

    output = {
        "timestamp": time.time(),
        "results": results
    }

    os.makedirs("results", exist_ok=True)

    file_path = f"results/eval_results_{int(time.time())}.json"

    with open(file_path, "w") as f:
        json.dump(output, f, indent=2)

    print("\nSaved results to:", file_path)


if __name__ == "__main__":
    run_evaluation("data/eval_dataset.json")