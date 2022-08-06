from typing import Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import VARCHAR, Column
from sqlalchemy.orm import relationship

from default import ServiceDefault as Service, ControllerDefault as Controller, \
    DataModelDefault, Mix, MessageDataDefault, Base

from record.Record import tag_recorde


class Tag(Base, Mix):
    name = Column(VARCHAR(100), nullable=False, unique=True)
    my_records = relationship('Record', secondary=tag_recorde, back_populates='my_tags')


class TagData(DataModelDefault):
    name: Optional[str]


app = FastAPI()
__controller__ = Controller(Service(database_class=Tag))


@app.get("/{id}", response_class=JSONResponse, response_model=TagData)
@app.get("/", response_class=JSONResponse, response_model=list[TagData])
async def search(name: Optional[str] = '', id: Optional[int] = -1, code: Optional[str] = None):
    return await __controller__.search(name=name, id=id, free_fields={"code": code})


@app.put("/", response_class=JSONResponse, response_model=list[TagData])
@app.post("/", response_class=JSONResponse, response_model=list[TagData], status_code=201)
async def create(account: TagData | list[TagData]):
    return await __controller__.new(data=account)


@app.delete("/{id}", response_model=MessageDataDefault)
async def delete(id: int):
    return await __controller__.delete(id=id, message_sucess={"code": "Ok", "text": f"Tag {id} was deleted."})
