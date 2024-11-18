import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from routers import webhook
from fastapi.exceptions import RequestValidationError

from fastapi.responses import JSONResponse
app = FastAPI()
app.include_router(webhook.router)

# 422 에러 핸들러 추가
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # 로그 출력 (선택 사항)
    print(f"422 오류 발생: {exc}")

    # 사용자 정의 JSON 응답 반환
    return JSONResponse(
        status_code=422,
        content={
            "error":"Unprocessable Entity",
            "message":"요청 데이터가 올바르지 않습니다.",
            "detail":exc.errors(),  # FastAPI가 기본적으로 제공하는 상세 오류 정보
            "body":await request.body()  # 요청 본문 (선택 사항, 디버깅에 유용)
        },
    )
app.mount("/", StaticFiles(directory="public", html = True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)