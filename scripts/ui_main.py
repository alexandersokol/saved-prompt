import gradio as gr

from scripts.storage import DatabaseManager


# Function to fetch all SavedPrompt objects and render as HTML
def fetch_prompts():
    # Get all SavedPrompt objects from the database
    prompts = DatabaseManager().get_all()
    if not prompts:
        return "<p>No saved prompts found.</p>"

    # Render each SavedPrompt object as an HTML block
    html_blocks = ""
    for prompt in prompts:
        fields = vars(prompt)  # Get all fields from the SavedPrompt object as a dictionary
        html_block = "<div style='border: 1px solid #ccc; padding: 10px; margin: 10px;'>"
        for field_name, field_value in fields.items():
            html_block += f"<strong>{field_name.capitalize()}:</strong> {field_value} <br>"
        html_block += "</div>"
        html_blocks += html_block

    return html_blocks

# Function to handle refresh (also used for initial load)
def refresh_content():
    return fetch_prompts()


def main_ui_block():
    with gr.Blocks(elem_id='cucurumba_tab') as main_block:
        with gr.Row():
            refresh_button = gr.Button("Refresh")
        html_output = gr.HTML(value=refresh_content())            # Refresh Button at the top

        refresh_button.click(fn=refresh_content, outputs=html_output)

    return main_block
