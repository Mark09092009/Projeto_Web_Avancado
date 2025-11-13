from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """
    Substitui todas as ocorrências de um substring por outro.
    
    O argumento deve usar ':' (dois pontos) como separador entre o valor
    antigo e o novo.
    Uso: {{ value|replace:"old:new" }}
    """
    try:
        # Usamos ':' como delimitador para permitir que vírgulas sejam substituídas.
        if len(arg.split(':')) != 2:
            # Retorna o valor original se o formato for inválido ou o delimitador estiver faltando.
            return value 
        
        old, new = arg.split(':')
        # Garante que estamos trabalhando com uma string.
        return str(value).replace(old, new)
    except Exception:
        return value