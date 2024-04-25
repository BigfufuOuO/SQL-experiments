# 查询读者 Rose 的读者号和地址
select ID, address from Reader where name = 'Rose';

# 查询读者 Rose 所借阅读书(包括已还和未还图书)的图书名和借期;
select Book.name, Borrow.Borrow_Date, Borrow.Return_Date 
from Borrow, Book, Reader 
where Borrow.reader_ID = Reader.ID and Reader.name = 'Rose' and Borrow.book_ID = Book.ID;

# 查询未借阅图书的读者姓名;
select Reader.name 
from Reader
where Reader.ID not in (select Borrow.reader_ID from Borrow);

# 查询 Ullman 所写的书的书名和单价;
select name, price
from Book
where author = 'Ullman';

# 查询读者“李林”借阅未还的图书的图书号和书名;
select Book.ID, Book.name
from Book, Borrow, Reader
where Borrow.reader_ID = Reader.ID and Reader.name = '李林' 
    and Borrow.book_ID = Book.ID and Borrow.Return_Date is null;

# 查询借阅图书数目超过 3 本的读者姓名;
select name
from Reader
JOIN Borrow ON Borrow.reader_ID = Reader.ID
GROUP BY Reader.name
HAVING COUNT(Borrow.Book_ID) > 3;

# 查询没有借阅读者“李林”所借的任何一本书的读者姓名和读者号;
select Reader.name, Reader.ID
from Reader
where Reader.ID NOT IN (
    select Borrow.Reader_ID
    from Borrow
    where Borrow.book_ID IN (
        select Borrow.book_ID
        from Borrow, Reader
        where Reader.name = '李林' AND Borrow.Reader_ID = Reader.ID
    )
);

# 查询书名中包含“MySQL”的图书书名及图书号;
select ID, name
from Book
where name like '%MySQL%';
