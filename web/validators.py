from wtforms import ValidationError


def ticker_check(form, field):
    """
    Проверяет, что значение в поле тикера состоит только из заглавных букв.
    :return: ValidationError: Если поле не содержит только заглавные буквы.
    """
    if not field.data.isupper():
        raise ValidationError('Поле должно иметь только заглавные буквы')


def isalpha_check(form, field):
    """
    Проверяет, что значение в поле состоит только из букв (не содержит цифр).
    :return: ValidationError: Если поле содержит цифры.
    """
    if field.data.isdigit():
        raise ValidationError('Поле не может содержать цифр')
