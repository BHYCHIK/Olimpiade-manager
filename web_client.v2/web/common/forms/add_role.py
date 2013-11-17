# -*- coding: utf-8 -*-
from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from common import WebForm

class AddRoleForm(WebForm):
    form_name = 'Добавление роли в соревновании'
    submit_name = 'Добавить'

    choices = (('expert', 'Эксперт'), ('reviewer', 'Рецензент'), ('admin', 'Администратор'), ('curator', 'Куратор'), ('participant', 'Участник'))
    role = forms.ChoiceField(label='Роль', choices=choices, required=True)

    def __init__(self, persons, competitions, *args, **kwargs):
        super(AddRoleForm, self).__init__(*args, **kwargs)
        person_choices = ((c['id'], '%s %s %s' % (c['surname'], c['first_name'], c['second_name'])) for c in persons)
        self.fields['person_id'] = forms.TypedChoiceField(choices=person_choices, label='Участник', required=True, coerce=int)
        competition_choices = ((c['id'], c['year']) for c in competitions)
        self.fields['competition_id'] = forms.TypedChoiceField(choices=competition_choices, label='Год соревнования', required=True, coerce=int)
