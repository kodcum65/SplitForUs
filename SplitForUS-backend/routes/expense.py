from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from database import load_data, save_data, get_db
from auth import get_current_user
from models import User
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ExpenseIn(BaseModel):
    code: str         # tablo kodu
    who: str          # kim harcama yaptı
    desc: str         # açıklama
    amount: float     # miktar
    date: str         # tarih (örnek: "2025-05-10")
    shared_by: List[str]  # kimler bu harcamaya dahil

@router.post("/add_expense")
def add_expense(
     expense: ExpenseIn = Body(...),
     current_user: User = Depends(get_current_user),
     db: Session       = Depends(get_db),
 ):
    data = load_data()

    if expense.code not in data:
        raise HTTPException(status_code=404, detail="Table not found")
    if current_user.username not in data[expense.code]["users"]:
       raise HTTPException(status_code=403, detail="Bu tabloya erişim izniniz yok.")

    new_expense = {
        "who": expense.who,
        "desc": expense.desc,
        "amount": expense.amount,
        "date": expense.date,
        "shared_by": expense.shared_by
    }

    data[expense.code]["expenses"].append(new_expense)
    save_data(data)
    return {"message": "Expense added successfully"}
