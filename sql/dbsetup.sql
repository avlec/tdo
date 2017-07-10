DROP TABLE users;

CREATE TABLE USERS (ID INTEGER PRIMARY KEY NOT NULL,
                    NAME VARCHAR(32) NOT NULL,
                    SALT CHARACTER(16),
                    PASSPHRASE VARCHAR(32),
                    IPADDRESS VARCHAR(15));
