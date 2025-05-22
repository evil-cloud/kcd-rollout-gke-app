from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    service: str

class VersionResponse(BaseModel):
    version: str

class MessageResponse(BaseModel):
    message: str