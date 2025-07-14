from travel_bot import Travel


def main():
    travel_agent = Travel("gemini-2.0-flash", "google-genai", temperature=0)
    question = "Tại sao khi lên máy bay, người béo không mang hành lý lại được chấp nhận còn người gầy mang hành lý nặng lại không được chấp nhận dù tổng cân nặng như nhau?"
    response = travel_agent.run(question=question)
    print("=" * 50)
    print(response["output"])
    print("=" * 50)


if __name__ == "__main__":
    main()
