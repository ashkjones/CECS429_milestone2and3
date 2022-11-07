import sqlite3

connection = sqlite3.connect("search_engine.db")
cursor = connection.cursor()
print("Connected to Database")
cursor.execute("DROP TABLE IF EXISTS TERM_POSITIONS")

table = """ CREATE TABLE TERM_POSITIONS (
        TERM VARCHAR(255) NOT NULL,
        POSITION INT NOT NULL
        ); """

cursor.execute(table)

pos = 0

term = "poop"

add_term = f"""INSERT into TERM_POSITIONS ('TERM', 'POSITION')
                VALUES
                ('{term}', {pos})"""

cursor.execute(add_term)

connection.commit()