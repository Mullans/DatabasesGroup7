DELIMITER //
CREATE PROCEDURE goods_categories()
BEGIN
	SELECT Category
	FROM PossibleGoods
	GROUP BY Category;
END //
DELIMITER ;

