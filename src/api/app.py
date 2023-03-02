from fastapi import FastAPI

from src.main import send_daily_report

app = FastAPI()


@app.get("/")
async def root():
    send_daily_report()


