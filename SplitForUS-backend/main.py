from fastapi import FastAPI

from database import Base, engine     
import models                         

Base.metadata.create_all(bind=engine)



from routes import auth, create, join, table, expense

app = FastAPI(title="SplitForUS API")

# 3) Router’ları kaydet
app.include_router(auth.router,   prefix="/auth",    tags=["auth"])
app.include_router(create.router, prefix="",          tags=["create"])
app.include_router(join.router,   prefix="",          tags=["join"])
app.include_router(table.router,  prefix="",          tags=["table"])
app.include_router(expense.router,prefix="",          tags=["expense"])
