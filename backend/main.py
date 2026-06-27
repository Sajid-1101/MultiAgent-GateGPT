from src.rag_pipeline import get_rag_response



while True:


    question = input(
        "\nAsk Question: "
    )


    if question.lower()=="exit":

        break



    answer = get_rag_response(
        question
    )


    print(
        "\nAI Answer:\n"
    )

    print(answer)