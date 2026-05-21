from fastapi import APIRouter, Depends, HTTPException, status
from models import Usuario
from dependencies import get_session
from main import bcrypt_context
from schemas import UsuarioSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def get_auth():
    return {"message": "Authentication endpoint"}

@auth_router.post("/criar")
async def create_user(usuario_schema: UsuarioSchema, session = Depends(get_session)):

    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um usuário com esse email"
        )
    else: 
        
        hashed_password = bcrypt_context.hash(usuario_schema.senha)
        new_user = Usuario(usuario_schema.nome,usuario_schema.email, hashed_password)
        session.add(new_user)
        session.commit()
        return {"message": f"Usuário criado com sucesso {usuario_schema.email}"}