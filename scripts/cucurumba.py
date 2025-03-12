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
