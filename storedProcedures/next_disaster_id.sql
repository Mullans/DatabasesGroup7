DELIMITER //
CREATE PROCEDURE next_disaster_id()
	BEGIN
    SELECT DisasterID FROM Disasters
    ORDER BY DisasterID DESC
    LIMIT 1;
    END //
DELIMITER ;