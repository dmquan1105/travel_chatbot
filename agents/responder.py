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

from langchain.schema import BaseMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.schema.messages import get_buffer_string
import time
import google.api_core.exceptions


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
            max_tokens (int, optional): maximum token of the context window. Defaults to 4000.
        """
        self.llm_model = init_chat_model(
            model_name, model_provider=model_provider, temperature=temperature
        )

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", RESPONDER_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
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

    def run(self, question: str, chat_history: List[BaseMessage]):
        """Execute the agent

        Args:
            question (str): the question of the customer
            chat_history (List[BaseMessage]):the chat context
        """
        response = self.safe_invoke(
            {"question": [HumanMessage(content=question)], "chat_history": chat_history}
        )

        return response["output"]


def main():
    responder = Responder("gemini-2.0-flash", "google-genai")
    chat_history = [
        HumanMessage(content="Tớ định đi Đà Lạt hoặc Sapa dịp Tết."),
        AIMessage(content="Cả hai nơi đều đẹp, nhưng Sapa có thể lạnh hơn."),
    ]
    # query = "Xây dựng kế hoạch đi du lịch biển Đà Nẵng 2 ngày 1 đêm với ngân sách 5 triệu đồng, muốn thưởng thức hải sản"
    query = "Giá vé máy bay đi Đà Nẵng hiện là bao nhiêu?"
    rsp = responder.run(question=query, chat_history=chat_history)
    print(rsp)


if __name__ == "__main__":
    main()
