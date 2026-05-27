from fastapi import APIRouter, Depends, HTTPException, status
from models import Usuario
from dependencies import get_session
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(id: str, time_expire=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):  
    date_expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dic_info = {"sub": id, "exp": date_expire}
    token = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return token

def authenticate_user(email: str, senha: str, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    if not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

def verify_token(token: str, session = Depends(get_session)):
   usuario = session.query(Usuario).filter(Usuario.id == 6).first()
   return usuario

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
    usuario = authenticate_user(login_schema.email, login_schema.senha, session)
    if not usuario:
          raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário não encontrado ou senha incorreta" 
            )
    else: 
        access_token = create_token(usuario.id)
        refresh_token = create_token(usuario.id, time_expire=timedelta(minutes=15))
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token,
            "token_type": "bearer"
            }
    
@auth_router.post("/refresh")
async def refresh_token(token: str):
    usuario = verify_token(token)
    access_token = create_token(usuario.id)
    return {
            "access_token": access_token, 
            "refresh_token": refresh_token,
            "token_type": "bearer"
            }