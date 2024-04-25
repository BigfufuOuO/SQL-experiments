use DB;

CREATE TABLE IF NOT EXISTS Book(
    ID char(8) PRIMARY KEY,
    name varchar(10) NOT NULL,
    author varchar(10) NOT NULL,
    price float,
    status int DEFAULT 0,
    times int DEFAULT 0
);

CREATE TABLE Reader(
    ID char(8) PRIMARY KEY,
    name varchar(10) NOT NULL,
    age int,
    address varchar(20)
);

CREATE TABLE Borrow(
    book_ID char(8),
    reader_ID char(8),
    Borrow_Date date,
    Return_Date date,
    PRIMARY KEY(book_ID, reader_ID),
    FOREIGN KEY(book_ID) REFERENCES Book(ID),
    FOREIGN KEY(reader_ID) REFERENCES Reader(ID)
);