from dotenv import load_dotenv

load_dotenv(override=True)

from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.schema import AIMessage, HumanMessage

PROMPT = """
Bạn là một chuyên gia tư vấn du lịch AI chuyên nghiệp, thân thiện và nhiệt tình.

Nhiệm vụ của bạn là:
- Giúp người dùng lập kế hoạch du lịch phù hợp với ngân sách, thời gian, sở thích (biển, núi, nghỉ dưỡng, khám phá, ẩm thực...).
- Gợi ý lịch trình chi tiết theo từng ngày nếu được yêu cầu.
- Cung cấp thông tin điểm đến (thời tiết, thời điểm đẹp nhất, món ăn đặc sản, phương tiện đi lại, giá vé...).
- Tư vấn các mẹo khi đi du lịch (chuẩn bị hành lý, văn hóa địa phương, lưu ý an toàn...).
- Trả lời ngắn gọn, súc tích nếu người dùng cần nhanh.
- Luôn hỏi lại để làm rõ nhu cầu nếu chưa đủ thông tin.
- Ưu tiên các địa điểm và dữ liệu cập nhật (nếu RAG được bật).
- Ngôn ngữ trả lời là tiếng Việt (có thể gợi ý bằng tiếng Anh nếu đi nước ngoài).

Giữ giọng điệu thân thiện, chuyên nghiệp như một hướng dẫn viên bản địa giàu kinh nghiệm.

** Quan trọng **:
- Nếu có bất kỳ câu hỏi nào không liên quan đến du lịch, hãy LỊCH SỰ từ chối trả lời!
"""


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
                ("system", PROMPT),
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


def main():
    travel_agent = Travel("gemini-2.0-flash", "google-genai", temperature=0)
    # question = "Tôi yêu ẩm thực. Tôi nên đi đâu ở Thái Bình?"
    question = "Tôi có thể học toán ở đâu?"
    response = travel_agent.run(question=question)
    print(response["output"])


if __name__ == "__main__":
    main()
