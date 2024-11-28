from chat_logic import chatbot_response
from html_file import generate_chat_file
from ui_elements import create_ui


def handle_generate(prolific_id, task_type, chat_history):
    return generate_chat_file(prolific_id, task_type, chat_history)

if __name__ == "__main__":
    demo = create_ui(
        chat_response_fn=lambda user_input: chatbot_response(user_input, chat_history),
        generate_file_fn=handle_generate
    )
    demo.launch()