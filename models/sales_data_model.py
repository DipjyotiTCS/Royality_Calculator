from pydantic import BaseModel

class SalesData(BaseModel):
    title: str
    isbn: int
    author: str
    process_date: str
    sales_total: int
    sales_canada: int
    sales_chapter: int
    sales_us: int
    sales_foreign: int
    sales_high_discount: int
    sales_state_adoption: int
    sales_sub_us: int
    sales_sub_foreign: int
    sales_sub_trial: int

