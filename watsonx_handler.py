
# # watsonx_handler.py
# import os
# import logging
# from ibm_watsonx_ai.foundation_models import ModelInference
# from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
# from ibm_watsonx_ai.credentials import Credentials
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# # Set up credentials
# credentials = Credentials(
#     url=os.getenv("WATSONX_URL"),
#     api_key=os.getenv("WATSONX_APIKEY")
# )

# # Watsonx model configuration
# parameters = {
#     "decoding_method": "greedy",
#     "max_new_tokens": 1500,
#     "min_new_tokens": 5,
#     "temperature": 0
# }

# project_id = os.getenv("PROJECT_ID")
# model_id = "meta-llama/llama-3-3-70b-instruct"

# # Instantiate the Watsonx model
# model = ModelInference(
#     model_id=model_id,
#     credentials=credentials,
#     project_id=project_id,
#     params=parameters
# )


# import logging

# def generate_query_plan(question: str) -> str:
#     prompt = f"""
# You are a financial analyst.

# Given the question: "{question}"

# Generate a concise plan (exactly 14 to 15 bullet points) to analyze this question using enterprise financial data.

# Each bullet point should describe a meaningful and logical action such as comparing metrics, analyzing trends, or calculating ratios.

# Do NOT include more than 20 points.
# Do NOT return explanations or headers — only the bullet points.

# Plan:
# """

#     logging.info("[Watsonx] Generating plan for question: %s", question)
#     logging.debug("[Watsonx] Full prompt:\n%s", prompt)

#     try:
#         result = model.generate_text(prompt)

#         # Handle both string and dict result formats
#         if isinstance(result, dict) and "results" in result and result["results"]:
#             plan = result["results"][0]["generated_text"]
#         elif isinstance(result, str):
#             plan = result
#         else:
#             raise ValueError(f"Unexpected model response format: {result}")

#         # Post-processing to ensure clean 5-point format
#         lines = [line.strip() for line in plan.strip().split("\n") if line.strip().startswith("*")]
#         short_plan = "\n".join(lines[:5])  # Keep only first 5 bullet points

#         logging.info("[Watsonx] Shortened plan:\n%s", short_plan)
#         return short_plan

#     except Exception as e:
#         logging.error("[Watsonx] Error generating plan: %s", str(e))
#         return "Error generating plan from Watsonx."


import os
import logging
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.credentials import Credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set up credentials
credentials = Credentials(
    url=os.getenv("WATSONX_URL"),
    api_key=os.getenv("WATSONX_APIKEY")
)

# Watsonx model configuration
parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 1500,
    "min_new_tokens": 5,
    "temperature": 0
}

project_id = os.getenv("PROJECT_ID")
model_id = "meta-llama/llama-3-3-70b-instruct"

# Instantiate the Watsonx model
model = ModelInference(
    model_id=model_id,
    credentials=credentials,
    project_id=project_id,
    params=parameters
)

def load_metadata(file_path="/Users/sakshimaurya/Desktop/Query_planner/csv_metadata_summary.txt") -> str:
    """Reads and extracts key financial terms from metadata.txt."""
    if not os.path.exists(file_path):
        logging.warning("[Metadata] File not found: %s", file_path)
        return "No additional metadata available."

    with open(file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
        metadata_content = "\n".join(lines[:20])  # Limit metadata for brevity

    logging.info("[Metadata] Loaded financial metadata.")
    return metadata_content

def generate_query_plan(question: str) -> str:
    """Generates a structured financial query plan using metadata context."""
    metadata_info = load_metadata()

    prompt = f"""
You are a financial analyst with access to enterprise financial data. 
Below is metadata about the available data structure:

{metadata_info}

Given the question: "{question}"

Generate a concise plan (exactly 14 to 15 bullet points) to analyze this question using the available financial data.

Each bullet point should describe a meaningful and logical action such as comparing metrics, analyzing trends, or calculating ratios.

Do NOT include more than 20 points.
Do NOT return explanations or headers — only the bullet points.

Plan:
"""

    logging.info("[Watsonx] Generating plan for question: %s", question)
    logging.debug("[Watsonx] Full prompt:\n%s", prompt)

    try:
        result = model.generate_text(prompt)

        if isinstance(result, dict) and "results" in result and result["results"]:
            plan = result["results"][0]["generated_text"]
        elif isinstance(result, str):
            plan = result
        else:
            raise ValueError(f"Unexpected model response format: {result}")

        # Extract first 5 bullet points for a concise output
        lines = [line.strip() for line in plan.strip().split("\n") if line.strip().startswith("*")]
        short_plan = "\n".join(lines[:5])

        logging.info("[Watsonx] Shortened plan:\n%s", short_plan)
        return short_plan

    except Exception as e:
        logging.error("[Watsonx] Error generating plan: %s", str(e))
        return "Error generating plan from Watsonx."




