from app.rag.chain import answer_question


def main():

    query = "What was EBITDA growth?"

    result = answer_question(query)

    print("\nQUESTION\n")
    print(query)

    print("\nANSWER\n")
    print(result["answer"])


if __name__ == "__main__":
    main()