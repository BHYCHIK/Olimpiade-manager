# -*- coding: utf-8 -*-
from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from common import WebForm

class AddWorkForm(WebForm):
    form_name = 'Добавление работы участника соревнования'
    submit_name = 'Добавить'

    title = forms.CharField(max_length=2048, label='Название работы', required=True)
    state = forms.ChoiceField(choices=(('none', 'Нет'),('passes', 'Прошла'), ('not passed', 'Не прошла')), label='Состояние работы', required=True)

    def __init__(self, participants, curators, schools, *args, **kwargs):
        super(AddWorkForm, self).__init__(*args, **kwargs)
        participant_choices = ((p['id'], '%s %s %s - %s' % (p['surname'], p['first_name'], p['second_name'], p['year'])) for p in participants)
        self.fields['participant_id'] = forms.TypedChoiceField(choices=participant_choices, label='Участник соревнования', required=True, coerce=int)
        curator_choices = ((c['id'], '%s %s %s - %s' % (c['surname'], c['first_name'], c['second_name'], c['year'])) for c in curators)
        self.fields['curator_id'] = forms.TypedChoiceField(choices=curator_choices, label='Куратор участника', required=True, coerce=int)
        school_choices = ((s['id'], '%s' % (s['title'] if 'title' in s and s['title'] else str(s['number']))) for s in schools)
        self.fields['school_id'] = forms.TypedChoiceField(choices=school_choices, label='Школа участника', required=True, coerce=int)
        self.init_messages()
