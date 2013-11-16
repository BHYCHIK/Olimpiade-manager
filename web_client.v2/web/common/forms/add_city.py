# -*- coding: utf-8 -*-
from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from common import WebForm

class AddCityForm(WebForm):
    form_name = 'Добавление города'
    submit_name = 'Добавить'

    name = forms.CharField(label='Название города', max_length=45, required=True)

    def __init__(self, city_types, *args, **kwargs):
        super(AddCityForm, self).__init__(*args, **kwargs)
        city_choices = ((c['id'], c['short_title']) for c in city_types)
        self.fields['city_type_id'] = forms.TypedChoiceField(choices=city_choices, label='Тип города', required=True, coerce=int)
