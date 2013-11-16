# -*- coding: utf-8 -*-
from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from common import WebForm

class AddSchoolForm(WebForm):
    form_name = 'Добавление школы'
    submit_name = 'Добавить'

    number = forms.IntegerField(label='Номер школы', required=False)
    title = forms.CharField(label='Название школы', max_length=1024, required=False)
    address = forms.CharField(label='Адрес школы', max_length=1024, required=True)

    def __init__(self, cities, school_types, *args, **kwargs):
        super(AddSchoolForm, self).__init__(*args, **kwargs)
        city_choices = ((c['id'], c['name']) for c in cities)
        self.fields['city_id'] = forms.TypedChoiceField(choices=city_choices, label='Город', required=True, coerce=int)
        school_choices = ((c['id'], c['short_title']) for c in school_types)
        self.fields['school_type_id'] = forms.TypedChoiceField(choices=school_choices, label='Тип школы', required=True, coerce=int)
