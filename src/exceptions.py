# define uma exceção personalizada para erro de conta não encontrada
class AccountNotFoundError(Exception):
    pass  # usada para indicar que uma conta específica não foi encontrada

# define uma exceção personalizada para erros de negócio
class BusinessError(Exception):
    pass  # usada para representar erros genéricos de lógica de negócios
