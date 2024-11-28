import gradio as gr
import gradio.themes
from config import MODEL_NAME
from html_file import generate_chat_file
from chat_logic import chatbot_response

def create_ui(chat_response_fn, generate_file_fn):
    # Gradio-UI
    with gr.Blocks(theme=gradio.themes.Citrus()) as demo:
        gr.Markdown("<h1 style='text-align: center; color: #5b89b0;'>ChatGPT Interface</h1>")

        with gr.Row():
            with gr.Column(scale=3):
                gr.Markdown("<h2>ChatGPT</h2>")
                chat_box = gr.Chatbot(label=MODEL_NAME, type="messages")
                user_input = gr.Textbox(label="Input", placeholder="Your prompt here...", lines=4, interactive=True)
                alert_box = gr.HTML("", visible=False)
                submit_btn = gr.Button("Submit",interactive=False)
            with gr.Column(scale=1):
                gr.Markdown("<h2>Save Chat</h2>")
                gr.Markdown(
                """
                1. **Enter your Prolific ID** in the input field
                2. **Select the Task** you worked on
                3. **Generate** the Chat History File
                4. **Click on Download** to save the file
                4. **Upload the downloaded file** to the survey platform for the corresponding task
                """
                )
                # Inputs
                prolific_id = gr.Textbox(label="Prolific ID", placeholder="Please enter your Prolific ID")
                task_type = gr.Radio(label="Select the task you are working on", choices=["1", "2"], type="value", value=None)
                # Errors
                error_box = gr.HTML("", visible=False)
                # Buttons
                generate_btn = gr.Button("Generate File")
                download_btn = gr.DownloadButton("Download File", visible=False)

    # State for each user (per session)
        state = gr.State([])

        def handle_generate(prolific_id, task_type, state):
            file_path, error, download_update = generate_chat_file(prolific_id, task_type, state)
            return error, download_update  # Return the error box and download button

        # Activation of the button on entry
        def activate_submit_button(text):
            return gr.update(interactive=bool(text.strip()))  # Aktivieren, wenn Text vorhanden

        user_input.change(activate_submit_button, inputs=user_input, outputs=submit_btn)

        # events
        user_input.submit(
            fn=chatbot_response,
            inputs=[user_input, state],
            outputs=[chat_box,alert_box, user_input],
        )
        submit_btn.click(
            fn=chatbot_response,
            inputs=[user_input, state],
            outputs=[chat_box, alert_box, user_input],
            concurrency_limit=None
        )

        #submit_btn.click(chatbot_response, inputs=[user_input, state], outputs=[chat_box, alert_box, user_input])

        # Combine generate and download
        generate_btn.click(
            fn=handle_generate,
            inputs=[prolific_id, task_type,state],
            outputs=[error_box, download_btn],
            concurrency_limit=None
        )
    return demo
