from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Query, Request, BackgroundTasks, Form

import requests
from common.consts import DOORAY_ENDPOINT, DOORAY_API_KEY, DAYOFF_CAL_ID, UPBIT_ENDPOINT
from models.models import CoinPriceRequest

router = APIRouter(prefix='/webhook', tags=['webhook'])

def get_coin_market_code(name: str = '비트코인'):
    url = f"{UPBIT_ENDPOINT}/market/all?isDetails=false"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Dooray API call failed: {response.text}")
    markets = [item['market'] for item in response.json() if item['korean_name'] == name]
    krw_markets = [market for market in markets if market.startswith('KRW')]

    return krw_markets[0] if krw_markets else (markets[0] if markets else None)

@router.post("/coinprice")
async def get_coinprice(request: Request):
    body = await request.body()  # 요청 바디 전체 확인
    print(f"Request Body: {body}")

    # try:
    #     # 슬래시 커맨드의 입력 처리
    #     params = text.split()
    #     if len(params) != 2:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="Invalid input format. Use: <coin_name> <purchase_price>"
    #         )
    #
    #     coin_name = params[0]
    #     try:
    #         purchase_price = float(params[1])
    #     except ValueError:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="Purchase price must be a valid number."
    #         )
    #
    #     # 코인 시장 코드 조회
    #     code = get_coin_market_code(coin_name)
    #     if not code:
    #         raise HTTPException(
    #             status_code=400,
    #             detail=f"Invalid coin name: {coin_name}"
    #         )
    #
    #     # 현재 가격 조회
    #     url = f"{UPBIT_ENDPOINT}/ticker?markets={code}"
    #     response = requests.get(url)
    #     if response.status_code != 200:
    #         raise HTTPException(status_code=response.status_code, detail=f"Upbit API 호출 실패: {response.text}")
    #
    #     data = response.json()
    #     trade_price = data[0]["trade_price"]
    #
    #     # 가격 차이 및 상승률 계산
    #     price_difference = trade_price - purchase_price
    #     increase_rate = (price_difference / purchase_price) * 100
    #
    #     # 결과 반환
    #     return {
    #         "response_type": "in_channel",  # Dooray 슬래시 커맨드에서 결과를 공개
    #         "text": f"{coin_name}의 현재 가격은 {trade_price:,.0f} 원입니다.",
    #         "attachments": [
    #             {
    #                 "text": f"구매 가격: {purchase_price:,.0f} 원\n"
    #                         f"가격 차이: {price_difference:,.0f} 원\n"
    #                         f"상승률: {increase_rate:,.2f}%"
    #             }
    #         ]
    #     }
    # except Exception as e:
    #     print(f"에러 발생: {e}")
    #     raise HTTPException(status_code=500, detail=f"서버 처리 중 에러 발생: {e}")

# @router.post("/coinprice")
# async def get_coinprice(request: CoinPriceRequest):
#     try:
#         # print(f"받은 파라미터 - coin_name: {coin_name}, purchase_price: {purchase_price}")
#
#         # request = CoinPriceRequest(coin_name=coin_name, purchase_price=purchase_price)
#
#         code = get_coin_market_code(request.coin_name)
#         print(f"코드 조회 결과: {code}")
#
#         url = f"{UPBIT_ENDPOINT}/ticker?markets={code}"
#         print(f"api 호출 Url: {url}")
#         response = requests.get(url)
#         print(f"api 호출 response: {response}")
#         print(f"api 호출 response 코드: {response.status_code}")
#         print(f"api 호출 response 메시지: {response.text}")
#         if response.status_code != 200:
#             raise HTTPException(status_code=response.status_code, detail=f"Dooray API call failed: {response.text}")
#
#         data = response.json()
#         trade_price = data[0]["trade_price"]
#         print(f"현재 가격: {trade_price}")
#
#         # 가격 차이 계산
#         price_difference = trade_price - request.purchase_price
#         increase_rate = (price_difference / request.purchase_price) * 100
#
#         return {
#             "coin_name":request.coin_name,
#             "market_code":code,
#             "trade_price":f"{trade_price:,.0f}",  # 천 단위 쉼표 추가
#             "purchase_price":f"{request.purchase_price:,.0f}",  # 천 단위 쉼표 추가
#             "price_difference":f"{price_difference:,.0f}",  # 천 단위 쉼표 추가
#             "increase_rate":f"{increase_rate:,.2f}%"
#         }
#     except Exception as e:
#         print(f"에러 발생: {e}")
#         raise HTTPException(status_code=500, detail=f"서버 처리 중 에러 발생: {e}")

    # # Dooray API 호출 함수
    # def call_dooray_api(time_min: str, time_max: str, calendar_id: str):
    #     url = f"{DOORAY_ENDPOINT}/calendar/v1/calendars/*/events"
    #     params = {
    #         "timeMin": time_min,
    #         "timeMax": time_max,
    #         "calendars": calendar_id
    #     }
    #     headers = {
    #         'Authorization': f'dooray-api {DOORAY_API_KEY}'
    #     }
    #     print(f"api 호출 Url: {url}")
    #     print(f"api 호출 headers: {headers}")
    #     print(f"api 호출 params: {params}")
    #     response = requests.get(url, headers=headers, params=params)
    #     print(f"api 호출 response: {response}")
    #     print(f"api 호출 response 코드: {response.status_code}")
    #     print(f"api 호출 response 메시지: {response.text}")
    #     if response.status_code != 200:
    #         raise HTTPException(status_code=response.status_code, detail=f"Dooray API call failed: {response.text}")
    #     return response.json()
    #
    # @router.get("/calendar")
    # async def get_calendar():
    #     try:
    #         # 기본값 설정
    #         today = datetime.now()
    #         time_min = today.strftime("%Y-%m-%dT%H:%M:%S+09:00")
    #         time_max = (today + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S+09:00")
    #
    #         # Dooray API 호출 작업을 백그라운드에서 실행
    #         data = call_dooray_api(time_min, time_max, DAYOFF_CAL_ID)
    #
    #         return {
    #             "data": data
    #         }
    #     except Exception as e:
    #         raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
