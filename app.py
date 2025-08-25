from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
      <head>
        <title>Telegram → Gmail Forwarder</title>
        <style>
          body { font-family: Arial, sans-serif; background: #f4f6f8; text-align: center; padding: 40px; }
          .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.2); }
          h1 { color: #333; }
          p { color: #555; }
          .footer { margin-top: 30px; font-size: 12px; color: gray; }
        </style>
      </head>
      <body>
        <div class="card">
          <h1>🚀 Telegram → Gmail Forwarder</h1>
          <p>Bot is running and listening for new Telegram messages.</p>
          <p>Private + Group messages will be sent to your Gmail inbox.</p>
        </div>
        <div class="footer">
          <p>Made with ❤️ using Telethon + FastAPI</p>
        </div>
      </body>
    </html>
    """

