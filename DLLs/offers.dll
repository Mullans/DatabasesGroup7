CREATE TABLE `Offers` (
  `OfferID` int(11) NOT NULL AUTO_INCREMENT,
  `UserID` varchar(20) NOT NULL,
  `GoodsID` int(11) NOT NULL,
  `QuantityOffered` int(11) NOT NULL,
  `QuantityClaimed` int(11) DEFAULT NULL,
  `DatePosted` datetime NOT NULL,
  `Duration` int(11) DEFAULT NULL,
  `DisasterID` int(11) NOT NULL,
  PRIMARY KEY (`OfferID`),
  KEY `fk_GoodsID_idx` (`GoodsID`),
  KEY `fk_UsersID_idx` (`UserID`),
  KEY `fk_OfferDisastersID_idx` (`DisasterID`),
  CONSTRAINT `fk_OfferDisastersID` FOREIGN KEY (`DisasterID`) REFERENCES `disasters` (`disasterid`),
  CONSTRAINT `fk_OfferGoodsID` FOREIGN KEY (`GoodsID`) REFERENCES `possiblegoods` (`goodsid`),
  CONSTRAINT `fk_OfferUsersID` FOREIGN KEY (`UserID`) REFERENCES `users` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
