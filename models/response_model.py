from pydantic import BaseModel
from typing import Optional

class Response(BaseModel):
    title: str
    isbn: int
    author: str
    process_date: str
    royalty_canada_amount: float
    royalty_canada_discr: float
    royalty_chapter_amount: float
    royalty_chapter_discr: float
    royalty_us_amount: float
    royalty_us_discr: float
    royalty_foreign_amount: float
    royalty_foreign_discr: float
    royalty_high_discount_amount: float
    royalty_high_discount_discr: float
    royalty_state_adoption_amount: float
    royalty_state_adoption_discr: float
    royalty_sub_us_amount: float
    royalty_sub_us_discr: float
    royalty_sub_foreign_amount: float
    royalty_sub_foreign_discr: float
    royalty_sub_trial_amount: float
    royalty_sub_trial_discr: float
    royalty_total_DB: float
    royalty_total_latest: float
    royalty_total_disc: float
    royalty_rate_us_response: Optional[str] = None
    can_frn_chptr_state_response: Optional[str] = None
    royalty_rate_high_disc_response: Optional[str] = None
    royalty_rate_sub_response: Optional[str] = None
    royalty_rate_canada_response: Optional[str] = None
    royalty_rate_chapter_response: Optional[str] = None
    royalty_us_discr_response: Optional[str] = None
    royalty_rate_foreign_response: Optional[str] = None
    royalty_rate_state_adoptions_response: Optional[str] = None
    royalty_rate_sub_us_response: Optional[str] = None
    royalty_rate_sub_foreign_response: Optional[str] = None
    royalty_rate_sub_trial_response: Optional[str] = None
    
    