from app.gen.domainmodel.toolregistry import BaseToolregistry
{% for key, tool in cookiecutter.tools.items() %}
from app.gen.tool.{{tool.uid | aiurnimport }}.tool import {{tool.uid | aiurnvar}}
{% endfor %}


baseToolregistry = BaseToolregistry(registry={
    {% for key, tool in cookiecutter.tools.items() %}
    "{{tool.uid }}": {{tool.uid | aiurnvar }},
    {% endfor %}
})
