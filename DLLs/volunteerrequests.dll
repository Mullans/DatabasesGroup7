CREATE TABLE `VolunteerRequests` (
  `RequestID` int(11) NOT NULL,
  `UserID` varchar(20) NOT NULL,
  `PeopleNeeded` int(11) NOT NULL,
  `PeopleFound` int(11) DEFAULT NULL,
  `WorkCategory` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`RequestID`),
  KEY `fk_Users_idx` (`UserID`),
  CONSTRAINT `fk_Users` FOREIGN KEY (`UserID`) REFERENCES `users` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
