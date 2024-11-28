import os

# Suppress warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Retrieve hugging face token from environment variable
HF_TOKEN =os.getenv("HF_TOKEN")
MODEL_NAME = "gpt2"

# Forbidden prompts (copied text)
FORBIDDEN_PROMPTS = [
    "create five personas that represent distinct user groups",
    "create five personas and ensure that the set of personas aligns with your understanding of diversity"
]
