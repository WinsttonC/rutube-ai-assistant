import os

# General configuration
EMBEDDING_MODEL_NAME = os.getenv('EMBEDDING_MODEL_NAME', 'deepvk/USER-bge-m3')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'TEST')
DB_PATH = os.getenv('DB_PATH', './vector_db_TEST')

# OpenAI API configuration
KEY = os.getenv('KEY')
BASE_URL_ENDPOINT = os.getenv('BASE_URL_ENDPOINT', 'http://81.94.150.226:8000/v1/')
MODEL_NAME = os.getenv('MODEL_NAME', 'openchat/openchat-3.6-8b-20240522')

# Data file path
DATA_FILE_PATH = os.getenv('DATA_FILE_PATH', '/Users/kartashoffv/Documents/rutube-ai-assistant/data/concat_data.csv')
