from typing import List
from dotenv import load_dotenv

load_dotenv(override=True)

from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.schema import AIMessage, HumanMessage
from prompt import RESPONDER_PROMPT
from tools.search_travel_info import search_travel_info
from tools.get_weather import get_weather
from tools.web_search import web_search

import time
import google.api_core.exceptions
import json


class Responder:
    def __init__(
        self,
        model_name: str,
        model_provider: str,
        temperature=0.0,
    ):
        """Create responder agent

        Args:
            model_name (str): name of the model used
            model_provider (str): name of the provider
            temperature (float, optional): adjust the level of creativity. Defaults to 0.
        """
        self.llm_model = init_chat_model(
            model_name, model_provider=model_provider, temperature=temperature
        )

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", RESPONDER_PROMPT),
                MessagesPlaceholder(variable_name="question"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        self.tools = [search_travel_info, get_weather, web_search]

        # Create agent from prompt template
        Agent_calling = create_tool_calling_agent(
            self.llm_model, tools=self.tools, prompt=prompt
        )

        self.TravelExecutor = AgentExecutor(
            agent=Agent_calling,
            tools=self.tools,
            verbose=False,
            handle_parsing_errors=True,
        )

    def safe_invoke(self, inputs, retries=5, delay=2):
        for i in range(retries):
            try:
                return self.TravelExecutor.invoke(inputs)
            except google.api_core.exceptions.ServiceUnavailable as e:
                print(f"[Retry {i+1}] Model overloaded. Waiting {delay}s...")
                time.sleep(delay)
        raise Exception("Model vẫn quá tải sau nhiều lần thử lại.")

    def run(self, query):
        required_keys = {"id", "description", "depends_on"}
        if not isinstance(query, dict):
            raise ValueError("Input 'query' phải là một dictionary.")
        if not required_keys.issubset(query.keys()):
            missing = required_keys - set(query.keys())
            raise ValueError(f"Thiếu trường trong input: {', '.join(missing)}")

        # Trích xuất câu hỏi cốt lõi
        user_request = query["description"]

        response = self.safe_invoke({"question": [HumanMessage(content=user_request)]})

        agent_text_response = response.get(
            "output", "Xin lỗi, đã có lỗi xảy ra và tôi không thể tạo phản hồi."
        )

        final_output = {
            "id": query["id"],
            "description": query["description"],
            "depends_on": query["depends_on"],
            "response": agent_text_response.strip(),
        }

        return final_output


def main():
    responder = Responder("gemini-2.0-flash", "google-genai")
    query = {
        "id": "task_1",
        "description": "Các di tích lịch sử ở Hà Nội",
        "depends_on": [],
    }

    rsp = responder.run(query=query)
    print(rsp)


if __name__ == "__main__":
    main()
