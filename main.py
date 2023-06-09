from fastapi import FastAPI, Depends, status, HTTPException, Response
from database import engine, get_db
from models import Base, Product
from sqlalchemy.orm import Session
from schemas import Products

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/product")
def create(product: Products, db: Session = Depends(get_db)):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/product")
def get(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.put("/update/{id}")
def update(id: int, product:Products, db: Session = Depends(get_db)):
    updated_product = db.query(Product).filter(Product.id == id)
    updated_product.first()
    if not updated_product:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with such {id} does not exist")
    else:
        updated_product.update(product.dict(), synchronize_session=False)
        db.commit()
    return updated_product.first()

@app.delete("/delete/{id}")
def delete(id: int, db: Session = Depends(get_db), status_code=status.HTTP_204_NO_CONTENT):
    delete_product = db.query(Product).filter(Product.id == id)

    if not delete_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found to delete")
    else:
        delete_product.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status_code)