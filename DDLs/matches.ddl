CREATE TABLE `Matches` (
  `RequestID` int(11) NOT NULL,
  `OfferID` int(11) NOT NULL,
  `Status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`RequestID`,`OfferID`),
  KEY `fk_MatchedOfferID_idx` (`OfferID`),
  KEY `fk_MatchedRequestID` (`RequestID`),
  CONSTRAINT `fk_MatchedOfferID` FOREIGN KEY (`OfferID`) REFERENCES `offers` (`offerid`),
  CONSTRAINT `fk_MatchedRequestID` FOREIGN KEY (`RequestID`) REFERENCES `requests` (`requestid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
