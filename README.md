# Messenger App

# Browser Tested
Chrome & FireFox

# Python Version
Python 3.7

### Steps to Start Server
1. Setup Virtual Environment (OPTIONAL)
    a.  virtualenv --python python3 env (MAC)
        - source env/bin/activate  (MAC)
    b.  py -m venv env (WINDOWS)
        - env\Scripts\activate (WINDOWS)
_______
2. Install Dependencies
    a. py -m pip install -r requirements.txt (WINDOWS/MAC)
_______
3. Set Environment variables (OPTIONAL = python3 chat.py || py chat.py)
    a. set FLASK_APP=messenger.py (WINDOWS)
    b. export set FLASK_APP=messenger.py (MAC)
_______
4. Use "flask init-db" create/delete table data (WINDOWS/MAC)
_______
5. Use "flask run" to run the server (WINDOWS/MAC)
    - Running on http://127.0.0.1:5000/

### Test Code
python tests.py