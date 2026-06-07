from app.rag.chain import answer_question


def main():

    result = answer_question(
        query="What was revenue growth?",
        ticker="TCS"
    )

    print("\nQUESTION\n")
    print("What was revenue growth?")

    print("\nCOMPANY\n")
    print("TCS")

    print("\nANSWER\n")
    print(result["answer"])


if __name__ == "__main__":
    main()