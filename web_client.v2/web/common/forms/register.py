# -*- coding: utf-8 -*-
from django import forms
from bootstrap3_datetime.widgets import DateTimePicker

class FormMessages(object):
    error_messages = {
        'required': 'Поле является обязательным',
        'invalid': 'Введены неверные для этого поля данные',
    }

class RegisterPersonForm(forms.Form):
    msg = FormMessages.error_messages

    gender_choices = (
            ('Male', 'Мужской'),
            ('Female', 'Женский'),
    )
    date_widget = DateTimePicker(options={"format": "dd.MM.yyyy", "pickTime": False}, attrs={'placeholder': '01.01.1990'})

    first_name = forms.CharField(error_messages=msg, label='Имя', max_length=20, required=True)
    surname = forms.CharField(error_messages=msg, label='Фамилия', max_length=30, required=True)
    second_name = forms.CharField(error_messages=msg, label='Отчество', max_length=20, required=False)
    gender = forms.ChoiceField(label='Пол', choices=gender_choices, required=False)
    email = forms.EmailField(error_messages=msg, widget=forms.TextInput(attrs={'placeholder':'example@mail.ru'}),
                             required=True)
    date_of_birth = forms.DateField(input_formats=('%d.%m.%Y',), error_messages=msg, label='Дата рождения', widget=date_widget, required=False)
    description = forms.CharField(error_messages=msg, label='Дополнительные сведения', widget=forms.Textarea, max_length=1024, required=False)
    address = forms.CharField(error_messages=msg, widget=forms.TextInput(attrs={'placeholder': 'г. Москва, ул. Тверская, д.1, кв.1'}),
                              label='Адрес', max_length=1024, required=False)
    phone = forms.CharField(error_messages=msg, widget=forms.TextInput(attrs={'placeholder': '+79267775533'}),
                            label='Телефон', max_length=20, required=False)

class RegisterAccountForm(forms.Form):
    msg = FormMessages.error_messages

    login = forms.EmailField(label='Логин', error_messages=msg, max_length=45, required=True)
    password = forms.CharField(error_messages=msg, widget=forms.PasswordInput, label='Пароль', max_length=128, required=True)

    def __init__(self, persons, *args, **kwargs):
        super(RegisterAccountForm, self).__init__(*args, **kwargs)
        person_choices = ((1, 'Денис Исаев'), (2, 'Алибаба Дед'))
        self.fields['person'] = forms.ChoiceField(choices=person_choices, label='Пользователь', required=True)
