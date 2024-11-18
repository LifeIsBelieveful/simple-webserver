import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import webhook

app = FastAPI()
app.include_router(webhook.router)
app.mount("/", StaticFiles(directory="public", html = True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)