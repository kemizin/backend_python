from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    user: str = Field(min_length=3)
    senha: str = Field(min_length=6)

class UserCreate(BaseModel):
    user: str = Field(min_length=3)
    senha: str = Field(min_length=6)

class UserResponse(BaseModel):
    user: str

#modelos de classes para requisições e respostas