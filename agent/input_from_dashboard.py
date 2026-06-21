import json
from agent.schema_structures.Schema import *
import os

def get_patient_information_hardcoded() -> UserInputInformation:

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "assets", "hardcoded_input.json")

    with open(file_path, "r") as f:
        user_input_data = json.load(f)

    return user_input_data