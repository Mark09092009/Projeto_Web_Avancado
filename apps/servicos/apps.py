from django.apps import AppConfig
# Importa a classe base AppConfig do módulo django.apps, que é usada para configurar aplicativos no Django.

class ServicosConfig(AppConfig):
    # Define uma classe de configuração para o aplicativo "servicos", herdando de AppConfig.

    default_auto_field = 'django.db.models.BigAutoField'
    # Especifica o tipo de campo padrão para chaves primárias automáticas no banco de dados.
    # 'BigAutoField' é usado para gerar IDs automáticos como inteiros grandes.

    name = 'apps.servicos'
    # Define o nome do aplicativo como 'apps.servicos', que corresponde ao caminho do módulo Python do aplicativo.
