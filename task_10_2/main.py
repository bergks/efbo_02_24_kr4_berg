from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from models import Cat

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            'field': ' '.join(str(loc) for loc in error['loc']),
            'message': error['msg'],
            'type': error['type']
        })

    return JSONResponse(
        status_code=422,
        content={
            'status_code': 422,
            'message': "Cat's data validation error",
            'error_type': 'ValidationError',
            'detail': errors
        }
    )
cats = []

@app.get('/cats')
def all_cats ():
    return {'cats': cats}

@app.post('/cats')
def register_cat(cat: Cat):
    for exs_cat in cats:
        if exs_cat['name'] == cat.name:
            return JSONResponse(
                status_code=409,
                content={
                    'message': 'Cat with such name already exists',
                    'status': 'duplicated'
                }
            )
    cats.append(cat.model_dump())
    return {
        'message': f'Cat {cat.name} is successfully registered',
        'cat': cat.model_dump()
    }