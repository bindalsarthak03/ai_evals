from agents.sql_agent import SQLAgent


class SQLPipeline:

    def __init__(self, sql_agent):
        self.sql_agent = sql_agent

    def run(self, question):

        sql_query, result = self.sql_agent.run(question)

        return {
            "agent": "sql",
            "sql_query": sql_query,
            "result": result
        }