from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    try:
        if len(arg.split(':')) != 2:
            return value 
        
        old, new = arg.split(':')
        return str(value).replace(old, new)
    except Exception:
        return value


@register.filter
def is_employee(user):
    """Retorna True se o usuário for superuser ou possuir um registro Funcionario relacionado."""
    try:
        if user is None:
            return False
        if getattr(user, 'is_superuser', False):
            return True
        # Verifica relação one-to-one com Funcionario de forma segura
        return hasattr(user, 'funcionario')
    except Exception:
        return False