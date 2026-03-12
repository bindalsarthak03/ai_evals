from retreiver import Retriever
from llm_generator import LLMGenerator
from evals_engine import EvalsEngine

def run_pipeline(question):
    retriever = Retriever()
    llm = LLMGenerator()
    evaluator = EvalsEngine()
    
    answer = llm.generate_answer(question)
    context,metadata = retriever.retreive_context(answer)
    context_text = "\n".join(context)
    result = evaluator.evaluate(question,answer,context_text)
    
    print("\nQuestion:", question)
    print("\nAnswer:", answer)
    print("\nContext:", context)
    print("\nEvaluation:", result)


if __name__ == "__main__":
    print("Running evals program...")
    question = input("Ask a question: ")
    run_pipeline(question)