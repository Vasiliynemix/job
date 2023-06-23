import uvicorn
from fastapi import FastAPI, APIRouter

from settings import DEV_HOST, DEV_PORT
from api.handlers import router_user

app = FastAPI(title='Title')

main_app_router = APIRouter()

main_app_router.include_router(router_user, prefix='/user', tags=['User'])
app.include_router(main_app_router)

if __name__ == '__main__':
    uvicorn.run(app, host=DEV_HOST, port=int(DEV_PORT))
