CREATE TABLE USERS (ID serial PRIMARY KEY,
                    NAME VARCHAR(32) NOT NULL,
                    PASSPHRASE CHARACTER(64),
                    SALT CHARACTER(16),
                    IPADDRESS VARCHAR(15));