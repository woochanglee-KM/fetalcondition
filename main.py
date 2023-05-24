from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routes.bpm_routes import router as bpm

app = FastAPI() # FastAPI 모듈

#Cors정책 예외처리
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(bpm)
