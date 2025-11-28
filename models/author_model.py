from pydantic import BaseModel

class AuthorData(BaseModel):
    title: str
    isbn: int
    author: str
    royalty_canada: float
    royalty_chapter: float
    royalty_us: float
    royalty_foreign: float
    royalty_high_discount: float
    royalty_state_adoption: float
    royalty_sub_us: float
    royalty_sub_foreign: float
    royalty_sub_trial: float
    

class AuthorAmountData(AuthorData):
    royalty_canada_amount: float
    royalty_chapter_amount: float
    royalty_us_amount: float
    royalty_foreign_amount: float
    royalty_high_discount_amount: float
    royalty_state_adoption_amount: float
    royalty_sub_us_amount: float
    royalty_sub_foreign_amount: float
    royalty_sub_trial_amount: float
    royalty_total_amount: float
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