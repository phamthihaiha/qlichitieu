from wsgiref.validate import validator
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
class UserBase(BaseModel):
    username:str
    email=str
class UserCreate(UserBase):
    hash_password: str
    @validator ('password')
    def validate_password(cls,v ):
        if not any(char.isdigit() for char in v):
            raise ValueError(" Password phải có ít nhất 1 chữ số ")
        if not any(char.isupper() for char in v):
            raise ValueError('password phải có it nhất 1 chữ cái in hoa ')
        if not any("!@#$%^&*()_+-=[]{}|;:,.<>?" for char in v):
            raise ValueError('password must containt at least one special character')
        if len(v)<8:
            raise ValueError('Password must be at least 8 characters long')
        return v
class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
class CategoryBase(BaseModel):
    name: str
class CategoryCreate(CategoryBase):
    pass
class CategoryRespone( CategoryBase):
    id:int
    user_id: int

    class Config:
        orm_mode = True
class ExpenseBase(BaseModel):
    amount: float
    description: Optional[str]
    date: Optional[datetime]
    Category_id: int
class ExpenseCreate(ExpenseBase):
    pass
class  ExpenseRespone(ExpenseBase):
    id: int
    user_id: int 
    category=CategoryRespone

    class Config:
        orm_mode = True
class ExpenseAnalytics(BaseModel):
    total_amout:float
    expense_category: dict[str,float]
    month_expense:dict[str,float]
class  ExpenseSearchParams(BaseModel):
    start_date:Optional[datetime]=None
    end_date:Optional[datetime]=None
    category_id:Optional[int]=None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None


 
  

    
