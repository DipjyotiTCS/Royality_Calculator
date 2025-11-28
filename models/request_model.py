
from pydantic import BaseModel, field_validator
from typing import Optional

class Request(BaseModel):
    title: str
    isbn: int
    author: str
    process_date: str
    royalty_table_canada: Optional[float]
    royalty_latest_canada: Optional[float]
    royalty_table_chapter: Optional[float]
    royalty_latest_chapter: Optional[float]
    royalty_table_us: Optional[float]
    royalty_latest_us: Optional[float]
    royalty_table_foreign: Optional[float]
    royalty_latest_foreign: Optional[float]
    royalty_table_high_discount: Optional[float]
    royalty_latest_high_discount: Optional[float]
    royalty_table_state_adoption: Optional[float]
    royalty_latest_state_adoption: Optional[float]
    royalty_table_sub_us: Optional[float]
    royalty_latest_sub_us: Optional[float]
    royalty_table_sub_foreign: Optional[float]
    royalty_latest_sub_foreign: Optional[float]
    royalty_table_sub_trial: Optional[float]
    royalty_latest_sub_trial: Optional[float]
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

    @field_validator(
        "royalty_table_canada", "royalty_latest_canada",
        "royalty_table_chapter", "royalty_latest_chapter",
        "royalty_table_us", "royalty_latest_us",
        "royalty_table_foreign", "royalty_latest_foreign",
        "royalty_table_high_discount", "royalty_latest_high_discount",
        "royalty_table_state_adoption", "royalty_latest_state_adoption",
        "royalty_table_sub_us", "royalty_latest_sub_us",
        "royalty_table_sub_foreign", "royalty_latest_sub_foreign",
        "royalty_table_sub_trial", "royalty_latest_sub_trial",
        mode="before"
    )
    def convert_to_float(cls, v):
        if v is None:
            return 0.0
        if isinstance(v, (int, float)):
            return float(v)
        if isinstance(v, str):
            v = v.strip()
            # Try direct conversion
            try:
                return float(v)
            except ValueError:
                # Check if ends with %
                if v.endswith('%'):
                    try:
                        return float(v.rstrip('%'))
                    except ValueError:
                        return 0.0
                return 0.0
        return 0.0
