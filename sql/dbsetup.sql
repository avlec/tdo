CREATE TABLE USERS (SALT CHARACTER(16) PRIMARY KEY, ALIAS VARCHAR(16) NOT NULL, PASS CHARACTER(64));
CREATE ROLE api WITH UNENCRYPTED PASSWORD 'password';
ALTER ROLE api WITH LOGIN;
GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA public TO api;
GRANT CREATE, CONNECT ON DATABASE tdo TO api;