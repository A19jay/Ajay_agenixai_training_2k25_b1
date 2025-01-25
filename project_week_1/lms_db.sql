-- Schema creation
CREATE TABLE IF NOT EXISTS Categories (
    CategoryID SERIAL PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Authors (
    AuthorID SERIAL PRIMARY KEY,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    BirthYear INT
);

CREATE TABLE IF NOT EXISTS Books (
    BookID SERIAL PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    ISBN VARCHAR(13) NOT NULL UNIQUE,
    CategoryID INT NOT NULL,
    PublishedYear INT,
    Publisher VARCHAR(100),
    CONSTRAINT fk_category FOREIGN KEY (CategoryID) REFERENCES Categories (CategoryID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AuthorBook (
    AuthorID INT NOT NULL,
    BookID INT NOT NULL,
    PRIMARY KEY (AuthorID, BookID),
    CONSTRAINT fk_author FOREIGN KEY (AuthorID) REFERENCES Authors (AuthorID) ON DELETE CASCADE,
    CONSTRAINT fk_book FOREIGN KEY (BookID) REFERENCES Books (BookID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Customers (
    CustomerID SERIAL PRIMARY KEY,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone VARCHAR(15),
    Address TEXT
);

CREATE TABLE IF NOT EXISTS BookCopies (
    CopyID SERIAL PRIMARY KEY,
    BookID INT NOT NULL,
    LibraryLocation VARCHAR(100),
    AvailabilityStatus VARCHAR(20) NOT NULL,
    CONSTRAINT fk_bookcopy FOREIGN KEY (BookID) REFERENCES Books (BookID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Transactions (
    TransactionID SERIAL PRIMARY KEY,
    CustomerID INT NOT NULL,
    CopyID INT NOT NULL,
    CheckoutDate DATE NOT NULL,
    ReturnDate DATE NOT NULL,
    Fine NUMERIC(10, 2),
    CONSTRAINT fk_customer FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID) ON DELETE CASCADE,
    CONSTRAINT fk_copy FOREIGN KEY (CopyID) REFERENCES BookCopies (CopyID) ON DELETE CASCADE
);

-- Insert synthetic data
DO $$
DECLARE
    fake RECORD;
BEGIN
    FOR fake IN SELECT *
                FROM json_to_recordset('[
                {"category":"Fantasy"}, {"category":"Science Fiction"}, {"category":"Mystery"}, {"category":"Biography"}, {"category":"History"}
                ]') AS x(category VARCHAR(100))
    LOOP
        INSERT INTO Categories (CategoryName) VALUES (fake.category) ON CONFLICT (CategoryName) DO NOTHING;
    END LOOP;

    FOR fake IN 1..10 LOOP
        INSERT INTO Authors (FirstName, LastName, BirthYear)
        VALUES (LEFT(MD5(RANDOM()::TEXT), 10), LEFT(MD5(RANDOM()::TEXT), 10), 1950 + RANDOM() * 50);
    END LOOP;

    FOR fake IN 1..20 LOOP
        INSERT INTO Books (Title, ISBN, CategoryID, PublishedYear, Publisher)
        VALUES (LEFT(MD5(RANDOM()::TEXT), 10), LEFT(MD5(RANDOM()::TEXT), 13), 1 + RANDOM() * 5, 1990 + RANDOM() * 32, LEFT(MD5(RANDOM()::TEXT), 10));
    END LOOP;

    FOR fake IN 1..20 LOOP
        INSERT INTO Customers (FirstName, LastName, Email, Phone, Address)
        VALUES (LEFT(MD5(RANDOM()::TEXT), 10), LEFT(MD5(RANDOM()::TEXT), 10), LEFT(MD5(RANDOM()::TEXT), 10) || '@example.com', LEFT(MD5(RANDOM()::TEXT), 15), LEFT(MD5(RANDOM()::TEXT), 50));
    END LOOP;

    FOR fake IN 1..40 LOOP
        INSERT INTO BookCopies (BookID, LibraryLocation, AvailabilityStatus)
        VALUES (1 + RANDOM() * 20, LEFT(MD5(RANDOM()::TEXT), 10), CASE WHEN RANDOM() < 0.5 THEN 'Available' ELSE 'Issued' END);
    END LOOP;

    FOR fake IN 1..100 LOOP
        INSERT INTO Transactions (CustomerID, CopyID, CheckoutDate, ReturnDate, Fine)
        VALUES (
            1 + RANDOM() * 20,
            1 + RANDOM() * 40,
            (CURRENT_DATE - INTERVAL '1 year' + INTERVAL '1 day' * FLOOR(RANDOM() * 365))::DATE,
            (CURRENT_DATE - INTERVAL '1 year' + INTERVAL '1 day' * FLOOR(RANDOM() * 365))::DATE,
            ROUND(RANDOM() * 50, 2)
        );
    END LOOP;
END $$;

-- Queries

SELECT B.Title, COUNT(T.TransactionID) AS IssueCount
FROM Transactions T
JOIN BookCopies BC ON T.CopyID = BC.CopyID
JOIN Books B ON BC.BookID = B.BookID
GROUP BY B.Title
ORDER BY IssueCount DESC
LIMIT 5;

SELECT B.Title, A.FirstName, A.LastName, B.PublishedYear
FROM Books B
JOIN AuthorBook AB ON B.BookID = AB.BookID
JOIN Authors A ON AB.AuthorID = A.AuthorID
JOIN Categories C ON B.CategoryID = C.CategoryID
WHERE C.CategoryName = 'Fantasy'
ORDER BY B.PublishedYear DESC;

SELECT C.FirstName, C.LastName, COUNT(T.TransactionID) AS BooksBorrowed
FROM Transactions T
JOIN Customers C ON T.CustomerID = C.CustomerID
GROUP BY C.FirstName, C.LastName
ORDER BY BooksBorrowed DESC
LIMIT 3;

SELECT C.FirstName, C.LastName, T.CheckoutDate
FROM Transactions T
JOIN Customers C ON T.CustomerID = C.CustomerID
WHERE T.ReturnDate IS NULL AND T.CheckoutDate < NOW() - INTERVAL '30 days';

SELECT A.FirstName, A.LastName, COUNT(AB.BookID) AS BooksWritten
FROM Authors A
JOIN AuthorBook AB ON A.AuthorID = AB.AuthorID
GROUP BY A.FirstName, A.LastName
HAVING COUNT(AB.BookID) > 3;

SELECT DISTINCT A.FirstName, A.LastName
FROM Authors A
JOIN AuthorBook AB ON A.AuthorID = AB.AuthorID
JOIN Books B ON AB.BookID = B.BookID
JOIN BookCopies BC ON B.BookID = BC.BookID
JOIN Transactions T ON BC.CopyID = T.CopyID
WHERE T.CheckoutDate >= NOW() - INTERVAL '6 months';

SELECT 
    (SELECT COUNT(*) FROM BookCopies WHERE AvailabilityStatus = 'Issued') AS TotalIssuedBooks,
    (SELECT COUNT(*) FROM BookCopies) AS TotalBooks,
    ((SELECT COUNT(*) FROM BookCopies WHERE AvailabilityStatus = 'Issued')::float / (SELECT COUNT(*) FROM BookCopies)::float) * 100 AS IssuedPercentage;

SELECT 
    TO_CHAR(T.CheckoutDate, 'YYYY-MM') AS Month, 
    COUNT(T.TransactionID) AS BookCount,
    COUNT(DISTINCT T.CustomerID) AS UniqueCustomerCount
FROM Transactions T
WHERE T.CheckoutDate >= NOW() - INTERVAL '1 year'
GROUP BY TO_CHAR(T.CheckoutDate, 'YYYY-MM')
ORDER BY Month;

CREATE INDEX idx_books_title ON Books(Title);
CREATE INDEX idx_books_categoryid ON Books(CategoryID);
CREATE INDEX idx_authors_firstname_lastname ON Authors(FirstName, LastName);
CREATE INDEX idx_transactions_checkoutdate ON Transactions(CheckoutDate);
CREATE INDEX idx_transactions_customerid ON Transactions(CustomerID);
CREATE INDEX idx_bookcopies_availabilitystatus ON BookCopies(AvailabilityStatus);
