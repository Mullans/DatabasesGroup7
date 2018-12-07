CREATE TABLE `PossibleGoods` (
  `GoodsID` int(11) NOT NULL AUTO_INCREMENT,
  `Category` varchar(20) DEFAULT NULL,
  `Name` varchar(45) NOT NULL,
  `UnitOfMeasure` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`GoodsID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
