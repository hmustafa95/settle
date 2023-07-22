from django.core import validators


def only_letters(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise validators.ValidationError('Only letters and spaces are allowed')


def only_digits(value):
    if not value.isdigit():
        raise validators.ValidationError('Only digits are allowed')
