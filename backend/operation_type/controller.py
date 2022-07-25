from typing import Optional

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .data import OperationTypeData
from .service import OperationTypeService
from startup import get_db

app = FastAPI()

templates = Jinja2Templates(directory='operation_type/templates')


@app.post("/", response_class=JSONResponse)
def new(request: Request, operation_type: OperationTypeData | list[OperationTypeData], db: Session = Depends(get_db)):
    operations_type: list[OperationTypeData] = []
    if isinstance(operation_type, list):
        for data in operation_type:
            operations_type.append(OperationTypeService.new(db, data))
    else:
        operations_type.append(OperationTypeService.new(db, operation_type))
    return templates.TemplateResponse('fulldata.json', {"request": request, "operations": operations_type},
                                      headers={'content-type': 'application/json'})


@app.get("/", response_class=JSONResponse)
def search(request: Request, name: Optional[str] = "", db: Session = Depends(get_db)):
    return templates.TemplateResponse('fulldata.json', {"request": request,
                                                        "operations": OperationTypeService.search(db, name)},
                                      headers={'content-type': 'application/json'})
