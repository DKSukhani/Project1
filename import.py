import secret
import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(secret.books_database_url)
db = scoped_session(sessionmaker(bind=engine))

def main():
    print("Attempting to open the CSV")
    f = open("books.csv")
    print("Opened - Checked; Attempting to read the CSV")
    reader = csv.reader(f)
    print("Opened, Read- Checked; Attempting to import the data the CSV")
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                        {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added books with {isbn}, {title} by {author}, released in {year}.")
    db.commit()

if __name__ == "__main__":
    main()


