# 流程圖 (Flowchart) - 食譜收藏夾系統

本文件根據 PRD 與架構設計，描繪使用者的操作路徑以及系統內部的資料流動。

## 1. 使用者流程圖 (User Flow)

此圖展示使用者從進入網站開始，能夠進行的主要操作路徑，包含瀏覽、新增、編輯與刪除食譜。

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 食譜列表]
    
    B --> C{要執行什麼操作？}
    
    C -->|搜尋或篩選標籤| B
    C -->|點擊特定食譜| D[食譜詳細資訊頁]
    C -->|點擊新增食譜| E[新增食譜表單]
    
    D --> F{在詳細頁的操作}
    F -->|檢視食材| D
    F -->|點擊編輯| G[編輯食譜表單]
    F -->|點擊刪除| H{防呆確認視窗}
    F -->|回上一頁| B
    
    E -->|填寫並送出| I[儲存至資料庫]
    I -->|重導向| B
    
    G -->|修改並送出| I
    
    H -->|確認刪除| J[從資料庫移除]
    J -->|重導向| B
    H -->|取消| D
```

## 2. 系統序列圖 (Sequence Diagram)

此圖以「使用者新增食譜」為例，描述從使用者送出表單到資料庫完成儲存，並回傳畫面的完整系統運作流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Route as Flask (Controller)
    participant Model as Recipe Model
    participant DB as SQLite

    User->>Browser: 填寫食譜名稱、食材、步驟並點擊送出
    Browser->>Route: POST /recipes/create (攜帶表單資料)
    Route->>Route: 驗證資料是否完整
    alt 資料不完整
        Route-->>Browser: 重新渲染表單並顯示錯誤訊息
        Browser-->>User: 看到錯誤提示
    else 資料完整
        Route->>Model: 呼叫 create_recipe()
        Model->>DB: 執行 INSERT INTO recipes ...
        DB-->>Model: 回傳成功 (新 ID)
        Model-->>Route: 回傳新食譜物件
        Route-->>Browser: HTTP 302 重導向至首頁 (GET /)
        Browser->>Route: GET / (請求首頁)
        Route->>Model: 呼叫 get_all_recipes()
        Model->>DB: 執行 SELECT * FROM recipes
        DB-->>Model: 回傳食譜列表
        Model-->>Route: 回傳列表資料
        Route-->>Browser: 渲染 index.html 並回傳
        Browser-->>User: 看到新增加的食譜出現在列表
    end
```

## 3. 功能清單與 API 對照表

以下整理了系統主要功能對應的 URL 路徑與 HTTP 方法，為後續的路由設計提供基礎。

| 功能名稱 | HTTP 方法 | URL 路徑 | 說明 |
| --- | --- | --- | --- |
| 檢視食譜列表 | GET | `/` 或 `/recipes` | 首頁，顯示所有食譜，支援關鍵字與標籤篩選。 |
| 新增食譜頁面 | GET | `/recipes/create` | 顯示新增食譜的 HTML 表單。 |
| 處理新增食譜 | POST | `/recipes/create` | 接收表單資料並寫入資料庫。 |
| 檢視單一食譜 | GET | `/recipes/<id>` | 顯示特定食譜的詳細步驟與食材清單。 |
| 編輯食譜頁面 | GET | `/recipes/<id>/edit` | 顯示載入現有資料的編輯表單。 |
| 處理編輯食譜 | POST | `/recipes/<id>/edit` | 接收修改後的資料並更新至資料庫。 |
| 刪除食譜 | POST | `/recipes/<id>/delete`| 接收刪除請求並從資料庫移除（為安全考量，使用 POST 代替 GET）。 |
