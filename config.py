import os

# Suppress warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

#Get OpenAI Key
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# API Key Hugging Face (Settings -> Access Tokens)
HF_TOKEN = os.getenv("HF_TOKEN") 

#MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"
#MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
#MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"

# Forbidden prompts (copied text)
FORBIDDEN_PROMPTS = [
    "create five personas that represent distinct user groups",
    "create five personas and ensure that the set of personas aligns with your understanding of diversity",
    "Hi!"
]
# Define password
PASSWORD = os.getenv("PASSWORD")
