from fastapi import FastAPI
from controllers import calculatorController
from controllers import authorController
from controllers import WishdomnextRouterController
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# Allow React app origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React app origin
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, etc.
    allow_headers=["*"],  # Authorization, Content-Type, etc.
)


# Include routers
app.include_router(calculatorController.router)
app.include_router(authorController.router)
app.include_router(WishdomnextRouterController.router)

# Initialize DB tables if not exist
conn = sqlite3.connect("local_sales_db.sqlite")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS sales_data (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, isbn INTEGER, author TEXT, process_date TEXT, sales_total INTEGER, sales_canada INTEGER, sales_chapter INTEGER, sales_us INTEGER, sales_foreign INTEGER, sales_high_discount INTEGER, sales_state_adoption INTEGER, sales_sub_us INTEGER, sales_sub_foreign INTEGER, sales_sub_trial INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS author_data (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, isbn INTEGER, author TEXT, royalty_canada REAL, royalty_chapter REAL, royalty_us REAL, royalty_foreign REAL, royalty_high_discount REAL, royalty_state_adoption REAL, royalty_sub_us REAL, royalty_sub_foreign REAL, royalty_sub_trial REAL, UNIQUE(isbn, author))")
cursor.execute("CREATE TABLE IF NOT EXISTS author_calculated_data (id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, title TEXT, isbn INTEGER, author TEXT, royalty_canada_amount REAL, royalty_chapter_amount REAL, royalty_us_amount REAL, royalty_foreign_amount REAL, royalty_high_discount_amount REAL, royalty_state_adoption_amount REAL, royalty_sub_us_amount REAL, royalty_sub_foreign_amount REAL, royalty_sub_trial_amount REAL, royalty_total_amount REAL, UNIQUE(isbn, author))")
conn.commit()

# Insert a sample user if table is empty
cursor.execute("SELECT COUNT(*) FROM sales_data")
count = cursor.fetchone()[0]
if count == 0:
    cursor.execute("INSERT INTO sales_data (title, isbn, author, process_date, sales_total, sales_canada, sales_chapter, sales_us, sales_foreign, sales_high_discount, sales_state_adoption, sales_sub_us, sales_sub_foreign, sales_sub_trial) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ("Reading Program", 1234567890123, "John Doe", "23-Nov-2025​", 337500, 20000, 15000, 70000, 30000, 8000, 15000, 36000, 7000, 15000))
    conn.commit()

cursor.execute("SELECT COUNT(*) FROM author_data")
count = cursor.fetchone()[0]
if count == 0:
    cursor.execute("""INSERT INTO author_data (title, isbn, author, royalty_canada, royalty_chapter, royalty_us, royalty_foreign, royalty_high_discount, royalty_state_adoption, royalty_sub_us, royalty_sub_foreign, royalty_sub_trial) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(isbn, author) DO UPDATE SET
                        title = excluded.title,
                        royalty_canada = excluded.royalty_canada,
                        royalty_chapter = excluded.royalty_chapter,
                        royalty_us = excluded.royalty_us,
                        royalty_foreign = excluded.royalty_foreign,
                        royalty_high_discount = excluded.royalty_high_discount,
                        royalty_state_adoption = excluded.royalty_state_adoption,
                        royalty_sub_us = excluded.royalty_sub_us,
                        royalty_sub_foreign = excluded.royalty_sub_foreign,
                        royalty_sub_trial = excluded.royalty_sub_trial
                   """, 
                   ("Reading Program", 1234567890123, "John Doe", 0.15, 0.1, 0.15, 0.15, 0.075, 0.15, 0.15, 0.15, 0))
    conn.commit()
    
cursor.execute("SELECT COUNT(*) FROM author_calculated_data")
count = cursor.fetchone()[0]
if count == 0:
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
                   ("Reading Program", 1234567890123, "John Doe", 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 300.0, 2700))
    conn.commit()

conn.close()