from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import login, oil_marketing_companies

app = FastAPI()

app.include_router(login.router)
app.include_router(oil_marketing_companies.router)

origins = [
    'http://127.0.0.1:3000',
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
