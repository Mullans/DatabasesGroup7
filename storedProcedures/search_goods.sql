DELIMITER //
CREATE PROCEDURE search_goods(
IN searchTerm varchar(45)
)
	BEGIN
    SELECT * FROM PossibleGoods 
    WHERE Name LIKE searchTerm
    Order By Name;
    END //
DELIMITER ;