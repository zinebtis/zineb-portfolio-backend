from app.rag.rag_agent import ask_agent


def main() -> None:
    question = "What are Zineb's research areas?"
    answer = ask_agent(question)
    print("💡 Question:", question)
    print("💬 Answer:", answer)


if __name__ == "__main__":
    main()
