import os
import sqlite3
from threading import Lock

from scripts import env
from scripts.models import SavedPrompt

_DB_FILE = 'database.sqlite'
_DB_VERSION = 1


class DatabaseManager:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            db_file_path = os.path.join(env.script_dir, _DB_FILE)
            self.connection = sqlite3.connect(db_file_path, check_same_thread=False)
            self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()

        # Create SavedPrompt table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS SavedPrompt (
            id INTEGER PRIMARY KEY,
            name TEXT,
            positive_prompt TEXT,
            negative_prompt TEXT,
            image_path TEXT,
            usage_count INTEGER,
            is_favourite BOOLEAN,
            created_at INTEGER,
            is_removed BOOLEAN,
            sampling_method TEXT,
            sampling_steps INTEGER,
            width INTEGER,
            height INTEGER,
            cfg_steps INTEGER,
            clip_skip INTEGER
        )
        """)

        cursor.execute(f'''CREATE TABLE IF NOT EXISTS Version
                                        (version INTEGER DEFAULT {_DB_VERSION})''')

        self.connection.commit()

    def insert(self, saved_prompt):
        cursor = self.connection.cursor()
        cursor.execute("""
                INSERT INTO SavedPrompt (
                    name, positive_prompt, negative_prompt, image_path, usage_count, 
                    is_favourite, created_at, is_removed, sampling_method, sampling_steps, 
                    width, height, cfg_steps, clip_skip
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
            saved_prompt.name, saved_prompt.positive_prompt, saved_prompt.negative_prompt,
            saved_prompt.image_path, saved_prompt.usage_count, saved_prompt.is_favourite,
            saved_prompt.created_at, saved_prompt.is_removed, saved_prompt.sampler,
            saved_prompt.sampling_steps, saved_prompt.width, saved_prompt.height,
            saved_prompt.cfg_scale, saved_prompt.clip_skip
                ))
        self.connection.commit()

    def update(self, saved_prompt):
        cursor = self.connection.cursor()
        cursor.execute("""
        UPDATE SavedPrompt
        SET name = ?, positive_prompt = ?, negative_prompt = ?, image_path = ?, 
            usage_count = ?, is_favourite = ?, created_at = ?, is_removed = ?, 
            sampling_method = ?, sampling_steps = ?, width = ?, height = ?, 
            cfg_steps = ?, clip_skip = ?
        WHERE id = ?
        """, (
            saved_prompt.name, saved_prompt.positive_prompt, saved_prompt.negative_prompt,
            saved_prompt.image_path, saved_prompt.usage_count, saved_prompt.is_favourite,
            saved_prompt.created_at, saved_prompt.is_removed, saved_prompt.sampler,
            saved_prompt.sampling_steps, saved_prompt.width, saved_prompt.height,
            saved_prompt.cfg_scale, saved_prompt.clip_skip, saved_prompt.id_
        ))
        self.connection.commit()
    
    def get_by_id(self, prompt_id):
        cursor = self.connection.cursor()
        cursor.execute("""
        SELECT id, name, positive_prompt, negative_prompt, image_path, usage_count,
               is_favourite, created_at, is_removed, sampling_method, sampling_steps,
               width, height, cfg_steps, clip_skip
        FROM SavedPrompt
        WHERE id = ?
        """, (prompt_id,))
        row = cursor.fetchone()
        if row:
            return SavedPrompt(*row)
        return None

    def get_by_name(self, name):
        cursor = self.connection.cursor()
        cursor.execute("""
        SELECT id, name, positive_prompt, negative_prompt, image_path, usage_count,
               is_favourite, created_at, is_removed, sampling_method, sampling_steps,
               width, height, cfg_steps, clip_skip
        FROM SavedPrompt
        WHERE name = ?
        """, (name,))

    def get_by_positive_prompt(self, positive_prompt):
        cursor = self.connection.cursor()
        cursor.execute("""
        SELECT id, name, positive_prompt, negative_prompt, image_path, usage_count,
               is_favourite, created_at, is_removed, sampling_method, sampling_steps,
               width, height, cfg_steps, clip_skip
        FROM SavedPrompt
        WHERE positive_prompt = ?
        """, (positive_prompt,))
        row = cursor.fetchone()
        if row:
            return SavedPrompt(*row)
        return None

    def get_all(self):
        query = """
        SELECT id, name, positive_prompt, negative_prompt, image_path, usage_count, 
               is_favourite, created_at, is_removed, sampling_method, sampling_steps, 
               width, height, cfg_steps, clip_skip
        FROM SavedPrompt
        WHERE is_removed = 0
        ORDER BY is_favourite DESC, created_at DESC
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        saved_prompts = [SavedPrompt(*row) for row in rows]
        return saved_prompts
    
    

    def delete(self, prompt_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM SavedPrompt WHERE id = ?", (prompt_id,))
        self.connection.commit()

