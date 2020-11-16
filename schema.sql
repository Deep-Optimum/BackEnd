DROP TABLE IF EXISTS Addresses;
DROP TABLE IF EXISTS Order_info;
DROP TABLE IF EXISTS Listings;
DROP TABLE IF EXISTS User_info;

CREATE TABLE `User_info` (
  `uni` varchar(8) NOT NULL,
  `user_name` varchar(25) NOT NULL,
  `email` varchar(45) NOT NULL,
  `phone_number` varchar(10) NOT NULL,
  `credential` varchar(45) NOT NULL,
  PRIMARY KEY (`uni`),
  UNIQUE KEY `userName_UNIQUE` (`user_name`),
  UNIQUE KEY `uni_UNIQUE` (`uni`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Addresses` (
  `address_id` int NOT NULL,
  `uni` varchar(8) NOT NULL,
  `country` varchar(20) NOT NULL,
  `state` varchar(2) NOT NULL,
  `city` varchar(20) NOT NULL,
  `address` varchar(40) NOT NULL,
  `zipcode` varchar(5) NOT NULL,
  PRIMARY KEY (`address_id`),
  UNIQUE KEY `address_ID_UNIQUE` (`address_id`),
  KEY `address_uni_idx` (`uni`),
  CONSTRAINT `address_uni` FOREIGN KEY (`uni`) REFERENCES `User_info` (`uni`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Listings` (
  `listing_id` varchar(10) NOT NULL,
  `isbn` varchar(15) NOT NULL,
  `uni` varchar(8) NOT NULL,
  `title` varchar(45) NOT NULL,
  `price` decimal(5,2) NOT NULL,
  `category` varchar(45) NOT NULL,
  `description` mediumtext NOT NULL,
  `image_url` varchar(256) NOT NULL,
  `is_sold` tinyint(1) NOT NULL,
  PRIMARY KEY (`listing_id`,`isbn`),
  UNIQUE KEY `post_ID_UNIQUE` (`listing_id`),
  UNIQUE KEY `uni_UNIQUE` (`uni`),
  UNIQUE KEY `ISBN_UNIQUE` (`isbn`),
  CONSTRAINT `listing_uni` FOREIGN KEY (`uni`) REFERENCES `User_info` (`uni`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Order_info` (
  `order_id` varchar(10) NOT NULL,
  `buyer_uni` varchar(8) NOT NULL,
  `seller_uni` varchar(8) NOT NULL,
  `listing_id` varchar(10) NOT NULL,
  `transaction_amt` decimal(5,2) NOT NULL,
  `status` enum('Completed','In progress','Canceled') NOT NULL,
  PRIMARY KEY (`order_id`),
  UNIQUE KEY `order_ID_UNIQUE` (`order_id`),
  UNIQUE KEY `seller_uni_UNIQUE` (`seller_uni`),
  UNIQUE KEY `buyer_uni_UNIQUE` (`buyer_uni`),
  KEY `listing_id_idx` (`listing_id`),
  CONSTRAINT `buyer_uni` FOREIGN KEY (`buyer_uni`) REFERENCES `User_info` (`uni`),
  CONSTRAINT `listing_id` FOREIGN KEY (`listing_id`) REFERENCES `Listings` (`listing_id`),
  CONSTRAINT `seller_uni` FOREIGN KEY (`seller_uni`) REFERENCES `User_info` (`uni`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;