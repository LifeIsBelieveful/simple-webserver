from pydantic import BaseModel

# 요청 데이터 모델
class CoinPriceRequest(BaseModel):
    coin_name: str  # 코인명 (예: 비트코인)
    purchase_price: float  # 구매 당시 가격