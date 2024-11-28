import os
import gradio as gr
from config import MODEL_NAME

def generate_chat_file(prolific_id, task_type, chat_history):
     # Display error if entries are missing
    if not prolific_id and not task_type:
        return None, gr.update(
        value="<div style='background-color: #fdecea; color: #d93025; border: 1px solid #f5c2c7; border-radius: 8px; padding: 10px;'>Error: Please provide both Prolific ID and Task Type before downloading the chat history</div>",
        visible=True
    ), gr.update(visible=False)
    elif not prolific_id:
        return None, gr.update(
            value="<div style='background-color: #fdecea; color: #d93025; border: 1px solid #f5c2c7; border-radius: 8px; padding: 10px;'>Error: Please provide Prolific ID before downloading the chat history</div>",
            visible=True
        ), gr.update(visible=False)
    elif not task_type:
        return None, gr.update(
            value="<div style='background-color: #fdecea; color: #d93025; border: 1px solid #f5c2c7; border-radius: 8px; padding: 10px;'>Error: Please provide Task Type before downloading the chat history</div>",
            visible=True
        ), gr.update(visible=False)

    filename = f"{prolific_id}_task{task_type.replace(' ', '').lower()}.html"

   # Generate HTML content including layout
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background-color: #1e1e1e;
                color: #ffffff;
            }}
            .container {{
                width: 90%;
                margin: 20px auto;
                background-color: #2e2e2e;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
            }}
            .header {{
                text-align: center;
                background-color: #3c3c3c;
                color: #5b89b0;
                padding: 15px 0;
                border-radius: 12px 12px 0 0;
                font-size: 20px;
                font-weight: bold;
    #temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8")
    #temp_file.write(html_content)
    #temp_file.close()
            }}
            .info {{
                text-align: center;
                margin-top: 10px;
                font-size: 14px;
                color: #bdbdbd;
            }}
            .chat {{
                display: flex;
                flex-direction: column;
                gap: 10px;
                padding: 10px 0;
            }}
            .message {{
                padding: 15px;
                border-radius: 8px;
                max-width: 80%;
                font-size: 16px;
                line-height: 1.5;
                white-space: pre-wrap;
                display: flex;
                flex-direction: column;
            }}
            .user {{
                align-self: flex-end;
                background-color: #ff9800;
                color: black;
                text-align: right;
            }}
            .assistant {{
                align-self: flex-start;
                background-color: #d6d6d6;
                color: black;
                text-align: left;
            }}
            .role {{
                font-weight: bold;
                margin-bottom: 5px;
            }}
            @media (max-width: 768px) {{
                .message {{
                    max-width: 100%;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                Chat History
            </div>
            <div class="info">
                <p>Prolific ID: {prolific_id} | Task: {task_type} | Model: {MODEL_NAME}</p>
            </div>
            <div class="chat">
    """

    # Add messages
    for message in chat_history:
        if message["role"] == "user":
            html_content += f"""
            <div class="message user">
                <div class="role">User:</div>
                <div>{message['content']}</div>
            </div>
            """
        elif message["role"] == "assistant":
            html_content += f"""
            <div class="message assistant">
                <div class="role">{MODEL_NAME}:</div>
                <div>{message['content']}</div>
            </div>
            """

    html_content += """
            </div>
        </div>
    </body>
    </html>
    """

    # Create temp file
    temp_dir = os.path.join(os.getcwd(), "downloads")  # Local dir for downloads
    os.makedirs(temp_dir, exist_ok=True)  # create dir if not existing
    file_path = os.path.join(temp_dir, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    return file_path, gr.update(visible=False), gr.update(visible=True, value=file_path)