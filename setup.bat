@echo off
setlocal

:: Create virtual environment
if not exist ".venv\" (
    echo Creating virtual environment...
    py -m venv .venv
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

:: Generate MD5 hash of requirements.txt
set "REQ_HASH="
for /f "skip=1 tokens=*" %%a in ('certutil -hashfile requirements.txt MD5') do (
    if not defined REQ_HASH set "REQ_HASH=%%a"
)

:: Read previous hash if it exists
set "OLD_HASH="
if exist ".venv\req.hash" (
    set /p OLD_HASH=<".venv\req.hash"
)

:: Compare hashes and install if they differ
if "%REQ_HASH%" == "%OLD_HASH%" (
    echo Requirements unchanged. Skipping pip install
) else (
    echo Requirements changed. Installing...
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo %REQ_HASH%>".venv\req.hash"
    )
)

:: Delete and recreate the database
echo Recreating database...
if exist "flashcards.db" (
    del "flashcards.db"
)
sqlite3 flashcards.db < schema.sql
sqlite3 flashcards.db ".tables"

echo Done! Virtual environment is ready.
pause
