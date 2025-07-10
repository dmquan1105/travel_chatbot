from travel_bot import Travel


def main():
    travel_agent = Travel("gemini-2.0-flash", "google-genai", temperature=0)
    question = "Tôi yêu ẩm thực. Tôi nên đi đâu ở Thái Bình?"
    # question = "Tôi có thể học toán ở đâu?"
    response = travel_agent.run(question=question)
    print(response["output"])


if __name__ == "__main__":
    main()
