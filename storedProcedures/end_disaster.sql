DELIMITER //
CREATE PROCEDURE end_disaster(
	IN dID INT
)
	BEGIN
    UPDATE Disasters
    SET Active = 0
    WHERE (DisasterID = dID);
    END //
DELIMITER ;
