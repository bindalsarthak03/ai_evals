from agents.rag_agent import RAGAgent
from evals.evals_engine import EvalsEngine


class RAGPipeline:

    def __init__(self, rag_agent):
        self.rag_agent = rag_agent
        self.evaluator = EvalsEngine()

    def run(self, question):

        answer, context = self.rag_agent.run(question)

        eval_result = self.evaluator.evaluate(
            question,
            answer,
            context
        )

        return {
            "agent": "rag",
            "answer": answer,
            "context": context,
            "evaluation": eval_result
        }