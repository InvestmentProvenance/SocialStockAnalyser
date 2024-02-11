CREATE TABLE `stock_data` (
  `timestamp` datetime DEFAULT NULL,
  `open` float DEFAULT NULL,
  `high` float DEFAULT NULL,
  `low` float DEFAULT NULL,
  `close` float DEFAULT NULL,
  `volume` bigint DEFAULT NULL,
  `symbol` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE sns_data_sentiment (
  id INT AUTO_INCREMENT PRIMARY KEY,
  timestamp DATETIME,
  user_id VARCHAR(255),
  post_text TEXT,
  sentiment VARCHAR(20),
  positive_score FLOAT,
  negative_score FLOAT,
  neutral_score FLOAT,
  mixed_score FLOAT
); 


-- TODO: remove your_database_name bit?
CREATE TABLE your_database_name.Platform (
	PlatformID      INT AUTO_INCREMENT NOT NULL,
	PlatformName    varchar(20) NOT NULL,
	CONSTRAINT      PlatformID PRIMARY KEY (PlatformID)
);

CREATE TABLE your_database_name.User (
	UserID      INT AUTO_INCREMENT NOT NULL,
	PlatformID  INT NOT NULL,
    Username    VARCHAR(40), -- TODO: Needs length adjustment
	PRIMARY KEY (PlatformID),
    FOREIGN KEY (ForeignID) REFERENCES your_database_name.Platform(PlatformID)
)

CREATE TABLE your_database_name.Api (
	ApiID       INT AUTO_INCREMENT NOT NULL,
    ApiName     VARCHAR(20), -- TODO: Needs length adjustment
	ApiInfo     --TODO: What datatype is this?
	ApiKey      VARCHAR(50) NOT NULL,
	PRIMARY KEY (ApiID)
)

CREATE TABLE your_database_name.Request (
	RequestID       INT AUTO_INCREMENT NOT NULL,
    ApiID           INT NOT NULL, -- TODO: Needs changing?
	ReqTimestamp    VARCHAR(50) NOT NULL, -- TODO: I think timestamp is a keyword? 
	PRIMARY KEY (RequestID),
    FOREIGN KEY (ApiID) REFERENCES your_database_name.Api(ApiID)
)