# from elasticsearch import Elasticsearch
# import os

# ELASTIC_URL = os.getenv("ELASTIC_URL")
# ELASTIC_USER = os.getenv("ELASTIC_USER")
# ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")



# client = Elasticsearch(
#     ELASTIC_URL,
#     basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
#     verify_certs=False,
#     request_timeout=3600
# )

# def search_vector_db(question):
#     response = client.search(index="query_plans", body={"query": {"match": {"question": question}}})
#     return response["hits"]["hits"][0]["_source"]["plan"] if response["hits"]["hits"] else None

# def save_query_plan(question, plan):
#     client.index(index="query_plans", body={"question": question, "plan": plan})

# from elasticsearch import Elasticsearch
# import os

# # Load Elasticsearch credentials from env
# # ELASTIC_URL = os.getenv("ELASTIC_URL")
# # ELASTIC_USER = os.getenv("ELASTIC_USER")
# # ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")


from elasticsearch import Elasticsearch
import os
import logging
import json
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# Get credentials from environment variables
ELASTIC_URL = os.getenv("ELASTIC_URL")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")

if not ELASTIC_URL or not ELASTIC_USER or not ELASTIC_PASSWORD:
    raise ValueError("Elasticsearch credentials are missing. Check environment variables.")

# Initialize Elasticsearch client
try:
    client = Elasticsearch(
        ELASTIC_URL,
        basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD),
        verify_certs=False,
        request_timeout=3600
    )
except Exception as e:
    raise ConnectionError(f"Failed to connect to Elasticsearch: {e}")

def search_vector_db(question):
    """
    Search for an existing query plan in Elasticsearch.
    """
    query = {
        "query": {
            "match": {
                "question": question
            }
        }
    }

    try:
        response = client.search(index="query_plans", query={"match": {"question": question}})

        hits = response.get("hits", {}).get("hits", [])

        if hits:
            query_plan = hits[0]["_source"].get("query_plan", None)
            if query_plan and isinstance(query_plan, dict):  # Ensure it's a dictionary
                logging.info(f"Found Query Plan in Elasticsearch: {json.dumps(query_plan, indent=2)}")
                return query_plan  
        
        logging.info("No matching query plan found in Elasticsearch.")
        return None
    except Exception as e:
        logging.error(f"Elasticsearch search failed: {e}")
        return None

def save_query_plan(question, query_plan):
    """
    Save a generated query plan in Elasticsearch.
    """
    if not query_plan or not isinstance(query_plan, dict):
        logging.error(f"Invalid query plan format: {query_plan}")
        return None  # Prevents saving an invalid format

    doc = {
        "question": question,
        "query_plan": query_plan
    }

    try:
        response = client.index(index="query_plans", document=doc)

        logging.info(f"Saved Query Plan in Elasticsearch: {json.dumps(doc, indent=2)}")
        return response
    except Exception as e:
        logging.error(f"Failed to save query plan in Elasticsearch: {e}")
        return None




