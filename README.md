# Desafio: API_Bancária Assíncrona com FastAPI

Nesse desafio foi implementado uma API RESTful assíncrona usando FastAPI para gerenciar operações bancárias de depósitos e saques, vinculadas a contas correntes. Nele foi utilizado autenticação JWT e práticas recomendadas de design de APIs.

O desafio teve como objetivo atender as seguintes funcionalidades e os seguintes requisitos técnicos:

## Funcionalidades
- **Cadastro de Transações**: Permite o cadastro de transações bancárias, como depósitos e saques;
- **Exibição de Extrato**: Endpoint para exibir o extrato de uma conta e mostrar todas as transações realizadas;
- **Autenticação com JWT**: Utiliza JWT(JSON Web Tokens) para garantir que apenas usuários autenticados possam acessar os endpoints que exigem autenticação.


## Requisitos Técnicos
- **FastAPI**: Utiliza FastAPI como framework e recursos assíncronos para lidar com operações I/O de forma eficiente;
- **Modelagem de Dados**: Modelo de dados para representar contas correntes e transações;
- **Validação das operações**: Não permite depósitos e saques com valores negativos e valida se o usuário possui saldo para realizar o saque;
- **Segurança**: Autenticação com JWT para proteger os endpoints que necessitam de acesso autenticado;
- **Documentação com OpenAPI**: API documentada com descrições para cada endpoint, parâmetros e modelos de dados.

## Funcionalidades a serem implementadas
- Deploy;
- Novos endpoints.
