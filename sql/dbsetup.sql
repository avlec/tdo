CREATE TABLE users (ID CHARACTER(16) PRIMARY KEY,
                    ALIAS VARCHAR(16) NOT NULL,
                    PASS CHARACTER(64));

CREATE TABLE channels (ID CHARACTER(16) PRIMARY KEY,
                      NAME CHARACTER(16),
                      PERMISSIONS CHARACTER(3),
                      BLOCKED_MEMBERS CHARACTER(16) ARRAY[1024]);

CREATE TABLE messages (ID CHARACTER(16) PRIMARY KEY,
                       SENDERID CHARACTER(16),
                       CHANNELID CHARACTER(16),
                       MESSAGE VARCHAR(256),
                       TIME TIMESTAMP);

CREATE ROLE api WITH UNENCRYPTED PASSWORD 'password';
ALTER ROLE api WITH LOGIN;
GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA public TO api;
GRANT CREATE, CONNECT ON DATABASE tdo TO api;

INSERT INTO tdo.public.channels (id, name, permissions) VALUES ('0000000000000000', 'General', '011');