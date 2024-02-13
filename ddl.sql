-- TODO: remove your_database_name bit?
CREATE TABLE your_database_name.Platform (
	PlatformID      INT AUTO_INCREMENT NOT NULL,
	PlatformName    varchar(20) NOT NULL,
	PRIMARY KEY (PlatformID)
);

CREATE TABLE your_database_name.User (
	UserID      INT AUTO_INCREMENT NOT NULL,
	PlatformID  INT NOT NULL,
    Username    VARCHAR(40), -- TODO: Needs length adjustment
	PRIMARY KEY (PlatformID),
    FOREIGN KEY (ForeignID) REFERENCES your_database_name.Platform(PlatformID)
);

CREATE TABLE your_database_name.Api (
	ApiID       INT AUTO_INCREMENT NOT NULL,
    ApiName     VARCHAR(20), -- TODO: Needs length adjustment
	ApiInfo     --TODO: What datatype is this?
	ApiKey      VARCHAR(50) NOT NULL,
	PRIMARY KEY (ApiID)
);

CREATE TABLE your_database_name.Request (
	RequestID       INT AUTO_INCREMENT NOT NULL,
    ApiID           INT NOT NULL,
	`Timestamp`     DATETIME NOT NULL,
	PRIMARY KEY (RequestID),
    FOREIGN KEY (ApiID) REFERENCES your_database_name.Api(ApiID)
);

CREATE TABLE your_database_name.Comment (
	CommentID       INT AUTO_INCREMENT NOT NULL,
	UserID          INT NOT NULL,
    `Text`          TEXT NOT NULL,
	`Timestamp`     DATETIME NOT NULL,
    RequestID       INT NOT NULL,
	PRIMARY KEY (RequestID),
    FOREIGN KEY (UserID) REFERENCES your_database_name.User(UserID),
    FOREIGN KEY (RequestID) REFERENCES your_database_name.Request(RequestID)
);

CREATE TABLE your_database_name.Stock (
	StockID         INT AUTO_INCREMENT NOT NULL,
	Ticker          VARCHAR(16) NOT NULL,
	`Name`          VARCHAR(64) NOT NULL,
    Exchange        VARCHAR(64) NOT NULL,
	PRIMARY KEY (StockID)
);

CREATE TABLE your_database_name.RangeCheck (
    TimeFrameID     INT AUTO_INCREMENT NOT NULL,
    StockID         INT NOT NULL,
    StartTime       DATETIME NOT NULL,
    EndTime         DATETIME NOT NULL,
    RequestID       INT NOT NULL,
    PRIMARY KEY (TimeFrameID),
    FOREIGN KEY (StockID) REFERENCES your_database_name.Stock(StockID),
    FOREIGN KEY (RequestID) REFERENCES your_database_name.Request(RequestID)
);

CREATE TABLE your_database_name.TickerMention (
    StockID         INT NOT NULL,
    CommentID       INT NOT NULL,
    PRIMARY KEY (StockID, CommentID)
    FOREIGN KEY (StockID) REFERENCES Stock(StockID)
    FOREIGN KEY (CommentID) REFERENCES Comment(CommentID)
);

CREATE TABLE your_database_name.Sentiment (
SentimentID         INT AUTO_INCREMENT NOT NULL,
    CommentID       INT NOT NULL,
    StockID         INT NOT NULL,
    Sentiment       FLOAT NOT NULL,
    PRIMARY KEY (SentimentID)
    FOREIGN KEY (StockID) REFERENCES Stock(StockID)
    FOREIGN KEY (CommentID) REFERENCES Comment(CommentID)  
);
