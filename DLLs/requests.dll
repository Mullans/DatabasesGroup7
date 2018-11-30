CREATE TABLE `Requests` (
  `RequestID` int(11) NOT NULL AUTO_INCREMENT,
  `UserID` varchar(20) NOT NULL,
  `DisasterID` int(11) NOT NULL,
  `GoodsID` int(11) NOT NULL,
  `DatePosted` datetime NOT NULL,
  `Duration` int(11) DEFAULT NULL,
  `QuantityNeeded` int(11) NOT NULL,
  `QuantityReceived` int(11) DEFAULT NULL,
  PRIMARY KEY (`RequestID`),
  KEY `fk_DisasterID_idx` (`DisasterID`),
  KEY `fk_GoodsID_idx` (`GoodsID`),
  KEY `fk_UserID_idx` (`UserID`),
  CONSTRAINT `fk_DisasterID` FOREIGN KEY (`DisasterID`) REFERENCES `disasters` (`disasterid`),
  CONSTRAINT `fk_GoodsID` FOREIGN KEY (`GoodsID`) REFERENCES `possiblegoods` (`goodsid`),
  CONSTRAINT `fk_UserID` FOREIGN KEY (`UserID`) REFERENCES `users` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
