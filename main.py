import asyncio
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
import uvicorn
import hellobot
import mathbot

app = FastAPI()

# ----- 個人網站登入頁面 -----
@app.get("/", response_class=HTMLResponse)
async def login_page():
    html_content = """
    <html>
        <head>
            <title>個人網站登入</title>
        </head>
        <body>
            <h1>歡迎來到我的個人網站</h1>
            <form action="/login" method="post">
                <label>帳號: <input type="text" name="username"></label><br>
                <label>密碼: <input type="password" name="password"></label><br>
                <button type="submit">登入</button>
            </form>
        </body>
    </html>
    """
    return html_content

@app.post("/login", response_class=HTMLResponse)
async def do_login(username: str = Form(...), password: str = Form(...)):
    # 這裡用簡單範例驗證，實務可接資料庫
    if username == "admin" and password == "1234":
        return f"<h2>登入成功！歡迎, {username}</h2>"
    else:
        return "<h2>登入失敗，帳號或密碼錯誤</h2>"

# ----- API 或其他頁面示範 -----
@app.get("/status")
async def status():
    return {"message": "網站運作中，HelloBot + MathBot 正常啟動"}

# ----- 同時啟動 FastAPI + Discord Bot -----
async def main():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)

    await asyncio.gather(
        server.serve(),
        hellobot.run_bot(),
        mathbot.run_bot()
    )

if __name__ == "__main__":
    asyncio.run(main())
