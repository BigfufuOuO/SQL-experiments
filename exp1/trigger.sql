CREATE TRIGGER BookBorrowed
AFTER INSERT ON Borrow
FOR EACH ROW
BEGIN
    UPDATE Book
    SET status = 1, times = times + 1
    WHERE ID = NEW.book_ID;
END;

CREATE TRIGGER BookReturned
AFTER UPDATE ON Borrow
FOR EACH ROW
BEGIN
    IF NEW.Return_Date IS NOT NULL THEN
        UPDATE Book
        SET status = 0
        WHERE ID = NEW.book_ID;
    END IF;
END;