from pydantic import BaseModel
from typing import Optional

class RoyaltyDiscrepancies(BaseModel):
    royalty_canada_discr_reason: Optional[str] = None
    royalty_chapter_discr_reason: Optional[str] = None
    royalty_us_discr_response: Optional[str] = None
    royalty_foreign_discr_reponse: Optional[str] = None
    royalty_high_discount_discr_response: Optional[str] = None
    royalty_state_adoption_discr_response: Optional[str] = None
    royalty_sub_us_discr_response: Optional[str] = None
    royalty_sub_foreign_discr_response: Optional[str] = None
    royalty_sub_trial_discr_response: Optional[str] = None