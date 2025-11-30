from fastapi import APIRouter
from models.request_model import Request
from models.response_model import Response
from models.sales_data_model import SalesData
from database.db import get_db_connection

router = APIRouter(prefix="/sales", tags=["Sales"])

#API to perform calculation

@router.post("/calculate")
def calculateSales(request: Request):
    
    #Fetch data based on user and isbn
    conn = get_db_connection()
    tabular_sales_data = conn.execute("SELECT * FROM sales_data WHERE isbn=? AND author=?", (request.isbn, request.author)).fetchone()
    conn.close()
    
  # Convert row to SalesData object
    sales_data = SalesData(
        title=tabular_sales_data["title"],
        isbn=tabular_sales_data["isbn"],
        author=tabular_sales_data["author"],
        process_date=tabular_sales_data["process_date"],
        sales_total=tabular_sales_data["sales_total"],
        sales_canada=tabular_sales_data["sales_canada"],
        sales_chapter=tabular_sales_data["sales_chapter"],
        sales_us=tabular_sales_data["sales_us"],
        sales_foreign=tabular_sales_data["sales_foreign"],
        sales_high_discount=tabular_sales_data["sales_high_discount"],
        sales_state_adoption=tabular_sales_data["sales_state_adoption"],
        sales_sub_us=tabular_sales_data["sales_sub_us"],
        sales_sub_foreign=tabular_sales_data["sales_sub_foreign"],
        sales_sub_trial=tabular_sales_data["sales_sub_trial"]
    )
    
    #Perform calculation
    canada_old_amount = (sales_data.sales_canada * request.royalty_table_canada)/100
    canada_new_amount = (sales_data.sales_canada * request.royalty_latest_canada)/100
    canada_diff = 0 if canada_old_amount == canada_new_amount else (canada_new_amount - canada_old_amount)
    
    chapter_old_amount = (sales_data.sales_chapter * request.royalty_table_chapter)/100
    chapter_new_amount = (sales_data.sales_chapter * request.royalty_latest_chapter)/100
    chapter_diff = 0 if chapter_old_amount == chapter_new_amount else (chapter_new_amount - chapter_old_amount)
    
    us_old_amount = (sales_data.sales_us * request.royalty_table_us)/100
    us_new_amount = (sales_data.sales_us * request.royalty_latest_us)/100
    us_diff = 0 if us_old_amount == us_new_amount else (us_new_amount - us_old_amount)
    
    foreign_old_amount = (sales_data.sales_foreign * request.royalty_table_foreign)/100
    foreign_new_amount = (sales_data.sales_foreign * request.royalty_latest_foreign)/100
    foreign_diff = 0 if foreign_old_amount == foreign_new_amount else (foreign_new_amount - foreign_old_amount)
    
    
    highDiscout_old_amount = (sales_data.sales_high_discount * request.royalty_table_high_discount)/100
    highDiscout_new_amount = (sales_data.sales_high_discount * request.royalty_latest_high_discount)/100
    highDiscout_diff = 0 if highDiscout_old_amount == highDiscout_new_amount else (highDiscout_new_amount - highDiscout_old_amount)
    
    
    stateAdoption_old_amount = (sales_data.sales_state_adoption * request.royalty_table_state_adoption)/100
    stateAdoption_new_amount = (sales_data.sales_state_adoption * request.royalty_latest_state_adoption)/100
    stateAdoption_diff = 0 if stateAdoption_old_amount == stateAdoption_new_amount else (stateAdoption_new_amount - stateAdoption_old_amount)
    
    subUs_old_amount = (sales_data.sales_sub_us * request.royalty_table_sub_us)/100
    subUs_new_amount = (sales_data.sales_sub_us * request.royalty_latest_sub_us)/100
    subUs_diff = 0 if subUs_old_amount == subUs_new_amount else (subUs_new_amount - subUs_old_amount)
    
    subForeign_old_amount = (sales_data.sales_sub_foreign * request.royalty_table_sub_foreign)/100
    subForeign_new_amount = (sales_data.sales_sub_foreign * request.royalty_latest_sub_foreign)/100
    subForeign_diff = 0 if subForeign_old_amount == subForeign_new_amount else (subForeign_new_amount - subForeign_old_amount)
    
    subTrial_old_amount = (sales_data.sales_sub_trial * request.royalty_table_sub_trial)/100
    subTrial_new_amount = (sales_data.sales_sub_trial * request.royalty_latest_sub_trial)/100
    subTrial_diff = 0 if subTrial_old_amount == subTrial_new_amount else (subTrial_new_amount - subTrial_old_amount)
    
    total_db = canada_old_amount+chapter_old_amount+us_old_amount+foreign_old_amount+highDiscout_old_amount+stateAdoption_old_amount+subUs_old_amount+subForeign_old_amount+subTrial_old_amount
    
    total_new = canada_new_amount+us_new_amount+chapter_new_amount+foreign_new_amount+highDiscout_new_amount+stateAdoption_new_amount+subUs_new_amount+subForeign_new_amount+subTrial_new_amount
    
    total_diff = canada_diff+chapter_diff+us_diff+foreign_diff+highDiscout_diff+stateAdoption_diff+subUs_diff+subForeign_diff+subTrial_diff

    #Formulate and return the response
    return Response(title=request.title, 
                    isbn=request.isbn, 
                    author=request.author, 
                    process_date=request.process_date,
                    royalty_canada_amount=round(canada_new_amount, 3),
                    royalty_canada_discr=round(canada_diff, 3),
                    royalty_chapter_amount=round(chapter_new_amount, 3),
                    royalty_chapter_discr=round(chapter_diff, 3),
                    royalty_us_amount=round(us_new_amount, 3),
                    royalty_us_discr=round(us_diff, 3),
                    royalty_foreign_amount=round(foreign_new_amount, 3),
                    royalty_foreign_discr=round(foreign_diff, 3),
                    royalty_high_discount_amount=round(highDiscout_new_amount, 3),
                    royalty_high_discount_discr=round(highDiscout_diff, 3),
                    royalty_state_adoption_amount=round(stateAdoption_new_amount, 3),
                    royalty_state_adoption_discr=round(stateAdoption_diff, 3),
                    royalty_sub_us_amount=round(subUs_new_amount, 3),
                    royalty_sub_us_discr=round(subUs_diff, 3),
                    royalty_sub_foreign_amount=round(subForeign_new_amount, 3),
                    royalty_sub_foreign_discr=round(subForeign_diff, 3),
                    royalty_sub_trial_amount=round(subTrial_new_amount, 3),
                    royalty_sub_trial_discr=round(subTrial_diff, 3),
                    royalty_total_DB=round(total_db, 3),
                    royalty_total_latest=round(total_new, 3),
                    royalty_total_disc=round(total_diff, 3),
                    royalty_rate_us_response=request.royalty_rate_us_response,
                    royalty_rate_high_disc_response=request.royalty_rate_high_disc_response,
                    royalty_rate_sub_response=request.royalty_rate_sub_response,
                    royalty_rate_canada_response=request.royalty_rate_canada_response,
                    royalty_rate_chapter_response=request.royalty_rate_chapter_response,
                    royalty_us_discr_response=request.royalty_us_discr_response,
                    royalty_rate_foreign_response=request.royalty_rate_foreign_response,
                    royalty_rate_state_adoptions_response=request.royalty_rate_state_adoptions_response,
                    royalty_rate_sub_us_response=request.royalty_rate_sub_us_response,
                    royalty_rate_sub_foreign_response=request.royalty_rate_sub_foreign_response,
                    royalty_rate_sub_trial_response=request.royalty_rate_sub_trial_response)

# API to add new sales data
@router.post("/addSalesData")
def addSalesData(salesData: SalesData):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sales_data (title, isbn, author, process_date, sales_total, sales_canada, sales_chapter, sales_us, sales_foreign, sales_high_discount, sales_state_adoption, sales_sub_us, sales_sub_foreign, sales_sub_trial) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (salesData.title, salesData.isbn, salesData.author, salesData.process_date, salesData.sales_total, salesData.sales_canada, salesData.sales_chapter, salesData.sales_us, salesData.sales_foreign, salesData.sales_high_discount, salesData.sales_state_adoption, salesData.sales_sub_us, salesData.sales_sub_foreign, salesData.sales_sub_trial))
    conn.commit()
    conn.close()
    return {"message": "Sales data updated successfully"}
  
  
  
# API to fetch all sales data
@router.get("/getAllSalesData")
def getAllSalesData():
    conn = get_db_connection()
    sales_data = conn.execute("SELECT * FROM sales_data").fetchall()
    conn.close()
    return [dict(data) for data in sales_data]