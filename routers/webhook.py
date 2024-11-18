from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
import requests
from common.consts import DOORAY_ENDPOINT, DOORAY_API_KEY, DAYOFF_CAL_ID

router = APIRouter(prefix='/webhook', tags=['webhook'])

# Dooray API 호출 함수
def call_dooray_api(time_min: str, time_max: str, calendar_id: str):
    url = f"{DOORAY_ENDPOINT}/calendar/v1/calendars/*/events"
    params = {
        "timeMin": time_min,
        "timeMax": time_max,
        "calendars": calendar_id
    }
    headers = {
        'Authorization': f'dooray-api {DOORAY_API_KEY}'
    }
    print(f"api 호출 Url: {url}")
    print(f"api 호출 headers: {headers}")
    print(f"api 호출 params: {params}")
    response = requests.get(url, headers=headers, params=params)
    print(f"api 호출 response: {response}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Dooray API call failed: {response.text}")
    return response.json()

@router.get("/calendar")
async def get_calendar():
    try:
        # 기본값 설정
        today = datetime.now()
        time_min = today.strftime("%Y-%m-%dT%H:%M:%S+09:00")
        time_max = (today + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S+09:00")

        # Dooray API 호출 작업을 백그라운드에서 실행
        data = call_dooray_api(time_min, time_max, DAYOFF_CAL_ID)

        return {
            "data": data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")