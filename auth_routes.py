from fastapi import APIRouter, Depends, HTTPException, status
from models import Usuario
from dependencies import get_session
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(email: str): 
    token = f"kasjhndioashb{email}"
    return token

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
    
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session = Depends(get_session)):
    usuario = session.query(Usuario).filter(Usuario.email == login_schema.email).first()
    if not usuario:
          raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário não encontrado" 
            )
    else: 
        access_token = create_token(usuario.email)
        return {
            "access_token": access_token, 
                "token_type": "bearer"
            }