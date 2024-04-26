# 查询读者 Rose 的读者号和地址
use DB;

SELECT ID, address FROM Reader WHERE name = 'Rose';

# 查询读者 Rose 所借阅读书(包括已还和未还图书)的图书名和借期;
SELECT Book.name, Borrow.Borrow_Date, Borrow.Return_Date 
FROM Borrow, Book, Reader 
WHERE Borrow.reader_ID = Reader.ID and Reader.name = 'Rose' and Borrow.book_ID = Book.ID;

# 查询未借阅图书的读者姓名;
SELECT Reader.name 
FROM Reader
WHERE Reader.ID NOT IN (SELECT Borrow.reader_ID FROM Borrow);

# 查询 Ullman 所写的书的书名和单价;
SELECT name, price
FROM Book
WHERE author = 'Ullman';

# 查询读者“李林”借阅未还的图书的图书号和书名;
SELECT Book.ID, Book.name
FROM Book, Borrow, Reader
WHERE Borrow.reader_ID = Reader.ID and Reader.name = '李林' 
    and Borrow.book_ID = Book.ID and Borrow.Return_Date is null;

# 查询借阅图书数目超过 3 本的读者姓名;
SELECT name
FROM Reader
JOIN Borrow ON Borrow.reader_ID = Reader.ID
GROUP BY Reader.name
HAVING COUNT(Borrow.Book_ID) > 3;

# 查询没有借阅读者“李林”所借的任何一本书的读者姓名和读者号;
SELECT Reader.name, Reader.ID
FROM Reader
WHERE Reader.ID NOT IN (
    SELECT Borrow.Reader_ID
    FROM Borrow
    WHERE Borrow.book_ID IN (
        SELECT Borrow.book_ID
        FROM Borrow, Reader
        WHERE Reader.name = '李林' AND Borrow.Reader_ID = Reader.ID
    )
);

# 查询书名中包含“MySQL”的图书书名及图书号;
SELECT ID, name
FROM Book
WHERE name like '%MySQL%';

# 查询 2021 年借阅图书数目排名前 20 名的读者号、姓名、年龄以及借阅图书数
SELECT Reader.ID, Reader.name, Reader.age, COUNT(Borrow.book_ID) as borrow_num
FROM Reader, Borrow
WHERE Reader.ID = Borrow.reader_ID and Borrow.Borrow_Date >= '2021-01-01' and Borrow.Borrow_Date < '2022-01-01'
GROUP BY Reader.ID
ORDER BY borrow_num DESC
LIMIT 20;

# 创建一个读者借书信息的视图，该视图包含读者号、姓名、所借图书号、图书名和借期;
CREATE OR REPLACE view BorrowInfo AS
SELECT Reader.ID, Reader.name AS reader_name, Borrow.book_ID, Book.name AS book_name, Borrow.Borrow_Date, Borrow.Return_Date
FROM Reader, Borrow, Book
WHERE Reader.ID = Borrow.reader_ID and Borrow.book_ID = Book.ID;

# 并使用该视图查询最近一年所有读者的读者号以及所借阅的不同图书数;
SELECT ID, COUNT(DISTINCT book_ID) as borrow_num
FROM BorrowInfo
WHERE Borrow_Date >= '2023-04-25'
GROUP BY ID;