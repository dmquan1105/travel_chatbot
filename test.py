from travel_bot import Travel
from langchain.schema import HumanMessage, AIMessage


def main():
    travel_agent = Travel("gemini-2.0-flash", "google-genai", temperature=0)

    print("Chatbot du lịch khởi động! Gõ 'exit' để thoát.\n")

    while True:
        user_input = input("Bạn: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Tạm biệt! Hẹn gặp lại chuyến sau.")
            break

        response = travel_agent.run(question=user_input)
        print(f"Bot: {response['output']}\n")

        print(
            f"Lịch sử: {len(travel_agent.chat_history)} lượt | Tokens: {travel_agent.total_tokens}"
        )
        print("-" * 50)


if __name__ == "__main__":
    main()
