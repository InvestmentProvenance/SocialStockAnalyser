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


CREATE TABLE `stock_data` (
  `timestamp` datetime DEFAULT NULL,
  `open` float DEFAULT NULL,
  `high` float DEFAULT NULL,
  `low` float DEFAULT NULL,
  `close` float DEFAULT NULL,
  `volume` bigint DEFAULT NULL,
  `symbol` varchar(10) DEFAULT NULL
)

CREATE TABLE StockInterval (
  StockIntervalID   INT AUTO_INCREMENT NOT NULL,
  Interval          DATETIME NOT NULL,
  `Open`              FLOAT NOT NULL,
  High              FLOAT NOT NULL,
  Low               FLOAT NOT NULL,
  `Close`             FLOAT NOT NULL,
  Volume            INT NOT NULL,
  Symbol            varchar(10) NOT NULL,
  PRIMARY KEY(StockIntervalID)
)

-- TODO: remove your_database_name bit?
CREATE TABLE Platform (
	PlatformID      INT AUTO_INCREMENT NOT NULL,
	PlatformName    varchar(20) NOT NULL,
	PRIMARY KEY (PlatformID)
);

CREATE TABLE User (
	UserID      INT AUTO_INCREMENT NOT NULL,
	PlatformID  INT NOT NULL,
    Username    VARCHAR(40), -- TODO: Needs length adjustment
	PRIMARY KEY (PlatformID),
    FOREIGN KEY (ForeignID) REFERENCES your_database_name.Platform(PlatformID)
);

CREATE TABLE Api (
	ApiID       INT AUTO_INCREMENT NOT NULL,
    ApiName     VARCHAR(20), -- TODO: Needs length adjustment
	ApiInfo     --TODO: What datatype is this?
	ApiKey      VARCHAR(50) NOT NULL,
	PRIMARY KEY (ApiID)
);

CREATE TABLE Request (
	RequestID       INT AUTO_INCREMENT NOT NULL,
    ApiID           INT NOT NULL,
	`Timestamp`    DATETIME NOT NULL,
	PRIMARY KEY (RequestID),
    FOREIGN KEY (ApiID) REFERENCES your_database_name.Api(ApiID)
);

CREATE TABLE Comment (
	CommentID       INT AUTO_INCREMENT NOT NULL,
	UserID          INT NOT NULL,
    `Text`          TEXT NOT NULL,
	`Timestamp`     DATETIME NOT NULL,
    RequestID       INT NOT NULL,
	PRIMARY KEY (RequestID),
    FOREIGN KEY (UserID) REFERENCES your_database_name.User(UserID),
    FOREIGN KEY (RequestID) REFERENCES your_database_name.Request(RequestID)
);

CREATE TABLE Stock (
	StockID         INT AUTO_INCREMENT NOT NULL,
	Ticker          VARCHAR(16) NOT NULL,
	`Name`          VARCHAR(64) NOT NULL,
    Exchange        VARCHAR(64) NOT NULL,
	PRIMARY KEY (StockID)
);

CREATE TABLE RangeCheck (
    TimeFrame ID INT AUTO_INCREMENT NOT NULL,
    StockID     INT NOT NULL,
    StartTime       DATETIME NOT NULL,
    EndTime DATETIME NOT NULL,
    RequestID INT NOT NULL,
    FOREIGN KEY (StockID) REFERENCES your_database_name.Stock(StockID)
    FOREIGN KEY (RequestID) REFERENCES your_database_name.Request(RequestID)

);

