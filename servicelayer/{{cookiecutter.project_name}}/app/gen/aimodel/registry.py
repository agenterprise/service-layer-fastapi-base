from app.gen.domainmodel.modelregistry import BaseModelregistry
{% for key, llm in cookiecutter.llms.items() %}
from app.gen.aimodel.{{llm.uid | aiurnimport }}.model import {{llm.uid | aiurnvar}}
{% endfor %}


baseAimodelregistry = BaseModelregistry(registry={
    {% for key, llm in cookiecutter.llms.items() %}
    "{{llm.uid }}": {{llm.uid | aiurnvar }},
    {% endfor %}
})
