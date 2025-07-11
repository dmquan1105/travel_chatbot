from travel_bot import Travel


def main():
    travel_agent = Travel("gemini-2.0-flash", "google-genai", temperature=0)
    question = "Bà Nà Hill ở đâu?"
    response = travel_agent.run(question=question)
    print("=" * 50)
    print(response["output"])
    print("=" * 50)


if __name__ == "__main__":
    main()
