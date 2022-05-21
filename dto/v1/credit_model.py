from pydantic import BaseModel


class CreditData(BaseModel):
    age: int
    gender: str
    source_income: str
    income_last_year: int
    credit_rate: int
    credit_sum: float
    maturity: int
    goal: str
