# Prerequisits
Install uv to work with this project. 
See https://docs.astral.sh/uv/getting-started/installation/ for how to install

# Virtual Environment
```bash
uv venv
```
Afterwards activate your virtual envrionment by 
```bash
source .venv/bin/activate
```

# Dependencies
Sync your environment to get all dependencies needed.
```bash
uv sync --all-groups
```

# Run
Set the environment variable
```bash
export PYTHONPATH=$PWD
```
Run the app locally by run the app/main.py

```bash
uv run python app/main.py
```

This will run by default a host at http://0.0.0.0:9000

# Debug

## Start attachable debugging session
Run debugpy at port 5678 and wait until debugger will be attached
```bash
uv run python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app/main.py
```

## Attach Debugger with VSCode
At ".vscode/launch.json" there is a debugger configured. Just hit play at "Debug {{cookiecutter.project_name}}"

# API
Foundation of {{cookiecutter.project_name}}'s' service layer is [FastAPI](https://fastapi.tiangolo.com/) in other projects. You can review the API Documentation at http://0.0.0.0:9000/docs or http://0.0.0.0:9000/redoc