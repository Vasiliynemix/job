import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI

from api.handlers import router_user
from api.login_handler import router_login
from settings import DEV_HOST
from settings import DEV_PORT

app = FastAPI(title="Title")

main_app_router = APIRouter()

main_app_router.include_router(router_user, prefix="/user", tags=["User"])
main_app_router.include_router(router_login, prefix="/login", tags=["Login"])
app.include_router(main_app_router)

if __name__ == "__main__":
    uvicorn.run(app, host=DEV_HOST, port=int(DEV_PORT))
