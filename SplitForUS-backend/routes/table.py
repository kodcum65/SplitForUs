from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import load_data, get_db
from auth import get_current_user
from models import User
from schemas import Expense, Table

router = APIRouter()

@router.get("/table/{code}")
def get_table(
     code: str,
     current_user: User = Depends(get_current_user),
     db: Session       = Depends(get_db),
 ):
    data = load_data()
    if code not in data:
        raise HTTPException(status_code=404, detail="Table not found.")
    # Sadece katılmış olduğu tabloya bakabilir
    if current_user.username not in data[code]["users"]:
        raise HTTPException(status_code=403, detail="Bu tabloya erişim izniniz yok.")
    return data[code]
