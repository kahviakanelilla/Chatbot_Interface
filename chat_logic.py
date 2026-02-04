import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from config import MODEL_NAME, FORBIDDEN_PROMPTS

print(f"Loading model {MODEL_NAME} locally...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# device_map="cpu" is safer for free tiers to avoid CUDA errors
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, 
    device_map="cpu", 
    torch_dtype="auto"
)

def chatbot_response(user_input, chat_history):
    """
    Local inference logic similar to your old code.
    No API calls, everything happens inside the Space.
    """
    if not user_input.strip():
        return chat_history, "", ""
    
    if user_input in FORBIDDEN_PROMPTS:
        return chat_history, "Unauthorized prompt.", ""

    try:
        # Reconstruct chat history into a single string
        prompt = ""
        for turn in chat_history:
            role = "user" if turn["role"] == "user" else "assistant"
            prompt += f"<|{role}|>\n{turn['content']}<|end|>\n"
        prompt += f"<|user|>\n{user_input}<|end|>\n<|assistant|>\n"

        # Tokenize and Generate
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=256)
        
        # Decode the response
        full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract only the last assistant part
        answer = full_text.split("<|assistant|>")[-1].strip()

        # Update History
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": answer})
        
        return chat_history, "", ""

    except Exception as e:
        print(f"Local Error: {str(e)}")
        return chat_history, f"Local Error: {str(e)}", ""
