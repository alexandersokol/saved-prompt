from typing import Optional

import gradio as gr
import modules.scripts as scripts
from fastapi import FastAPI
from gradio import Blocks
from modules import script_callbacks
from modules import shared, sd_models, sd_vae, paths, ui_extra_networks
from modules.shared import OptionInfo

from scripts import env
from scripts.api_samplet import init_extension_api
from scripts.storage import DatabaseManager
from scripts.ui_main import main_ui_block

env.script_dir = scripts.basedir()


def on_ui_tabs():
    return ((main_ui_block(), "Prompts", "cucurumba"),)


def on_app_started(demo: Optional[Blocks], app: FastAPI):
    DatabaseManager()
    init_extension_api(app)

script_callbacks.on_ui_tabs(on_ui_tabs)
script_callbacks.on_app_started(on_app_started)


def _do_the_input(input_text):
    print(input_text)
    try:
        if not hasattr(shared.opts, "original_pattern"):
            shared.opts.original_pattern = shared.opts.directories_filename_pattern

        if input_text:
            new_pattern = (
                f"{shared.opts.original_pattern}/{input_text}"
                if shared.opts.original_pattern
                else input_text
            )
        else:
            new_pattern = shared.opts.original_pattern

        shared.opts.directories_filename_pattern = new_pattern
        print(shared.opts.directories_filename_pattern)

    except Exception as e:
        print(f"An error occurred while accessing directories_filename_pattern: {e}")
    return input_text


class CucurumbaScript(scripts.Script):
    def __init__(self) -> None:
        super().__init__()

    def title(self):
        return "History"

    def show(self, is_img2img):
        return scripts.AlwaysVisible


    def ui(self, is_img2img):
        editable_save_dir = gr.Textbox(
            label='Save extra dir:',
            value='',
            max_lines=1,
            elem_id='cucurumba_extra_save_dir_edit',
            elem_classes=['cucurumba_tiny_edit_box'],
            scale=1,
            inputs=None,
            outputs=None,
            style={"width": "100px"}
        )

        editable_save_dir.change(_do_the_input, inputs=[editable_save_dir], outputs=None)

        return [editable_save_dir]
