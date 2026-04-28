import sqlite3
from datetime import datetime
import os

# 預設資料庫路徑，指向 instance/database.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DB_PATH = os.environ.get('DB_PATH', os.path.join(INSTANCE_DIR, 'database.db'))

def get_db_connection():
    # 若 instance 目錄不存在則建立
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)
        
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # 啟用 Foreign Key 支援以支援 CASCADE 刪除
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

class RecipeModel:
    @staticmethod
    def create(title, instructions, description=None, category=None, tags=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO recipes (title, description, instructions, category, tags)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, description, instructions, category, tags))
        recipe_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return recipe_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        recipes = conn.execute('SELECT * FROM recipes ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(r) for r in recipes]

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db_connection()
        recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
        conn.close()
        return dict(recipe) if recipe else None

    @staticmethod
    def update(recipe_id, title, instructions, description=None, category=None, tags=None):
        conn = get_db_connection()
        updated_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute('''
            UPDATE recipes 
            SET title = ?, description = ?, instructions = ?, category = ?, tags = ?, updated_at = ?
            WHERE id = ?
        ''', (title, description, instructions, category, tags, updated_at, recipe_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(recipe_id):
        conn = get_db_connection()
        # 因為啟用了 PRAGMA foreign_keys = ON，相關連的 ingredients 會被 CASCADE 刪除
        conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        conn.close()


class IngredientModel:
    @staticmethod
    def create(recipe_id, name, quantity=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ingredients (recipe_id, name, quantity)
            VALUES (?, ?, ?)
        ''', (recipe_id, name, quantity))
        conn.commit()
        conn.close()
        return cursor.lastrowid

    @staticmethod
    def get_by_recipe_id(recipe_id):
        conn = get_db_connection()
        ingredients = conn.execute('SELECT * FROM ingredients WHERE recipe_id = ?', (recipe_id,)).fetchall()
        conn.close()
        return [dict(i) for i in ingredients]

    @staticmethod
    def delete_by_recipe_id(recipe_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM ingredients WHERE recipe_id = ?', (recipe_id,))
        conn.commit()
        conn.close()
