import json
import time

from retriever import Retriever
from llm_generator import LLMGenerator
from evals_engine import EvalsEngine


def run_evaluation(dataset_path):

    with open(dataset_path, "r") as f:
        dataset = json.load(f)

    retriever = Retriever()
    llm = LLMGenerator()
    evaluator = EvalsEngine()

    results = []
    hallucinations = 0

    for item in dataset:

        question = item["question"]

        answer = llm.generate_answer(question)

        context, _ = retriever.retrieve_context(question)

        context_text = "\n".join(context)

        eval_result = evaluator.evaluate(question, answer, context_text)

        is_hallucinated = "true" in eval_result.lower()

        if is_hallucinated:
            hallucinations += 1

        record = {
            "question": question,
            "answer": answer,
            "context": context,
            "evaluation": eval_result
        }

        results.append(record)

        print("\nQUESTION:", question)
        print("ANSWER:", answer)
        print("EVAL:", eval_result)

    total = len(dataset)

    summary = {
        "total_questions": total,
        "hallucinations": hallucinations,
        "hallucination_rate": hallucinations / total
    }

    output = {
        "summary": summary,
        "results": results
    }

    timestamp = int(time.time())

    output_file = f"results/eval_results_{timestamp}.json"

    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    print("\nSaved results to:", output_file)


if __name__ == "__main__":

    run_evaluation("data/eval_dataset.json")