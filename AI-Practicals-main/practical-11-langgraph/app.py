from workflow.graph import graph

print("\nLangGraph Conditional Workflow Ready!\n")

while True:

    query = input("Enter your query (or type exit): ")

    if query.lower() == "exit":
        break

    response = graph.invoke({
        "query": query
    })

    print("\nRESULT:")
    print(response["result"])
    print()
