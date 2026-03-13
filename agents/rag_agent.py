class RAGAgent:

    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm

    def run(self, question):

        context, _ = self.retriever.retrieve_context(question)

        context_text = "\n".join(context)

        answer = self.llm.generate_answer(question)

        return answer, context_text