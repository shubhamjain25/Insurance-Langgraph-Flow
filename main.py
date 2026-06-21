from agent.graph_main import get_graph

compiled_graph = get_graph()

if __name__ == '__main__':

    test_state = {
        "user_information": {
            "patient_name": "Hardcoded John Doe",
            "claim_category": "MEDICAL",
            "treatment_date": "2026-06-15",
            "claimed_amt": 5000.00
        },
        "document_name": "apollo_bill.jpg",
        "status": "initiated",
        "count_itr": 0
    }

    print("Starting local LangGraph execution...")

    # 3. Invoke with the test state instead of {}
    final_state = compiled_graph.invoke(test_state)

    print("Final Output:")
    print(final_state)

