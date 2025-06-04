# SplitForUS-backend/routes/auth.py

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta

import models, schemas, utils
from database import get_db

router = APIRouter()

# ---------- JWT Ayarları ----------
SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")  # Ortam değişkeninden okuyun.
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 gün

# passlib ile parola hash/verify
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

### YARDIMCI FONKSİYONLAR ##################################

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(OAuth2PasswordRequestForm), db: Session = Depends(get_db)):
    from fastapi.security import OAuth2PasswordBearer
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
    token_str = await oauth2_scheme(token)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Geçersiz veya Süresi Dolmuş Token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token_str, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

### 1) KAYIT (REGISTER) ####################################
@router.post("/auth/register", status_code=201)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1) Aynı username var mı?
    if get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="Kullanıcı adı zaten kullanılıyor.")
    # 2) Aynı email var mı?
    if get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı.")

    # 3) Parolayı hash'le
    hashed_pw = get_password_hash(user_in.password)

    # 4) E-posta doğrulama kodu üret
    email_code = utils.generate_verification_code()

    # 5) Yeni kullanıcı objesi yarat
    new_user = models.User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pw,
        email_verified=False,
        email_verification_code=email_code
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 6) E-posta doğrulama maili gönder
    subject = "SplitForUs - E-posta Doğrulama Kodu"
    body = (
        f"Merhaba {new_user.username},\n\n"
        f"SplitForUs hesabınızı etkinleştirmek için aşağıdaki doğrulama kodunu kullanın:\n\n"
        f"Kod: {email_code}\n\n"
        "Teşekkürler!"
    )
    try:
        utils.send_email(new_user.email, subject, body)
    except Exception as e:
        # Geliştirme aşamasında SMTP bilgileri yoksa konsola kodu bastırıyoruz
        print("E-posta gönderme hatası:", e)
        print("Doğrulama kodu (konsolda):", email_code)

    return {"message": "Kayıt başarılı. Lütfen e-posta adresinizi doğrulayın."}


### 2) E-POSTA DOĞRULAMA (VERIFY EMAIL) #####################
@router.post("/auth/verify-email")
def verify_email(data: schemas.UserVerifyEmail, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    if user.email_verified:
        return {"message": "E-posta zaten doğrulanmış."}
    if user.email_verification_code != data.code:
        raise HTTPException(status_code=400, detail="Geçersiz doğrulama kodu.")
    # Doğrulama başarılı
    user.email_verified = True
    user.email_verification_code = None
    db.add(user)
    db.commit()
    return {"message": "E-posta başarıyla doğrulandı."}
    ### 2b) DOĞRULAMA KODU YENİDEN GÖNDER #########################
@router.post("/auth/resend-verification")
def resend_verification_email(data: schemas.UserEmail, db: Session = Depends(get_db)):
    """Kullanıcıya yeni bir e-posta doğrulama kodu gönderir."""
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
    if user.email_verified:
        return {"message": "E-posta zaten doğrulanmış."}

    email_code = utils.generate_verification_code()
    user.email_verification_code = email_code
    db.add(user)
    db.commit()

    subject = "SplitForUs - E-posta Doğrulama Kodu"
    body = (
        f"Merhaba {user.username},\n\n"
        f"SplitForUs hesabınızı etkinleştirmek için aşağıdaki doğrulama kodunu kullanın:\n\n"
        f"Kod: {email_code}\n\n"
        "Teşekkürler!"
    )
    try:
        utils.send_email(user.email, subject, body)
    except Exception as e:
        print("E-posta gönderme hatası:", e)
        print("Doğrulama kodu (konsolda):", email_code)

    return {"message": "Doğrulama e-postası gönderildi."}


### 3) GİRİŞ (LOGIN) #########################################
@router.post("/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    form_data.username: identifier (username veya email)
    form_data.password: şifre
    """
    identifier = form_data.username
    password = form_data.password

    # 1) Kullanıcıyı bul (username → email)
    user = get_user_by_username(db, identifier)
    if not user:
        user = get_user_by_email(db, identifier)

    if not user:
        raise HTTPException(status_code=401, detail="Kullanıcı adı veya e-posta bulunamadı.")

    # 2) Parola doğrulama
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Hatalı parola.")

    # 3) E-posta doğrulaması yapılmış mı kontrolü
    if not user.email_verified:
        raise HTTPException(status_code=401, detail="Lütfen önce e-posta adresinizi doğrulayın.")

    # 4) Token üret ve döndür
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


### 4) KULLANICI BİLGİSİ (GET CURRENT USER INFO) ##############
@router.get("/auth/user/info", response_model=schemas.UserInfo)
def user_info(current_user: models.User = Depends(get_current_user)):
    return schemas.UserInfo(
        username=current_user.username,
        email=current_user.email,
        created_tables_count=current_user.created_tables_count,
        is_paid=current_user.is_paid,
        email_verified=current_user.email_verified
    )

