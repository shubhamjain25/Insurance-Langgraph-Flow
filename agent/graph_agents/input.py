from agent.schema_structures.Schema import *


def input_agent(p_state: DocumentValidator):
    print("+ Entered Input Agent")

    print("="*20)
    print(p_state)

    print("+ Passed Input Agent")
    return {
        # 'user_information': user_input_data,
        'count_itr':1
    }