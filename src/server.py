from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import routes_user,routers_donations
# from infra.sqlalchemy.config.database import criar_bd


app  =FastAPI()



origins = ['http://localhost:5000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(routes_user.router,prefix='/auth')
app.include_router(routers_donations.router)


