from fastapi import FastAPI, APIRouter

from app.api.holiday import api_router as holiday_router
import database.connection
# from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017/")
# db = client["calendar"]
# collection = db["holiday"]

# class Holiday(BaseModel):
#     title: str
#     day: int
#     month: int
# client = MongoClient("mongodb://localhost:27017/")
# db = client["calendar"]
# collection_holidays = db["holidays"]
# connect_to_mongodb()
app = FastAPI()
api_router = APIRouter()

app.include_router(holiday_router)


@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, World!"}


# @api_router.get("/holidays")
# async def get_holidays(year: Optional[int] = 2023):
#     holidays = []
#     for holiday in collection.find():
#         d = date(year, holiday["month"], holiday["day"])
#         holidays.append(d)
#     start_date = date(year, 1, 1)
#     end_date = date(year, 12, 31)
#     delta = timedelta(days=1)
#     saturdays_and_sundays = []
#
#     while start_date <= end_date:
#         if start_date.weekday() >= 5:
#             saturdays_and_sundays.append(start_date)
#         start_date += delta
#
#     holidays.extend(saturdays_and_sundays)
#     holidays = sorted(holidays)
#
#     result = [d.strftime("%a, %d %b %Y") for d in holidays]
#     return result
#
#
# @api_router.post("/new_holiday")
# async def create_holiday(holiday: Holiday):
#     holiday_data = {
#         "title": holiday.title,
#         "day": holiday.day,
#         "month": holiday.month,
#     }
#     result = collection.insert_one(holiday_data)
#     inserted_id = str(result.inserted_id)
#     response_data = {
#         "id": inserted_id,
#         "title": holiday_data["title"],
#         "day": holiday_data["day"],
#         "month": holiday_data["month"]
#     }
#     return response_data


app.include_router(api_router)

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
