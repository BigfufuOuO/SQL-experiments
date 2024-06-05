DELIMITER //
CREATE PROCEDURE UpdateBookID(IN oldID char(8), IN newID char(8))
BEGIN
    IF oldID NOT like '00%' AND newID NOT like '00%' THEN
		SET FOREIGN_KEY_CHECKS = 0;
        UPDATE Book
        SET ID = newID 
        WHERE ID = oldID; 
        UPDATE Borrow
        SET Book_ID = newID
        WHERE Book_ID = oldID;
        SET FOREIGN_KEY_CHECKS = 1;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'error';
    END IF;
END;

