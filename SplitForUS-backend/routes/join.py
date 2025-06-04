from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import load_data, save_data, get_db
from auth import get_current_user
from models import User
from schemas import Expense, Table

router = APIRouter()

@router.post("/join_table")
def join_table(
     code: str,
     alias: str,
     current_user: User = Depends(get_current_user),
     db: Session       = Depends(get_db),
 ):
    data = load_data()
    if code not in data:
        raise HTTPException(status_code=404, detail="Table not found.")
    if alias not in data[code]["users"]:
        data[code]["users"].append(alias)
        save_data(data)
    return {"message": f"{alias} joined table {code}."}
