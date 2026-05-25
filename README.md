# API de Carros — FastAPI + SQLModel

CRUD completo para **Marcas**, **Modelos** e **Carros** usando FastAPI e SQLModel com banco SQLite.

## Decisões Técnicas

* Foi escolhido o [FastApi](https://fastapi.tiangolo.com/) por ser mais "clean" sem muitas configurações diferente do [Django](https://www.djangoproject.com/) e também porque de forma transparente já cria documentação [Swagger](https://swagger.io) / OpenAPI.
> [!NOTE]
> Preferi 
```bash
pip install fastapi
```
em vez de 
```bash
pip install fastapi[standard]
```
para evitar adicionar muitas dependências que não vão ser usadas nesse projeto.

* No gerenciador de pacotes / depêndencias se esta usando o [pip](https://pip.pypa.io/en/stable/). Inicialmente foi escolhido o [Poetry](https://python-poetry.org/) por gerenciar de forma transparente as virtual environments e tendo um arquivo de dependências no estilo do [Maven](https://maven.apache.org/) e [Gradle](https://gradle.org/) do [Java](https://www.java.com/). Mas após algum tempo de uso começou dar alguns erros e se voltou para o tradicional [pip](https://pip.pypa.io/en/stable/). Se pensou também no [vu](https://docs.astral.sh/uv/) mas por ser mais recente não acabou sendo usado.

* De ORM escolhi o [SQLModel](https://sqlmodel.tiangolo.com/) do mesmo criador do [FastApi](https://fastapi.tiangolo.com/) que utiliza as tecnologias [Pydantic](https://pydantic.dev/) e [SQLAlchemy](https://www.sqlalchemy.org/) o que diminui a duplicação de código na criação dos models / dtos. 

* Todos os updates usam PUT com exclude_unset=True, permitindo atualizar apenas os campos enviados. Preferi PUT em vez de PATCH.

* Carros.descricao é o único campo opcional, mudei no main.py em default_response_class para não enviar atributos null em qualquer endpoint.

* Para facilitar os endpoints deixei o arquivo Insomnia_v5.yaml para ser importado e fazer os testes dos endpoints.

* WIP: Autenticação e Autorização: login ok mas quando colocado o Bearer Token nas requisições retorna Invalid or expired token.

## GitHub https://github.com/fabiosilvaacs/cars_fastapi

## Publicação https://cars-fastapi.onrender.com/

## Documentação
Acesse a documentação interativa em: **http://localhost:8000/docs** ou **https://cars-fastapi.onrender.com/docs**

## Instalação
```bash
pip install -r requirements.txt
```

## Execução
```bash
uvicorn main:app --reload
```

## Testes
```bash
python -m pytest tests/ -v
```