from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel  # ¡Nuevo import!
from typing import List  # Para tipado de listas

# Configuración de la base de datos (igual que antes)
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/lesstime_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Modelo SQLAlchemy (para la base de datos)
class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    position = Column(String(50))

# Modelo Pydantic (para la respuesta API)
class EmployeeResponse(BaseModel):
    id: int
    name: str
    position: str

    class Config:
        from_attributes = True  # Habilita la conversión desde ORM

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia (igual que antes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints actualizados con response_model
@app.post("/employees/", response_model=EmployeeResponse)
def create_employee(name: str, position: str, db: Session = Depends(get_db)):
    employee = Employee(name=name, position=position)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee  # Ahora se puede serializar

@app.get("/employees/", response_model=List[EmployeeResponse])  # Lista de empleados
def read_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return employees

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def read_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted"}