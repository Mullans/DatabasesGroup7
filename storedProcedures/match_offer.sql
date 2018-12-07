DELIMITER //
CREATE PROCEDURE requests_for_offer(
	IN userID INT, IN disasterID INT, IN goodsID INT
)
	BEGIN
    SELECT RequestID, QuantityNeeded, QuantityReceived, DatePosted, Duration
    FROM Requests
    WHERE (userID != UserID) AND (QuantityNeeded < QuantityReceived) AND (DisasterID = disasterID) AND (GoodsID = goodsID) AND (DATE_ADD(DatePosted, INTERVAL Duration DAY) > NOW());    
    END //
DELIMITER ;
