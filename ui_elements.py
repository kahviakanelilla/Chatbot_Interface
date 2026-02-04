import gradio as gr
import gradio.themes
from config import MODEL_NAME, PASSWORD
from html_file import generate_chat_file
from chat_logic import chatbot_response

def create_ui(chat_response_fn, generate_file_fn):
    # Gradio-UI mit dem Ocean Theme
    with gr.Blocks(theme=gr.themes.Ocean(), fill_width=True) as demo:
        gr.Markdown("<h1 style='text-align: center; color: #5b89b0;'>Chatbot Interface</h1>")

        # 1. CSS Styles für die Boxen (wie im ersten Beispiel)
        gr.HTML(
            """
            <style>
                .infobox {
                    background-color: rgba(249, 166, 3, 0.2); 
                    border-left: 4px solid #f9a603; 
                    padding: 12px;
                    margin: 12px 0;
                    border-radius: 4px;
                    color: #fff;
                }
                .guidelinebox {
                    background-color: rgba(91, 137, 176, 0.1); 
                    border-left: 4px solid #5b89b0; 
                    padding: 16px;
                    margin: 12px 0;
                    border-radius: 4px;
                    color: #fff;
                    line-height: 1.6;
                }
                .guidelinebox ol li strong {
                    color: #f9a603;
                }
            </style>
            """
        )

        # Login Sektion
        with gr.Column(visible=True) as login_section:
            for row_index in range(3):
                with gr.Row():
                    for col_index in range(3):
                        if row_index == 1 and col_index == 1:
                            with gr.Column(scale=1, min_width=320):
                                password_input = gr.Textbox(label="Enter Password", type="password", placeholder="Password...")
                                login_error = gr.HTML("", visible=False)
                                login_button = gr.Button("Login")
                        else:
                            with gr.Column(scale=1):
                                gr.HTML("")

        # Haupt-Interface (App Section)
        with gr.Row(visible=False) as app_section:
            # Linke Spalte: Chat
            with gr.Column(scale=3):
                gr.HTML(
                    f"""
                    <h2>LLM Model ({MODEL_NAME})</h2>
                    <h3>1. Complete Task</h3>
                    <div class="infobox">
                        <strong>Performance Note:</strong><br>
                        This model runs locally on the server's RAM (16GB). Processing might take a moment even for short prompts. Please be patient.
                    </div>
                    <div class="infobox" style="background-color: rgba(91, 137, 176, 0.2); border-left-color: #5b89b0;">
                        <strong>Task Instruction:</strong><br>
                        - <strong>Do not manually</strong> describe personas or provide specific examples<br>
                        - Instead, guide the LLM through the task by asking it to generate them 
                    </div>
                    """
                )
                
                chat_box = gr.Chatbot(label=MODEL_NAME)
                user_input = gr.Textbox(label="Input", placeholder="Your prompt here...", lines=3, interactive=True)
                alert_box = gr.HTML("", visible=False)
                submit_btn = gr.Button("Submit", interactive=False)

            # Rechte Spalte: Saving & Guidelines
            with gr.Column(scale=2, min_width=400):
                gr.HTML(
                    """
                    <h2>Saving</h2>
                    <h3>2. Save Chat</h3>
                    <div style="margin-bottom: 20px;">
                        <ol>
                            <li>Enter your <strong>ID</strong> below</li>
                            <li>Click <strong>Generate File</strong></li>
                            <li><strong>Download</strong> and upload to the survey platform</li>
                        </ol>
                    </div>
                    """
                )
                
                prolific_id = gr.Textbox(label="ID", placeholder="Enter your ID")
                error_box = gr.HTML("", visible=False)
                generate_btn = gr.Button("Generate File")
                download_btn = gr.DownloadButton("Download File", visible=False)
                

        # Logik & Events
        state = gr.State([])

        def handle_generate(p_id, chat_state):
            file_path, error, download_update = generate_chat_file(p_id, "DEMO", chat_state)
            return error, download_update

        def activate_submit_button(text):
            return gr.update(interactive=bool(text.strip()))

        user_input.change(activate_submit_button, inputs=user_input, outputs=submit_btn)

        # Chat Events
        user_input.submit(fn=chatbot_response, inputs=[user_input, state], outputs=[chat_box, alert_box, user_input])
        submit_btn.click(fn=chatbot_response, inputs=[user_input, state], outputs=[chat_box, alert_box, user_input])

        # Generate/Download Event
        generate_btn.click(fn=handle_generate, inputs=[prolific_id, state], outputs=[error_box, download_btn])

        # Login Logik
        def check_password(input_password):
            if input_password == PASSWORD:
                return gr.update(visible=False), gr.update(visible=True), "", ""
            return gr.update(visible=True), gr.update(visible=False), "<div style='color:red;'>Incorrect password.</div>", ""

        login_button.click(fn=check_password, inputs=password_input, outputs=[login_section, app_section, login_error, password_input])
        password_input.submit(fn=check_password, inputs=password_input, outputs=[login_section, app_section, login_error, password_input])

    return demo
