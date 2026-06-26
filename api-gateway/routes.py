from pydantic import BaseModel


class ProcessRequest(BaseModel):
    number: int