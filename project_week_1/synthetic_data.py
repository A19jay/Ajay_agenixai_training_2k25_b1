import psycopg2
from faker import Faker
import random

# Define the connection parameters
DATABASE_NAME = "lms_db"
USER = "postgres"
PASSWORD = "root"
HOST = "127.0.0.1"

# Define SQL commands for schema creation
schema_creation_commands = [
    "CREATE TABLE IF NOT EXISTS Categories ("
    "CategoryID SERIAL PRIMARY KEY, "
    "CategoryName VARCHAR(100) NOT NULL UNIQUE);",

    "CREATE TABLE IF NOT EXISTS Authors ("
    "AuthorID SERIAL PRIMARY KEY, "
    "FirstName VARCHAR(100) NOT NULL, "
    "LastName VARCHAR(100) NOT NULL, "
    "BirthYear INT);",

    "CREATE TABLE IF NOT EXISTS Books ("
    "BookID SERIAL PRIMARY KEY, "
    "Title VARCHAR(255) NOT NULL, "
    "ISBN VARCHAR(13) NOT NULL UNIQUE, "
    "CategoryID INT NOT NULL, "
    "PublishedYear INT, "
    "Publisher VARCHAR(100), "
    "CONSTRAINT fk_category FOREIGN KEY (CategoryID) REFERENCES Categories (CategoryID) ON DELETE CASCADE);",

    "CREATE TABLE IF NOT EXISTS AuthorBook ("
    "AuthorID INT NOT NULL, "
    "BookID INT NOT NULL, "
    "PRIMARY KEY (AuthorID, BookID), "
    "CONSTRAINT fk_author FOREIGN KEY (AuthorID) REFERENCES Authors (AuthorID) ON DELETE CASCADE, "
    "CONSTRAINT fk_book FOREIGN KEY (BookID) REFERENCES Books (BookID) ON DELETE CASCADE);",

    "CREATE TABLE IF NOT EXISTS Customers ("
    "CustomerID SERIAL PRIMARY KEY, "
    "FirstName VARCHAR(100) NOT NULL, "
    "LastName VARCHAR(100) NOT NULL, "
    "Email VARCHAR(100) NOT NULL UNIQUE, "
    "Phone VARCHAR(15), "
    "Address TEXT);",

    "CREATE TABLE IF NOT EXISTS BookCopies ("
    "CopyID SERIAL PRIMARY KEY, "
    "BookID INT NOT NULL, "
    "LibraryLocation VARCHAR(100), "
    "AvailabilityStatus VARCHAR(20) NOT NULL, "
    "CONSTRAINT fk_bookcopy FOREIGN KEY (BookID) REFERENCES Books (BookID) ON DELETE CASCADE);",

    "CREATE TABLE IF NOT EXISTS Transactions ("
    "TransactionID SERIAL PRIMARY KEY, "
    "CustomerID INT NOT NULL, "
    "CopyID INT NOT NULL, "
    "CheckoutDate DATE NOT NULL, "
    "ReturnDate DATE NOT NULL, "
    "Fine NUMERIC(10, 2), "
    "CONSTRAINT fk_customer FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID) ON DELETE CASCADE, "
    "CONSTRAINT fk_copy FOREIGN KEY (CopyID) REFERENCES BookCopies (CopyID) ON DELETE CASCADE);"
]

# Function to generate and insert synthetic data directly
def insert_synthetic_data(cursor):
    fake = Faker()

    # Insert categories
    categories = ["Fantasy", "Science Fiction", "Mystery", "Biography", "History"]
    for category in categories:
        cursor.execute(f"INSERT INTO Categories (CategoryName) VALUES ('{category}') ON CONFLICT (CategoryName) DO NOTHING;")

    # Insert authors
    for _ in range(10):
        first_name = fake.first_name()
        last_name = fake.last_name()
        birth_year = random.randint(1950, 2000)
        cursor.execute(f"INSERT INTO Authors (FirstName, LastName, BirthYear) VALUES ('{first_name}', '{last_name}', {birth_year});")

    # Insert books
    for _ in range(20):
        title = fake.sentence(nb_words=3).replace("'", "''")
        isbn = fake.isbn13().replace("-", "")[:13]
        category_id = random.randint(1, len(categories))
        published_year = random.randint(1990, 2022)
        publisher = fake.company().replace("'", "''")
        cursor.execute(f"INSERT INTO Books (Title, ISBN, CategoryID, PublishedYear, Publisher) VALUES ('{title}', '{isbn}', {category_id}, {published_year}, '{publisher}');")

    # Link books and authors with duplicate check
    author_book_pairs = set()
    for book_id in range(1, 21):
        author_ids = random.sample(range(1, 11), random.randint(1, 3))
        for author_id in author_ids:
            pair = (author_id, book_id)
            if pair not in author_book_pairs:
                cursor.execute(f"INSERT INTO AuthorBook (AuthorID, BookID) VALUES ({author_id}, {book_id}) ON CONFLICT DO NOTHING;")
                author_book_pairs.add(pair)

    # Insert customers
    for _ in range(20):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone = fake.phone_number()[:15]  # Ensure phone number fits in VARCHAR(15)
        address = fake.address().replace("'", "''")
        cursor.execute(f"INSERT INTO Customers (FirstName, LastName, Email, Phone, Address) VALUES ('{first_name}', '{last_name}', '{email}', '{phone}', '{address}');")

    # Insert book copies
    for _ in range(40):
        book_id = random.randint(1, 20)
        location = fake.city()
        availability_status = random.choice(["Available", "Issued"])
        cursor.execute(f"INSERT INTO BookCopies (BookID, LibraryLocation, AvailabilityStatus) VALUES ({book_id}, '{location}', '{availability_status}');")

    # Insert transactions
    for _ in range(100):
        customer_id = random.randint(1, 20)
        copy_id = random.randint(1, 40)
        checkout_date = fake.date_between(start_date="-1y", end_date="today").strftime('%Y-%m-%d')
        return_date = fake.date_between(start_date=checkout_date, end_date="today").strftime('%Y-%m-%d')
        fine = round(random.uniform(0, 50), 2)

        # Insert using parameterized query
        cursor.execute("""
            INSERT INTO Transactions (CustomerID, CopyID, CheckoutDate, ReturnDate, Fine) 
            VALUES (%s, %s, %s, %s, %s);
        """, (customer_id, copy_id, checkout_date, return_date, fine))

# Connect to the existing lms_db database and create tables and insert data
try:
    conn = psycopg2.connect(dbname=DATABASE_NAME, user=USER, password=PASSWORD, host=HOST)
    conn.autocommit = True
    cursor = conn.cursor()

    # Execute each schema creation command
    for command in schema_creation_commands:
        cursor.execute(command)

    print("All tables created successfully.")

    # Insert synthetic data directly
    insert_synthetic_data(cursor)

    print("Synthetic data inserted successfully.")

except Exception as e:
    print(f"Error: {e}")

finally:
    if conn:
        cursor.close()
        conn.close()





















