import openai
from config import MODEL_NAME, FORBIDDEN_PROMPTS, OPENAI_API_KEY

# Set key
openai.api_key = OPENAI_API_KEY

def chatbot_response(user_input, chat_history):
    # Function for processing user input
    if user_input in FORBIDDEN_PROMPTS:
        return chat_history, "<div style='color:red;'>Nice try, you shouldn't copy and paste the task.</div>", ""

    if not user_input.strip():  # empty prompt
        return chat_history, "<div style='color:red;'>Error: Prompt cannot be empty.</div>", ""

    # OpenAI API call
    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=chat_history + [{"role": "user", "content": user_input}]
        )

        # Extract the assistant's reply
        assistant_response = response['choices'][0]['message']['content']

        # Update chat history
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": assistant_response})

        return chat_history, None, ""  # Return updated history, no error, and empty user input
    except openai.error.OpenAIError as e:
        return (
            chat_history,
            f"<div style='color:red;'>Error: {str(e)}</div>",
            ""
        )