from typing import Optional

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .data import OperationTypeData
from .service import OperationTypeService

from startup import get_db
from Data import DefaultMessageData

app = FastAPI()

templates = Jinja2Templates(directory='operation_type/templates')
default_templates = Jinja2Templates(directory="Templates")


@app.put("/", response_class=JSONResponse, status_code=200, response_model=list[OperationTypeData])
@app.post("/", response_class=JSONResponse, status_code=201, response_model=list[OperationTypeData])
def new(request: Request, operation_type: OperationTypeData | list[OperationTypeData], db: Session = Depends(get_db)):
    operations_type: list[OperationTypeData] = []
    if isinstance(operation_type, list):
        for data in operation_type:
            operations_type.append(OperationTypeService.save(db, data))
    else:
        operations_type.append(OperationTypeService.save(db, operation_type))
    return templates.TemplateResponse('fulldata.json', {"request": request, "operations": operations_type},
                                      headers={'content-type': 'application/json'},
                                      status_code=201 if request.method == 'POST' else 200)


@app.get("/{id}", response_class=JSONResponse, response_model=OperationTypeData)
@app.get("/", response_class=JSONResponse, response_model=list[OperationTypeData])
def search(request: Request, name: Optional[str] = "", id: Optional[int] = -1, db: Session = Depends(get_db)):
    if id < 0:
        return templates.TemplateResponse('fulldata.json', {"request": request,
                                                            "operations": OperationTypeService.search(db, name)},
                                          headers={'content-type': 'application/json'})
    else:
        operation = OperationTypeService.get(db, id)
        if operation:
            return templates.TemplateResponse('one.json', {"request": request,
                                                           "operation": OperationTypeService.get(db, id)},
                                              headers={'content-type': 'application/json'})
        return default_templates.TemplateResponse('msg.json', {"request": request,
                                                               "message": {"code": "erro",
                                                                           "text": "não encontrado"}},
                                                  headers={"content-type": "application/json"},
                                                  status_code=404)


@app.delete("/{id}", response_class=JSONResponse, response_model=DefaultMessageData)
def delete(request: Request, id: int, db: Session = Depends(get_db)):
    if OperationTypeService.delete(db, id):
        return default_templates.TemplateResponse('msg.json', {"request": request,
                                                               "message": {
                                                                   "code": "Ok",
                                                                   "text": f"The Operation {id} was deleted."}},
                                                  headers={'content-type': 'application/json'})
    return default_templates.TemplateResponse('msg.json', {"request": request,
                                                           "message": {
                                                               "code": "Error",
                                                               "text": f"Imposible to delete Operation {id}."}},
                                              headers={'content-type': 'application/json'},
                                              status_code=404)
