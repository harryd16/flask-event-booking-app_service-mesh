# golfsoftware

Any of the code bases listed in requirements.txt are not our work and follow their respective license agreements.

## Deployment
1. Update secret key using `python -c 'import os; print(os.urandom(16))'`
2. Start webserver `waitress-serve --call 'flaskr:create_app'`
