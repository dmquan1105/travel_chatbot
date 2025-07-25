from typing import List
from dotenv import load_dotenv

load_dotenv(override=True)

from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.schema import AIMessage, HumanMessage
from prompt import ORCHESTRATOR_PROMPT

from langchain.schema import BaseMessage
from langchain.schema.messages import get_buffer_string
import time
import google.api_core.exceptions


class Orchestrator:
    def __init__(
        self,
        model_name: str,
        model_provider: str,
        temperature=0.0,
        max_tokens: int = 4000,
    ):
        """Create orchestrator agent

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
                ("system", ORCHESTRATOR_PROMPT),
                MessagesPlaceholder(variable_name="question"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        self.max_tokens = max_tokens
        self.total_tokens = 0
        self.chat_history: List[BaseMessage] = []
        self.tools = []

        # Create agent from prompt template
        Agent_calling = create_tool_calling_agent(
            self.llm_model, tools=self.tools, prompt=prompt
        )

        self.MasterExecutor = AgentExecutor(
            agent=Agent_calling,
            tools=self.tools,
            verbose=False,
            handle_parsing_errors=True,
        )

    def update_total_tokens(self):
        self.total_tokens = self.llm_model.get_num_tokens(
            get_buffer_string(self.chat_history)
        )

    def trim_history_to_fit(self):
        while self.total_tokens > self.max_tokens:
            if len(self.chat_history) > 2:
                removed_msg = self.chat_history.pop(0)
                self.total_tokens -= self.llm_model.get_num_tokens(
                    get_buffer_string([removed_msg])
                )
            else:
                break

    def safe_invoke(self, inputs, retries=5, delay=2):
        for i in range(retries):
            try:
                return self.MasterExecutor.invoke(inputs)
            except google.api_core.exceptions.ServiceUnavailable as e:
                print(f"[Retry {i+1}] Model overloaded. Waiting {delay}s...")
                time.sleep(delay)
        raise Exception("Model vẫn quá tải sau nhiều lần thử lại.")

    def run(self, question: str):
        """Execute the agent

        Args:
            question (str): the question of the customer
        """
        pass
