DELIMITER //
CREATE PROCEDURE offer_for_request(
	IN userID INT, IN disasterID INT, IN goodsID INT
)
	BEGIN
    SELECT OfferID, QuantityOffered, QuantityClaimed, DatePosted, Duration
    FROM Requests
    WHERE (userID != UserID) AND (QuantityClaimed < QuantityOffered) AND (DisasterID = disasterID) AND (GoodsID = goodsID) AND (DATE_ADD(DatePosted, INTERVAL Duration DAY) > NOW());    
    END //
DELIMITER ;
