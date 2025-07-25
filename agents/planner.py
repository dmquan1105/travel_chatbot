from dotenv import load_dotenv

load_dotenv(override=True)
import time
import google.api_core.exceptions
from agents.base_agent import BaseAgent
from prompt import PLANNER_PROMPT
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.schema import AIMessage, HumanMessage
import json
from langchain.schema import BaseMessage
from typing import List


# KHÔNG DÙNG TRONG PIPELINE


class Planner(BaseAgent):
    def __init__(self, model_name: str, model_provider: str, temperature=0.0):
        super().__init__(model_name=model_name, model_provider=model_provider)
        self.tools = []

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", PLANNER_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                MessagesPlaceholder(variable_name="question"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # Create agent from prompt template
        Agent_calling = create_tool_calling_agent(
            self.llm, tools=self.tools, prompt=prompt
        )

        self.PlanExecutor = AgentExecutor(
            agent=Agent_calling,
            tools=self.tools,
            verbose=False,
            handle_parsing_errors=True,
        )

    def safe_invoke(self, input, retries=5, delay=2):
        for i in range(retries):
            try:
                return self.PlanExecutor.invoke(input)
            except google.api_core.exceptions.ServiceUnavailable as e:
                print(f"[Retry {i+1}] Model overloaded. Waiting {delay}s...")
                time.sleep(delay)
        raise Exception("Model vẫn quá tải sau nhiều lần thử lại.")

    def run(self, query: str, chat_history: List[BaseMessage]):
        response = self.safe_invoke(
            {"question": [HumanMessage(content=query)], "chat_history": chat_history}
        )
        try:
            result = response["output"].strip()

            # Bỏ ```json và ``` nếu có
            if result.startswith("```json"):
                result = result[len("```json") :].strip()
            if result.endswith("```"):
                result = result[:-3].strip()
            return json.loads(result)
        except Exception as e:
            print("Lỗi parse JSON:", e)
            return [
                {"id": "task_1", "description": response["output"], "depends_on": []}
            ]


def main():
    planner = Planner("gemini-2.0-flash", "google-genai")
    chat_history = [
        HumanMessage(content="Xin chào"),
        AIMessage(content="Xin chào, bạn muốn làm gì hôm nay?"),
    ]
    query = "Các địa điểm đi du lịch hay ho ở miền Bắc?"
    response = planner.run(query=query, chat_history=chat_history)
    print(response)


if __name__ == "__main__":
    main()
