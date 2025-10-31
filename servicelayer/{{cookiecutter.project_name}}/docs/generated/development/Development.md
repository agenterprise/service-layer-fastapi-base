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


# How to extend project "{{cookiecutter.project_name}}"
Agenterprise princple is **"Give your AI project anchors and wings"**. Means: The anchor is generated and the wings is extended by you. Read on how to proceed.

## Your Code vs. Agenterprise Code
Agenterprise generates a lot of code for you. This code should not be edited or extended. The following files and folders are subject to change:
* <i>app/gen/**</i>
* <i>docs/generated/**</i>
* <i>deployment/Dockerfile.build</i>
* <i>deployment/Dockerfile.run</i>


## ⚓ Extend with your DSL (The anchors )
The origin DSL is copied and placed below folder ./dsl/{{cookiecutter.dsl_file}}. It's possible to edit the file all the time (pls. consult https://www.agenterprise.ai)

If you want to regenerate you project, feel happy 😃 -->  <i>agenterprise</i> is already in your path. 

1. Upgrade to the latest version of agenterprise by calling:
    ```bash
    uv pip install -U agenterprise --group projectlayer 
    ```
2. In the project root execute this command.
    ```bash
    agenterprise --dsl dsl/{{cookiecutter.dsl_file}}  --code-generation --target ./
    ```

## 🪽 Extend with custom code (The wings )
At folder <i>app/ext</i> you can freely implement anything that should be on top of the anchors.
The folder structure aligns to the one below <i>app/gen</i>. You can either:
* Extend the classes from <i>app/gen</i>.
* Implements own structures
NOTE: <i>app/gen</i> is your place and will not be deleted on regeneration

To tie everything together you should understand the configuration at app/gen/config/base.py. This is the place where the application will be assembled in a [IoC](https://en.wikipedia.org/wiki/Inversion_of_control) principles. 

You can assemble your own code below <i>app/ext/config</i>
* dev.py (see <i>app/ext/config/.dev.py</i>)   --> in .env file set <i>run_environment=dev</i>
* uat.py (see <i>app/ext/config/.uat.py</i>)   --> in .env file set <i>run_environment=uat</i>
* int.py (see <i>app/ext/config/.int.py</i>)   --> in .env file set <i>run_environment=int</i>
* test.py (see <i>app/ext/config/.test.py</i>) --> in .env file set <i>run_environment=systemtest or loadtest</i>
* prod.py (see <i>app/ext/config/.prod.py</i>) --> in .env file set <i>run_environment=prod or ref</i>