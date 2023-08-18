from wtforms import ValidationError


def ticker_check(form, field):
    if not field.data.isupper():
        raise ValidationError('Поле должно иметь только заглавные буквы')


def isalpha_check(form, field):
    if field.data.isdigit():
        raise ValidationError('Поле не может содержать цифр')

def isdigit_check(form, field):
    if field.data is None or not isinstance(field.data, float):
        raise ValidationError('Поле не может содержать букв')
