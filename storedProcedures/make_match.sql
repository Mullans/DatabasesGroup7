DELIMITER //
CREATE PROCEDURE make_match(
	IN requestID INT, IN offerID INT
)
	BEGIN
    SELECT @claimAmount := LEAST(o.QuantityNeeded - o.QuantityReceived, r.QuantityOffered - r.QuantityClaimed)
    FROM Offers as o, Requests as r
    WHERE o.OfferID = offerID AND r.RequestID = requestID;

    UPDATE Offers
    SET QuantityClaimed = QuantityClaimed + @claimAmount
    WHERE OfferID = offerID;

    UPDATE Requests
    SET QuantityReceived = QuantityReceived + @claimAmount
    WHERE RequestID = requestID;

    INSERT INTO Matches (OfferID, RequestID, Status)
    VALUES (requestID, offerID, "pending");
    END //
DELIMITER ;
