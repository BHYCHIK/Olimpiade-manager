# -*- coding: utf-8 -*-
from django import forms

error_messages = {
    'required': 'Поле является обязательным',
    'invalid': 'Введены неверные для этого поля данные',
}

class WebForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(WebForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.error_messages = error_messages
