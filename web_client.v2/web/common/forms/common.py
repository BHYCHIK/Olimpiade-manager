# -*- coding: utf-8 -*-
from django import forms

error_messages = {
    'required': 'Поле является обязательным',
    'invalid': 'Введены неверные для этого поля данные',
    'min_value': 'Значение должно быть >= %(limit_value)d',
    'max_value': 'Значение должно быть <= %(limit_value)d',
}

class WebForm(forms.Form):
    def init_messages(self):    
        for _, field in self.fields.items():
            field.error_messages = error_messages
