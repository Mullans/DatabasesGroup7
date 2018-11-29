DELIMITER //
CREATE PROCEDURE select_disaster(
	IN dID INT
)
	BEGIN
    SELECT * FROM Disasters 
    WHERE (DisasterID = dID);
    END //
DELIMITER ;