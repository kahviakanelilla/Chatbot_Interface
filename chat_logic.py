from transformers import AutoModelForCausalLM, AutoTokenizer
from config import HF_TOKEN, MODEL_NAME, FORBIDDEN_PROMPTS

# Modell und Tokenizer laden
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, token=HF_TOKEN)

def chatbot_response(user_input, chat_history):
    # Function for processing user input
    if user_input in FORBIDDEN_PROMPTS:
        return chat_history, "<div style='color:red;'>Nice try, you shouldn't copy and paste the task.</div>", ""

    if not user_input.strip():  # empty prompt
        return chat_history, "<div style='color:red;'>Error: Prompt cannot be empty.</div>", ""

    # Tokenization and model output
    inputs = tokenizer(user_input, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=50, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Update chat history
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": response})
    return chat_history, None, ""