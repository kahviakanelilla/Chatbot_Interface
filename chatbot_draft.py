import gradio as gr
import gradio.themes
import os
from transformers import AutoModelForCausalLM, AutoTokenizer

# Hugging Face Token aus Umgebungsvariable abrufen
token = os.getenv("HF_TOKEN")

# Tokenizer und Modell laden
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)

# Verbotene Prompts (kopierter Text)
forbidden_prompts = [
    "create five personas that represent distinct user groups",
    "create five personas and ensure that the set of personas aligns with your understanding of diversity"
]

# Funktion zum Verarbeiten der User-Eingaben
def chatbot_response(user_input, chat_history):
    # Exception bei kopierten Texten
    if user_input in forbidden_prompts:
        return chat_history, gr.update(
            value="<div style='background-color: #fdecea; color: #d93025; border: 1px solid #f5c2c7; border-radius: 8px; padding: 10px;'>Nice try, you shouldn't copy and paste the task. Please try using your own words.</div>",
            visible=True
        ), ""

    # Tokenisierung und Modell-Ausgabe
    inputs = tokenizer(user_input, return_tensors="pt")
    outputs = model.generate(inputs["input_ids"], max_length=50, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Chat-Verlauf aktualisieren
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": response})
    return chat_history, gr.update(visible=False), ""  # Fehlermeldung ausblenden, Eingabefeld leeren

# Funktion zum Generieren der HTML-Datei
def generate_chat_file(prolific_id, task_type, chat_history):
    if not prolific_id or not task_type:
        return "Error: Please provide a valid Prolific ID and select a task type."

    # Dateiname basierend auf den Eingaben erstellen
    filename = f"{prolific_id}_task{task_type.replace(' ', '').lower()}.html"

    html_content = "<html><body><h1>Chat History</h1><ul style='list-style-type: none;'>"
    for message in chat_history:
        if message["role"] == "user":
            html_content += f"<li style='text-align: right;'><b>{message['content']}</b></li>"
        elif message["role"] == "assistant":
            html_content += f"<li style='text-align: left; color: gray;'>{message['content']}</li>"
    html_content += "</ul></body></html>"

    # HTML-Inhalt zurückgeben
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)
    return f"File saved as {filename}"

# Gradio UI
with gr.Blocks(theme=gradio.themes.Citrus()) as demo:
    # Hauptüberschrift für die gesamte Seite
    gr.Markdown("<h1 style='text-align: center; color: #5b89b0;'>ChatGPT Interface</h1>")

    # Hauptbereich mit Chatbot
    with gr.Row():
        with gr.Column(scale=3):
            gr.Markdown("<h2>ChatGPT</h2>")
            chat_box = gr.Chatbot(label="GPT-4o", type="messages")  # Verwende type="messages"
            user_input = gr.Textbox(label="Input", placeholder="Your prompt here...")
            submit_btn = gr.Button("Submit")
            alert_box = gr.HTML("", visible=False)  # Fehlerfeld als HTML
        # Sidebar rechts
        with gr.Column(scale=1):
            gr.Markdown("<h2>Save Chat</h2>")
            prolific_id = gr.Textbox(label="Prolific ID", placeholder="Please enter your Prolific ID")
            task_type = gr.Radio(label="Select the task you are working on", choices=["Task 1", "Task 2"], type="value", value=None)
            download_btn = gr.Button("Download Chat History")
            result_output = gr.Textbox(label="Saving status", interactive=False)

    # Zustand für jeden Nutzer (pro Sitzung)
    state = gr.State([])  # Initial leerer Chatverlauf

    # Events
    submit_btn.click(chatbot_response, inputs=[user_input, state], outputs=[chat_box, alert_box, user_input])
    download_btn.click(generate_chat_file, inputs=[prolific_id, task_type, state], outputs=result_output)

# Starte die App
if __name__ == "__main__":
    demo.launch()
