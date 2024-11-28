import os

# Suppress warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

#Get OpenAI Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI-Model
MODEL_NAME = "gpt-4o-2024-11-20"

# Forbidden prompts (copied text)
FORBIDDEN_PROMPTS = [
    "create five personas that represent distinct user groups",
    "create five personas and ensure that the set of personas aligns with your understanding of diversity"
]
# Define password
PASSWORD = os.getenv("PASSWORD")