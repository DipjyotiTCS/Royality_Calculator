from pydantic import BaseModel

class AuthorAmountData(BaseModel):
    title: str
    isbn: int
    author: str
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