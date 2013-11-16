# -*- coding: utf-8 -*-
from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from common import WebForm

class RegisterPersonForm(WebForm):
    form_name = "Регистрация нового пользователя"
    submit_name = "Зарегистрировать пользователя"
    gender_choices = (
            ('Male', 'Мужской'),
            ('Female', 'Женский'),
    )
    date_widget = DateTimePicker(options={"format": "dd.MM.yyyy", "pickTime": False}, attrs={'placeholder': '01.01.1990'})

    surname = forms.CharField(label='Фамилия', max_length=30, required=True)
    first_name = forms.CharField(label='Имя', max_length=20, required=True)
    second_name = forms.CharField(label='Отчество', max_length=20, required=False)
    gender = forms.TypedChoiceField(label='Пол', choices=gender_choices, required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'example@mail.ru'}),
                             required=True)
    date_of_birth = forms.DateField(input_formats=('%d.%m.%Y',), label='Дата рождения', widget=date_widget, required=False)
    description = forms.CharField(label='Дополнительные сведения', widget=forms.Textarea, max_length=1024, required=False)
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'г. Москва, ул. Тверская, д.1, кв.1'}),
                              label='Адрес', max_length=1024, required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '+79267775533'}),
                            label='Телефон', max_length=20, required=False)

class RegisterAccountForm(WebForm):
    form_name = 'Регистрация аккаунта'
    submit_name = 'Зарегистрировать аккаунт'

    login = forms.CharField(label='Логин', max_length=45, required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль', max_length=128, required=True)
    admin_priv = forms.TypedChoiceField(choices=((0, 'Обычный аккаунт'), (1, 'Аккаунт администратора')), label='Тип аккаунта', required=True, coerce=int)
    def __init__(self, persons, *args, **kwargs):
        super(RegisterAccountForm, self).__init__(*args, **kwargs)
        choices = ((p['id'], '%s %s %s (%s)' % (p['surname'], p['first_name'], p['second_name'], p['email'])) for p in persons)
        self.fields['person_id'] = forms.ChoiceField(choices=choices, label='Пользователь', required=True)
