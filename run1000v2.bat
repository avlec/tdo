@ECHO off

ECHO Run server
start python "C:\...\server.py"

ECHO Run client
REM start,step,end
REM change 20 to 1000 when testing with many clients
FOR /L %%i IN (1, 1, 2) DO (
	start python "C:\...\client.py"
)
