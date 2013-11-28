# -*- coding: utf-8 -*-
from django import forms
from bootstrap3_datetime.widgets import DateTimePicker
from common import WebForm

class AddCriteriaScoreForm(WebForm):
    submit_name = 'Проставить'

    def __init__(self, criteria_titles, works, year, *args, **kwargs):
        super(AddCriteriaScoreForm, self).__init__(*args, **kwargs)

        works_choices = ((w['id'], '%s - %s' % (w['title'], w['person_name'])) for w in works)
        self.fields['work_id'] = forms.TypedChoiceField(choices=works_choices, label='Работа участника соревнования', required=True, coerce=int)
        for i, cr in enumerate(criteria_titles):
            self.fields['cr_' + str(i)] = forms.IntegerField(min_value=0, max_value=5, label=u'Оценка по критерию "%s"' % cr['short_name'])
        self.form_name = 'Проставление оценок участнику соревнований %d года' % year
        self.init_messages()
