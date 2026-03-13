from router.router import Router
from agents.rag_agent import RAGAgent
from agents.sql_agent import SQLAgent

from core.retriever import Retriever
from core.llm_generator import LLMGenerator
from evals.evals_engine import EvalsEngine


def run(question):

    router = Router()
    decision = router.route(question)

    print("\nRouter decision:", decision)

    evaluator = EvalsEngine()

    if decision == "sql_agent":

        sql_agent = SQLAgent("data/sample_db.sqlite")
        sql, result = sql_agent.run(question)

        print("\nGenerated SQL:", sql)
        print("Result:", result)

        return

    else:

        retriever = Retriever()
        llm = LLMGenerator()

        rag_agent = RAGAgent(retriever, llm)

        answer, context = rag_agent.run(question)

        print("\nAnswer:", answer)
        print("\nContext:", context)

        # Run evaluation
        eval_result = evaluator.evaluate(
            question,
            answer,
            context
        )

        print("\nEvaluation:", eval_result)


if __name__ == "__main__":

    question = input("\nAsk a question: ")

    run(question)