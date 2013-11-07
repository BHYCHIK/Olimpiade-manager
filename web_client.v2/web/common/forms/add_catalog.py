# -*- coding: utf-8 -*-
from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from common import WebForm

class AddSchoolTypeForm(WebForm):
    form_name = "Добавление нового типа школы"
    submit_name = "Добавить"

    short_title = forms.CharField(label='Краткое название', max_length=45)
    full_title = forms.CharField(label='Полное название', max_length=2048)

class AddCityTypeForm(WebForm):
    form_name = "Добавление нового типа города"
    submit_name = "Добавить"

    short_title = forms.CharField(label='Краткое название', max_length=45)
    full_title = forms.CharField(label='Полное название', max_length=2048)
