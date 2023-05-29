from fastapi import FastAPI, APIRouter

from app.api.holiday import api_router as holiday_router
import database.connection

app = FastAPI()
api_router = APIRouter()

app.include_router(holiday_router)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
