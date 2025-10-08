# {{ cookiecutter.project_name }} - Agents Summary

{%- for key, agent in cookiecutter.agents.items() %}
* [{{ agent['name'] }}](Agent-{{agent.name}}.md)
{%- endfor %}