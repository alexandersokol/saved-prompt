import time

from fastapi import FastAPI

from scripts.models import SavedPrompt
from scripts.storage import DatabaseManager


def init_extension_api(app: FastAPI):
    @app.get('/cucurumba')
    async def get_display_options():
        return {
            'version': 1.0,
            'display': True,
            'time': time.time()
        }

    @app.post('/save-prompt-data')
    async def process_prompt(payload: dict):
        required_fields = [
            "positive_prompt",
            "negative_prompt",
            "sampler",
            "sampling_steps",
            "width",
            "height",
            "cfg_scale"
        ]

        # Validate the JSON body fields
        if not all(field in payload for field in required_fields):
            return {"status": "error", "message": "Invalid request, missing required fields"}

        print("Received JSON body:", payload)

        db_manager = DatabaseManager()
        existing_prompt = db_manager.get_by_positive_prompt(payload.get("positive_prompt"))

        if existing_prompt:
            existing_prompt.usage_count += 1
            db_manager.update(existing_prompt)
            saved_prompt = existing_prompt
        else:
            saved_prompt = SavedPrompt(
                id_=None,
                name='',
                positive_prompt=payload.get("positive_prompt"),
                negative_prompt=payload.get("negative_prompt"),
                image_path=None,
                usage_count=0,
                is_favourite=False,
                created_at=int(time.time()),
                is_removed=False,
                sampling_method=payload.get("sampler"),
                sampling_steps=payload.get("sampling_steps"),
                width=payload.get("width"),
                height=payload.get("height"),
                cfg_steps=payload.get("cfg_scale"),
                clip_skip=''
            )
            db_manager.insert(saved_prompt)

        return {"status": "success", "message": "Prompt processed successfully", "saved_prompt": saved_prompt}

    @app.delete('/delete-saved-prompt')
    async def delete_saved_prompt(id_: int):
        """
        Delete a saved prompt by its ID.

        :param id_: ID of the saved prompt to be deleted
        :return: Status message indicating success or failure
        """
        db_manager = DatabaseManager()
        saved_prompt = db_manager.get_by_id(id_)

        if not saved_prompt:
            return {"status": "error", "message": f"No saved prompt found with ID: {id_}"}

        # Mark the prompt as deleted (soft delete)
        saved_prompt.is_removed = True
        db_manager.update(saved_prompt)

        return {"status": "success", "message": f"Saved prompt with ID: {id_} has been deleted successfully"}


    @app.get('/get-all-saved-prompts')
    async def get_all_saved_prompts():
        """
        Retrieve all saved prompts from the database.

        :return: List of all saved prompts
        """
        db_manager = DatabaseManager()

        # Fetch all saved prompts from the database
        all_prompts = db_manager.get_all()

        # If no prompts are found, return an empty list
        if not all_prompts:
            return {"status": "success", "message": "No saved prompts found", "data": []}

        # Otherwise, return the list of prompts
        return {"status": "success", "message": "Saved prompts retrieved successfully", "data": all_prompts}


