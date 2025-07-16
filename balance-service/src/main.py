import fastapi.responses
from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from balanceservice import BalanceService
from kakfa_consumer import start_consumer
from populate_db import init_db


print('Populating DB...')
init_db()

def main():
    pass

main()

app = FastAPI(
    title='balance service',
    version='1'
)


service: BalanceService = None

@app.on_event('startup')
def startup_event():
    global service

    print('Initializing Balance Service')
    service = BalanceService()

@app.on_event('shutdown')
def shutdown_event():
    global service

    if service:
        service = None
    
    print('Balance Service finished!')

print('Initalizing Kafka...')
start_consumer()


@app.get('/')
async def swagger_home():
    return RedirectResponse(url='/docs')

@app.post('/balances/{account_id}', status_code=status.HTTP_200_OK)
async def get_balance(request: Request, account_id: str):

    global service

    result = service.get_balance(account_id)
    return fastapi.responses.JSONResponse(result, status_code=status.HTTP_201_CREATED)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=3003, reload=True)



