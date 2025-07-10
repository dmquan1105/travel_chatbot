from dotenv import load_dotenv

load_dotenv(override=True)

from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.schema import AIMessage, HumanMessage
from prompt import BOT_PROMPT


class Travel:
    def __init__(self, model_name: str, model_provider: str, temperature=0):
        """Create travel chatbot agent

        Args:
            model_name (str): name of the model used
            model_provider (str): name of the provider
            temperature (int, optional): adjust the level of creativity. Defaults to 0.
        """
        llm_model = init_chat_model(
            model_name, model_provider=model_provider, temperature=temperature
        )

        # Create prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", BOT_PROMPT),
                MessagesPlaceholder(variable_name="question"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # Create agent from prompt template
        Agent_calling = create_tool_calling_agent(llm_model, tools=[], prompt=prompt)

        self.TravelExecutor = AgentExecutor(
            agent=Agent_calling,
            tools=[],
            verbose=False,
            handle_parsing_errors=True,
        )

    def run(self, question: str):
        """Execute the agent

        Args:
            question (str): the question of the customer
        """
        inputs = {
            "question": [HumanMessage(content=question)],
        }

        return self.TravelExecutor.invoke(inputs)
