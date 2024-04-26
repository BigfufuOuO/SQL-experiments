CREATE PROCEDURE UpdateBookID(IN oldID char(8), IN newID char(8))
BEGIN
    IF oldID NOT like '00%' AND newID NOT like '00%' THEN
        UPDATE Book
        SET ID = newID
        WHERE ID = oldID;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Book ID must not start with 00';
    END IF;
END;