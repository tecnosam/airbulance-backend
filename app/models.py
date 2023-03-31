from bson import ObjectId

from pydantic import BaseModel, validator


class PydanticObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        # if not isinstance(v, ObjectId):
        #     raise TypeError('ObjectId')
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string", example=str(ObjectId()))


class User(BaseModel):
    _id: PydanticObjectId
    name = 'John Doe'
    email: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PydanticObjectId: str}


class Request(BaseModel):

    _id: PydanticObjectId
    user_id: PydanticObjectId
    description: str
    location: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {PydanticObjectId: str}

    @validator("user_id")
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
