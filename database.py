import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="my_resume_db"
)

cursor = db.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        pib VARCHAR(255),
        birthdate DATE,
        address VARCHAR(255),
        phone_num VARCHAR(255),
        communication TEXT,
        email VARCHAR(255), 
        osvita VARCHAR(255),
        add_info TEXT
    )
""")
db.commit()
cursor.close()
db.close()