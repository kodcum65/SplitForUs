# SplitForUS-backend/schemas.py

from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional

######################
# -- Kullanıcı Modelleri
######################

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    identifier: str  # Buraya kullanıcı username/email yazacak
    password: str

class UserVerifyEmail(BaseModel):
    email: EmailStr
    code: str  # 6 haneli kod bekliyorum

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserInfo(BaseModel):
    username: str
    email: EmailStr
    created_tables_count: int
    is_paid: bool
    email_verified: bool

######################
# -- Tablo / Harcama Modelleri (Değişmedi)
######################

class Expense(BaseModel):
    who: str
    desc: str
    amount: float
    date: str
    shared_by: List[str]

class Table(BaseModel):
    code: str
    users: List[str]
    expenses: List[Expense]

class ExpenseIn(BaseModel):
    code: str
    who: str
    desc: str
    amount: float
    date: str
    shared_by: List[str]
