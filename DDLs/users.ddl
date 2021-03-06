CREATE TABLE `Users` (
  `username` VARCHAR(30) NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `password_` VARCHAR(255) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `address` VARCHAR(225) NOT NULL,
  `phone` VARCHAR(20) NOT NULL,
  `registerdate` DATETIME NOT NULL DEFAULT current_timestamp(),
  `isVolunteer` INT NOT NULL DEFAULT 0,
  `isAdmin` INT NOT NULL DEFAULT 0,
  `latitude` DECIMAL(7,4) NOT NULL,
  `longitude` DECIMAL(7,4) NOT NULL,
  `status` INT NOT NULL DEFAULT 0,
  `userRating` DECIMAL(6,3) NOT NULL DEFAULT 0,
  PRIMARY KEY (`username`)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
