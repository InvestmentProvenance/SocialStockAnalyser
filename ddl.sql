CREATE TABLE `stock_data` (
  `timestamp` datetime DEFAULT NULL,
  `open` float DEFAULT NULL,
  `high` float DEFAULT NULL,
  `low` float DEFAULT NULL,
  `close` float DEFAULT NULL,
  `volume` bigint DEFAULT NULL,
  `symbol` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE your_database_name.Platform (
	PlatformID      INTEGER auto_increment NOT NULL,
	PlatformName    varchar(20) NOT NULL,
	CONSTRAINT Platform_PK PRIMARY KEY (PlatformID)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci
AUTO_INCREMENT=1;