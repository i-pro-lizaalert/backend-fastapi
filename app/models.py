from pydantic import BaseModel, Field


class SuccessfullResponse(BaseModel):
    details: str = Field('Выполнено', title='Статус операции')

