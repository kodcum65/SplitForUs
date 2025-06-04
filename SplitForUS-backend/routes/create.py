from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas
from database import get_db, load_data, save_data

router = APIRouter()

def generate_code(length: int = 6) -> str:
    import random, string
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

@router.post("/create_table")
def create_table(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.is_paid and current_user.created_tables_count >= 2:
        raise HTTPException(status_code=402, detail="Ücretsiz kota doldu, ödeme yapmalısınız.")

    data = load_data()
    code = generate_code()
    while code in data:
        code = generate_code()

    data[code] = {"users": [current_user.username], "expenses": []}

    current_user.created_tables_count += 1
    db.add(current_user)
    db.commit()

    save_data(data)
    return {"code": code}


