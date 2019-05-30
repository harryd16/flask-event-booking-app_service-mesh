# golfsoftware

Any of the code bases listed in requirements.txt are not our work and follow their respective license agreements.

## Deployment
1. Update secret key using `python -c 'import os; print(os.urandom(16))'`
2. Install python (version in runtime.txt), install pip, and the requirements using pip install -r requirements.txt
3. Run server >>> python web gunicorn app:app
