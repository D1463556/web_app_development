from flask import Blueprint, render_template, request, redirect, url_for, flash
# from app.models.recipe import RecipeModel, IngredientModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    顯示所有食譜列表（支援依標籤或關鍵字篩選）。
    """
    pass

@main_bp.route('/recipes/new')
def new_recipe():
    """
    顯示新增食譜表單頁面。
    """
    pass

@main_bp.route('/recipes/create', methods=['POST'])
def create_recipe():
    """
    處理新增食譜表單送出的資料，並儲存至資料庫。
    """
    pass

@main_bp.route('/recipes/<int:recipe_id>')
def recipe_detail(recipe_id):
    """
    顯示單一食譜的詳細內容與食材清單。
    """
    pass

@main_bp.route('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    """
    顯示編輯食譜表單頁面，並載入現有資料供修改。
    """
    pass

@main_bp.route('/recipes/<int:recipe_id>/update', methods=['POST'])
def update_recipe(recipe_id):
    """
    處理編輯食譜表單送出的修改資料，更新至資料庫。
    """
    pass

@main_bp.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    處理刪除特定食譜的請求，從資料庫移除後返回首頁。
    """
    pass
