# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect
import settings
from common.forms import *
from common.api import Api, ApiUser
from django.template import RequestContext
import datetime
import logging

@cache_page(settings.caching_settings['static_page_cache_time'])
def error500(request):
    return render_to_response('common/500.html', {}, context_instance=RequestContext(request))

@cache_page(settings.caching_settings['static_page_cache_time'])
def index(request):
    return render_to_response('common/index.html', {}, context_instance=RequestContext(request))


@cache_page(settings.caching_settings['static_page_cache_time'])
def no_expert(request):
    return render_to_response('common/no_expert.html', {}, context_instance=RequestContext(request))

def simple_form(form_cls, redirect):
    def wrap(func):
        def wrapped_f(request, *args, **kwargs):
            form = form_cls(request.POST or None)
            if form.is_valid() and func(request, form.cleaned_data, *args, **kwargs):
                return HttpResponseRedirect(redirect)
            c = {'form': form}
            return render_to_response('common/forms/simple.html', c, context_instance=RequestContext(request))
        return wrapped_f
    return wrap

@ApiUser.admin_required
@simple_form(form_cls=RegisterPersonForm, redirect='/thanks?from=reg_person')
def register_person(request, form_data, api):
    return api.register_person(form_data)

@ApiUser.admin_required
def register_account(request, api):
    form = RegisterAccountForm(api.get_all_persons(), request.POST or None)
    if form.is_valid():
        reg_data = form.cleaned_data
        if api.register_account(reg_data):
            return HttpResponseRedirect('/thanks?from=reg_account')

    c = {'form': form}
    return render_to_response('common/forms/simple.html', c, context_instance=RequestContext(request))

@cache_page(settings.caching_settings['static_page_cache_time'])
def thanks(request):
    ref = request.GET['from']
    ref2msg = {'reg_person': 'Пользователь успешно зарегистрирован.',
               'reg_account': 'Аккаунт успешно зарегистрирован.',
               'successful_add': 'Добавление произошло успешно.'}
    return render_to_response('common/thanks.html', {'message': ref2msg[ref]}, context_instance=RequestContext(request))

def account_login(request):
    if request.method != 'POST':
        raise ValueError() #TODO: 404

    post = request.POST
    sess_id, err = request.api_user.login(request, post['login'], post['password'])
    if sess_id:
        red_url = '/'
    elif err and err['code'] == Api.ERR_CODE_INVALID_LOGIN:
        red_url = '/bad_login'
    else:
        red_url = '/500'
    return HttpResponseRedirect(red_url)

def account_logout(request):
    if request.method != 'POST':
        raise ValueError() #TODO: 404

    request.api_user.logout()
    return HttpResponseRedirect('/')

def about(request):
    return render_to_response('common/about.html', context_instance=RequestContext(request))
def bad_login(request):
    return render_to_response('common/bad_login.html', context_instance=RequestContext(request))

@ApiUser.admin_required
def persons(request, api):
    c = {'persons': api.get_all_persons()}
    return render_to_response('common/persons.html', c, context_instance=RequestContext(request))

@ApiUser.admin_required
@simple_form(form_cls=AddSchoolTypeForm, redirect='/thanks?from=successful_add')
def add_school_type(request, form_data, api):
    return api.add_school_type(form_data)

@ApiUser.admin_required
def school_types(request, api):
    c = {'types': api.get_school_types(), 'header': 'Зарегистрированные типы школ'}
    return render_to_response('common/types.html', c, context_instance=RequestContext(request))

@ApiUser.admin_required
def get_schools(request, api):
    schools = api.get_schools()
    for school in schools:
        school['city'] = api.get_city(school['city_id'])['name']
    return render_to_response('common/schools.html', {'schools': schools}, context_instance=RequestContext(request))

@ApiUser.admin_required
def add_school(request, api):
    form = AddSchoolForm(api.get_cities(), api.get_school_types(), request.POST or None)
    if form.is_valid():
        reg_data = form.cleaned_data
        if api.add_school(reg_data):
            return HttpResponseRedirect('/thanks?from=reg_account')

    c = {'form': form}
    return render_to_response('common/forms/simple.html', c, context_instance=RequestContext(request))

@ApiUser.admin_required
@simple_form(form_cls=AddCityTypeForm, redirect='/thanks?from=successful_add')
def add_city_type(request, form_data, api):
    return api.add_city_type(form_data)

@ApiUser.admin_required
def add_city(request, api):
    form = AddCityForm(api.get_city_types(), request.POST or None)
    if form.is_valid():
        reg_data = form.cleaned_data
        if api.add_city(reg_data):
            return HttpResponseRedirect('/thanks?from=successful_add')

    c = {'form': form}
    return render_to_response('common/forms/simple.html', c, context_instance=RequestContext(request))

@ApiUser.admin_required
def city_types(request, api):
    c = {'types': api.get_city_types(), 'header': 'Зарегистрированные типы городов'}
    return render_to_response('common/types.html', c, context_instance=RequestContext(request))

@ApiUser.admin_required
@simple_form(form_cls=AddCriteriaTitleForm, redirect='/thanks?from=successful_add')
def add_criteria_title(request, form_data, api):
    return api.add_criteria_title(form_data)

@ApiUser.admin_required
def criteria_titles(request, api):
    c = {'criterias': api.get_criteria_titles()}
    return render_to_response('common/criterias.html', c, context_instance=RequestContext(request))

@ApiUser.admin_required
def cities(request, api):
    c = {'cities': api.get_cities()}
    return render_to_response('common/cities.html', c, context_instance=RequestContext(request))

@ApiUser.admin_required
def competitions(request, api):
    competitions = api.get_competitions()
    data = []
    for competition in competitions:
        participants = api.get_competition_participants(competition['id'])
        data.append({'year': competition['year'], 'id': competition['id'], 'participants': participants, 'participants_count': len(participants)})
    return render_to_response('common/competitions.html', {'competitions': data}, context_instance=RequestContext(request))

@ApiUser.admin_required
@simple_form(form_cls=StartCompetitionForm, redirect='/thanks?from=successful_add')
def start_competition(request, form_data, api):
    return api.start_competition(form_data)

@ApiUser.admin_required
def add_role(request, api):
    form = AddRoleForm(api.get_all_persons(), api.get_competitions(), request.POST or None)
    if form.is_valid():
        reg_data = form.cleaned_data
        if api.add_role(reg_data):
            return HttpResponseRedirect('/thanks?from=successful_add')

    c = {'form': form}
    return render_to_response('common/forms/simple.html', c, context_instance=RequestContext(request))

@ApiUser.admin_required
def add_work(request, api):
    competitions = api.get_competitions()
    participants = []
    curators = []
    for competition in competitions:
        year = competition['year']
        comp_participants = []
        for p in api.get_competition_participants(competition['id']):
            participant = dict(p)
            participant.update({'year': year})
            comp_participants.append(participant)
        participants.extend(comp_participants)
        
        comp_curators = []
        for c in api.get_competition_curators(competition['id']):
            curator = dict(c)
            curator.update({'year': year})
            comp_curators.append(curator)
        curators.extend(comp_curators)

    schools = api.get_schools()
    print('curators', curators)
    form = AddWorkForm(participants, curators, schools, request.POST or None)
    if form.is_valid():
        reg_data = form.cleaned_data
        if api.add_work(reg_data):
            return HttpResponseRedirect('/thanks?from=successful_add')

    c = {'form': form}
    return render_to_response('common/forms/simple.html', c, context_instance=RequestContext(request))

@ApiUser.admin_required
def add_score(request, api):
    year = datetime.date.today().year
    roles = request.api_user.roles()
    expert_id = None
    for role in roles:
        cid = role['competition_id']
        if role['role'] == 'expert':
            comp = api.get_competition(cid)
            if comp['year'] == year:
                expert_id = role['id']
    if not expert_id:
        logger = logging.getLogger('main')
        logger.error(u'Пользователь не является экспертом в текущих соревнованиях, поэтому ему отказывается в доступе к проставлению оценок')
        return HttpResponseRedirect('/no_expert')

    works = []
    comps = (c for c in api.get_competitions() if c['year'] == year)
    for competition in comps: 
        cw = api.get_competition_works(competition['id'])
        participants = (api.get_role(w['id'])['person_id'] for w in cw)
        people = map(api.get_person, participants)
        works.extend({'id': w['id'], 'title': w['title'], 'person_name': '%s %s %s' % (p['surname'], p['first_name'], p['second_name'])} for w, p in zip(cw, people))
    criteria_titles = api.get_criteria_titles()
    form = AddCriteriaScoreForm(criteria_titles, works, year, request.POST or None)
    if form.is_valid():
        reg_data = form.cleaned_data
        score = api.add_score({'expert_id': expert_id, 'work_id': reg_data['work_id']})

        err = False
        for key, value in reg_data.iteritems():
            if not key.startswith('cr_'):
                continue
            i = int(key[len('cr_'):])
            if not api.add_criteria_score({'score_id': score['score_id'], 'criteria_title_id': criteria_titles[i]['id'], 'value': value}):
                err = True
                break
            
        if err:
            raise ValueError
        return HttpResponseRedirect('/thanks?from=successful_add')

    c = {'form': form}
    return render_to_response('common/forms/simple.html', c, context_instance=RequestContext(request))
