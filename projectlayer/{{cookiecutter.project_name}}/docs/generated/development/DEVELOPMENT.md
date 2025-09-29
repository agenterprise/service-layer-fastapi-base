# Prerequisits
Install uv to work with this project. 
See https://docs.astral.sh/uv/getting-started/installation/ for how to install

# Virtual Environment
```bash
uv init
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
Run the app locally by run the app/main.py

```bash
uv run python app/main.py
```

# Debug

## Start attachable debugging session
Run debugpy at port 5678 and wait until debugger will be attached
```bash
uv run python -m debugpy --listen 0.0.0.0:5678 --wait-for-client app/main.py
```

## Attach Debugger with VSCode
At ".vscode/launch.json" there is a debugger configured. Just hit play at "Debug {{cookiecutter.project_name}}"