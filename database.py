import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="project--2"
)

cursor = db.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pib VARCHAR(255),
            birthdate DATE,
            phone_num VARCHAR(255),
            email VARCHAR(255), 
            osvita VARCHAR(255),
            user_id VARCHAR(255)
        )
""")

db.commit()
cursor.close()
db.close()