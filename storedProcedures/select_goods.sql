DELIMITER //
CREATE PROCEDURE select_goods(
)
	BEGIN
    SELECT * FROM PossibleGoods 
    Order By Name;
    END //
DELIMITER ;