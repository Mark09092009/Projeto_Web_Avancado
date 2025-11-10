from django.apps import AppConfig

class CoreConfig(AppConfig):
    """
    CoreConfig é a classe de configuração do aplicativo Django para o módulo 'apps.core'.

    Atributos:
        default_auto_field (str): Define o tipo padrão de campo auto-incremental para
            modelos neste aplicativo como 'django.db.models.BigAutoField', que é
            recomendado para chaves primárias em novos projetos.
        name (str): Especifica o caminho Python completo do aplicativo como 'apps.core',
            permitindo que o Django identifique e registre este aplicativo corretamente.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    # Define o nome do aplicativo Django como 'apps.core'
    name = 'apps.core'
