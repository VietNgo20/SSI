from fastapi import APIRouter
from datetime import date, timedelta
from typing import Optional
from ..database.connection import collection_holidays
from ..model.holiday import Holiday

api_router = APIRouter()


@api_router.get("/holidays")
async def get_holidays(year: Optional[int] = 2023):
    holidays = []
    for holiday in collection_holidays.find():
        d = date(year, holiday["month"], holiday["day"])
        holidays.append(d)
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    delta = timedelta(days=1)
    saturdays_and_sundays = []

    while start_date <= end_date:
        if start_date.weekday() >= 5:
            saturdays_and_sundays.append(start_date)
        start_date += delta

    holidays.extend(saturdays_and_sundays)
    holidays = sorted(holidays)

    result = [d.strftime("%a, %d %b %Y") for d in holidays]
    return result


@api_router.post("/new_holiday")
async def create_holiday(holiday: Holiday):
    holiday_data = {
        "title": holiday.title,
        "day": holiday.day,
        "month": holiday.month,
    }
    result = collection_holidays.insert_one(holiday_data)
    inserted_id = str(result.inserted_id)
    response_data = {
        "id": inserted_id,
        "title": holiday_data["title"],
        "day": holiday_data["day"],
        "month": holiday_data["month"]
    }
    return response_data
