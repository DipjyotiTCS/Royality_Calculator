from fastapi import APIRouter
import httpx
import re
from typing import Dict, Optional
from models.response_model import Response
from models.royality_discrepancies import RoyaltyDiscrepancies


router = APIRouter(prefix="/router", tags=["Router"])


@router.get("/callWishdomNext")
def callWishdomNext():
    
    url = "https://www.tcsaiwisdomnext.tcsapps.com/wisdomv3/api/publish/published-url/prh-royalty-comparison"
    
    headers = {
               "Content-Type": "application/json",
               "X-BUC-ORG-NAME":"prh_royalty_comparison",
               "X-BUC-ORG-KEY":"k]/oZCbZBR33"
            }
    
    data = {
        "workflow_id": 525,
        "user_prompt": "For Reading Program work of author John Doe find out the latest Royalty rate from the contract and compare with the corresponding royalty rate in the database",
        "should_clear_session": "yes"
    }

    with httpx.Client(timeout=60) as client:
        response = client.post(url, json=data, headers=headers)
        data = response.json()
        
        items = data["state_details"]["responses"]["PRH-calc-royalty"]["1662"]["response"]
        requestItem = data["state_details"]["responses"]["PRH-calc-royalty"]["1662"]["payload"]
        
        model_instance = Response(**items)
            
        return model_instance
                
