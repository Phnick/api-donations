# Sistema de Doação - API

API para gerenciar o sistema de doações, incluindo funcionalidades para **registro de usuários**, **doações de itens**, **autenticação com JWT**, e **envio de e-mails de confirmação**.

## Tecnologias Usadas

- **FastAPI** - Framework para criar a API de forma rápida e eficiente.
- **SQLAlchemy** - ORM para interação com o banco de dados SQL.
- **Alembic** - Ferramenta para migração de banco de dados.
- **JWT** - Autenticação baseada em JSON Web Tokens.
- **Pydantic** - Validação de dados.
- **SMTP / Email** - Envio de e-mails de confirmação de registro e interesse na doação.

## Funcionalidades

- **Autenticação de Usuário**: Registro e login de usuários com JWT para autenticação.
- **Cadastro de Doações**: Usuários podem registrar itens que desejam doar.
- **Confirmação por E-mail**: Envio de e-mails para confirmação de registro e interesse nas doações.
- **Validação de Dados**: Validação de dados de entrada com Pydantic.
- **Gestão de Doações**: Consultar, editar e excluir itens cadastrados para doação.
