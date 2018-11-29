DELIMITER //
CREATE PROCEDURE short_disasters(
	IN activeCheck INT
)
	BEGIN
    SELECT DisasterID, Name, DisasterLocation, StartDate, Active FROM Disasters 
    WHERE (Active >= activeCheck);
    END //
DELIMITER ;