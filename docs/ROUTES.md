# 路由與頁面設計 (API Design) - 食譜收藏夾系統

本文件根據功能需求、架構文件與資料庫設計，規劃了 Flask 的路由規則、HTTP 方法與對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 食譜列表 | GET | `/` | `index.html` | 首頁，顯示所有食譜，支援關鍵字查詢 |
| 新增食譜頁面 | GET | `/recipes/new` | `add.html` | 顯示提供使用者填寫的新增食譜表單 |
| 建立食譜 | POST | `/recipes/create` | — | 接收新增表單，存入資料庫，並重導向至首頁 |
| 食譜詳情 | GET | `/recipes/<id>` | `recipe.html` | 顯示單一食譜的詳細步驟與所有食材 |
| 編輯食譜頁面 | GET | `/recipes/<id>/edit` | `edit.html` | 顯示編輯表單，並將現有資料帶入欄位中 |
| 更新食譜 | POST | `/recipes/<id>/update` | — | 接收修改後的資料，更新資料庫，重導向至詳情頁 |
| 刪除食譜 | POST | `/recipes/<id>/delete` | — | 從資料庫刪除該食譜及相關食材，重導向至首頁 |

> 備註：因為傳統 HTML 表單只支援 GET 與 POST，因此「更新」與「刪除」操作皆使用 POST 搭配特定 URL 後綴。

## 2. 每個路由的詳細說明

### 2.1 首頁 - 食譜列表 (`GET /`)
- **輸入**：URL 參數 `?q=keyword` (用於搜尋食譜名稱)。
- **處理邏輯**：
  - 呼叫 `RecipeModel.get_all()` 取得所有食譜。
  - 若有 `q` 參數，則在 Python 中過濾或擴充 Model 方法進行 LIKE 查詢。
- **輸出**：渲染 `index.html`，傳入食譜列表變數。

### 2.2 新增食譜頁面 (`GET /recipes/new`)
- **輸出**：單純渲染 `add.html` 顯示空白表單。

### 2.3 建立食譜 (`POST /recipes/create`)
- **輸入**：表單資料包含 `title`, `description`, `instructions`, `category`, `tags`，以及動態數量的 `ingredients`。
- **處理邏輯**：
  - 驗證必填欄位 (`title`, `instructions`) 是否為空。若驗證失敗，使用 `flash()` 提示並渲染 `add.html`。
  - 呼叫 `RecipeModel.create()` 建立食譜，取得回傳的新 `recipe_id`。
  - 針對表單傳來的每一項食材，呼叫 `IngredientModel.create(recipe_id, ...)`。
- **輸出**：`redirect('/')` 返回首頁。

### 2.4 食譜詳情 (`GET /recipes/<id>`)
- **輸入**：URL 路徑參數 `id`。
- **處理邏輯**：
  - 呼叫 `RecipeModel.get_by_id(id)`，若回傳 None，返回 404 錯誤頁面。
  - 呼叫 `IngredientModel.get_by_recipe_id(id)` 取得食材清單。
- **輸出**：渲染 `recipe.html`，傳入該食譜物件與食材陣列。

### 2.5 編輯食譜頁面 (`GET /recipes/<id>/edit`)
- **輸入**：URL 路徑參數 `id`。
- **處理邏輯**：
  - 透過 ID 取出食譜與對應食材，若無資料則報錯 404。
- **輸出**：渲染 `edit.html`，將取得的資料傳入模板供 `<input value="...">` 預設填入。

### 2.6 更新食譜 (`POST /recipes/<id>/update`)
- **輸入**：URL 路徑參數 `id` 與修改後的表單資料。
- **處理邏輯**：
  - 呼叫 `RecipeModel.update()` 覆寫食譜主檔。
  - 先呼叫 `IngredientModel.delete_by_recipe_id(id)` 清除舊食材，再迴圈呼叫 `IngredientModel.create()` 寫入新傳入的食材清單。
- **輸出**：`redirect('/recipes/<id>')` 返回該食譜詳情頁。

### 2.7 刪除食譜 (`POST /recipes/<id>/delete`)
- **輸入**：URL 路徑參數 `id`。
- **處理邏輯**：呼叫 `RecipeModel.delete(id)` 從資料庫刪除食譜。
- **輸出**：`redirect('/')` 返回首頁。

## 3. Jinja2 模板清單

所有的 HTML 檔案皆存放於 `app/templates/` 目錄中：

1. `base.html`：**基礎模板**。包含 `<html>` 骨架、`<head>` 引用 CSS、共同導覽列 (Navbar) 以及存放快顯訊息 (`flash messages`) 的區域。
2. `index.html`：繼承 `base.html`。首頁食譜列表與搜尋框。
3. `recipe.html`：繼承 `base.html`。食譜詳細內容展示。
4. `add.html`：繼承 `base.html`。新增食譜表單，包含使用 JavaScript 動態增加食材欄位的功能。
5. `edit.html`：繼承 `base.html`。結構與 `add.html` 類似，但會載入既有資料。

## 4. 路由骨架程式碼
對應的 Python Flask 路由骨架已經建立於 `app/routes/main.py`。
