from fastapi import APIRouter
from models.author_model import AuthorData
from models.sales_data_model import SalesData
from models.author_model import AuthorAmountData
from database.db import get_db_connection

router = APIRouter(prefix="/author", tags=["Author"])

# API to fetch author data
@router.get("/getAuthorDetails/{author_name}/{isbn}")
def getAuthorDetails(author_name: str, isbn: str):
    conn = get_db_connection()
    tabular_author_data = conn.execute("SELECT * FROM author_data WHERE isbn=? AND author=?", (int(isbn), author_name)).fetchone()
    conn.close()
    
    # Convert row to AuthorData object
    author_rate_data = AuthorData(
        title=tabular_author_data["title"],
        isbn=tabular_author_data["isbn"],
        author=tabular_author_data["author"],
        royalty_canada=tabular_author_data["royalty_canada"],
        royalty_chapter=tabular_author_data["royalty_chapter"],
        royalty_us=tabular_author_data["royalty_us"],
        royalty_foreign=tabular_author_data["royalty_foreign"],
        royalty_high_discount=tabular_author_data["royalty_high_discount"],
        royalty_state_adoption=tabular_author_data["royalty_state_adoption"],
        royalty_sub_us=tabular_author_data["royalty_sub_us"],
        royalty_sub_foreign=tabular_author_data["royalty_sub_foreign"],
        royalty_sub_trial=tabular_author_data["royalty_sub_trial"]
    )
    
    #Fetch data based on user and isbn
    conn = get_db_connection()
    tabular_sales_data = conn.execute("SELECT * FROM sales_data WHERE isbn=? AND author=?", (int(isbn), author_name)).fetchone()
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
    
    canada_amount = sales_data.sales_canada * author_rate_data.royalty_canada
    chapter_amount = sales_data.sales_chapter * author_rate_data.royalty_chapter
    us_amount = sales_data.sales_us * author_rate_data.royalty_us
    foreign_amount = sales_data.sales_foreign * author_rate_data.royalty_foreign
    high_discount_amount = sales_data.sales_high_discount * author_rate_data.royalty_high_discount
    state_adoption_amount = sales_data.sales_state_adoption * author_rate_data.royalty_state_adoption
    sub_us_amount = sales_data.sales_sub_us * author_rate_data.royalty_sub_us
    sub_foreign_amount = sales_data.sales_sub_foreign * author_rate_data.royalty_sub_foreign
    sub_trail_amount = sales_data.sales_sub_trial * author_rate_data.royalty_sub_trial
    
    total = canada_amount+chapter_amount+us_amount+foreign_amount+high_discount_amount+state_adoption_amount+sub_us_amount+sub_foreign_amount+sub_trail_amount

    #Formulate and return the response
    return AuthorAmountData(title=sales_data.title, 
                    isbn=sales_data.isbn, 
                    author=sales_data.author, 
                    royalty_canada_amount=canada_amount,
                    royalty_chapter_amount=chapter_amount,
                    royalty_us_amount=us_amount,
                    royalty_foreign_amount=foreign_amount,
                    royalty_high_discount_amount=high_discount_amount,
                    royalty_state_adoption_amount=state_adoption_amount,
                    royalty_sub_us_amount=sub_us_amount,
                    royalty_sub_foreign_amount=sub_foreign_amount,
                    royalty_sub_trial_amount=sub_trail_amount,
                    royalty_total_amount=total,
                    royalty_canada = author_rate_data.royalty_canada,
                    royalty_chapter = author_rate_data.royalty_chapter,
                    royalty_us = author_rate_data.royalty_us,
                    royalty_foreign=author_rate_data.royalty_foreign,
                    royalty_high_discount=author_rate_data.royalty_high_discount,
                    royalty_state_adoption=author_rate_data.royalty_state_adoption,
                    royalty_sub_us=author_rate_data.royalty_sub_us,
                    royalty_sub_foreign=author_rate_data.royalty_sub_foreign,
                    royalty_sub_trial=author_rate_data.royalty_sub_trial,
                    sales_total=sales_data.sales_total,
                    sales_canada=sales_data.sales_canada,
                    sales_chapter=sales_data.sales_chapter,
                    sales_us=sales_data.sales_us,
                    sales_foreign=sales_data.sales_foreign,
                    sales_high_discount=sales_data.sales_high_discount,
                    sales_state_adoption=sales_data.sales_state_adoption,
                    sales_sub_us=sales_data.sales_sub_us,
                    sales_sub_foreign=sales_data.sales_sub_foreign,
                    sales_sub_trial=sales_data.sales_sub_trial)
    
    
# API to add new sales data
@router.post("/updateAuthorData")
def addSalesData(authorAmountData: AuthorAmountData):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO author_calculated_data 
                   (title, isbn, author, royalty_canada_amount, royalty_chapter_amount, royalty_us_amount, royalty_foreign_amount, royalty_high_discount_amount, royalty_state_adoption_amount, royalty_sub_us_amount, royalty_sub_foreign_amount, royalty_sub_trial_amount, royalty_total_amount) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(isbn, author) DO UPDATE SET
                        title = excluded.title,
                        royalty_canada_amount = excluded.royalty_canada_amount,
                        royalty_chapter_amount = excluded.royalty_chapter_amount,
                        royalty_us_amount = excluded.royalty_us_amount,
                        royalty_foreign_amount = excluded.royalty_foreign_amount,
                        royalty_high_discount_amount = excluded.royalty_high_discount_amount,
                        royalty_state_adoption_amount = excluded.royalty_state_adoption_amount,
                        royalty_sub_us_amount = excluded.royalty_sub_us_amount,
                        royalty_sub_foreign_amount = excluded.royalty_sub_foreign_amount,
                        royalty_sub_trial_amount = excluded.royalty_sub_trial_amount,
                        royalty_total_amount = excluded.royalty_total_amount
                    """, 
                   (authorAmountData.title, authorAmountData.isbn, authorAmountData.author, authorAmountData.royalty_canada_amount, authorAmountData.royalty_chapter_amount, authorAmountData.royalty_us_amount, authorAmountData.royalty_foreign_amount, authorAmountData.royalty_high_discount_amount, authorAmountData.royalty_state_adoption_amount, authorAmountData.royalty_sub_us_amount, authorAmountData.royalty_sub_foreign_amount, authorAmountData.royalty_sub_trial_amount, authorAmountData.royalty_total_amount))
    
    conn.commit()
    conn.close()
    return {"message": "Author data updated successfully"}



# API to add new sales data
@router.get("/getAllAuthorData")
def addSalesData():
    conn = get_db_connection()
    tabular_author_data = conn.execute("SELECT * FROM author_calculated_data").fetchall()
    conn.close()
    return [dict(data) for data in tabular_author_data]


# API to add new sales data
@router.get("/getAuthorRoyaltyRate")
def addSalesData():
    conn = get_db_connection()
    tabular_author_data = conn.execute("SELECT * FROM author_data").fetchall()
    conn.close()
    return [dict(data) for data in tabular_author_data]