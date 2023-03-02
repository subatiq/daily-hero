from fastapi import FastAPI, HTTPException, Response

from src.main import send_daily_report

app = FastAPI()


@app.post("/")
async def trigger_daily_report():
    try:
        send_daily_report()
        return Response("OK")

    except Exception as exc:
        raise HTTPException(500, detail=str(exc))


