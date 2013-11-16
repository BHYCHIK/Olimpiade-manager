# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect
import settings
from common.forms import *
from common.api import Api, ApiUser
from django.template import RequestContext

@cache_page(settings.caching_settings['static_page_cache_time'])
def index(request):
    return render_to_response('common/index.html', {}, context_instance=RequestContext(request))

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
    return render_to_response('common/forms/register_account.html', c, context_instance=RequestContext(request))


@cache_page(settings.caching_settings['static_page_cache_time'])
def thanks(request):
    print(request.session['id'])
    ref = request.GET['from']
    ref2msg = {'reg_person': 'Пользователь успешно зарегистрирован.',
               'reg_account': 'Аккаунт успешно зарегистрирован.',
               'successful_add': 'Добавление произошло успешно.'}
    return render_to_response('common/thanks.html', {'message': ref2msg[ref]}, context_instance=RequestContext(request))

def account_login(request):
    if request.method != 'POST':
        raise ValueError() #TODO: 404

    post = request.POST
    request.api_user.login(request, post['login'], post['password'])
    return HttpResponseRedirect('/')

def account_logout(request):
    if request.method != 'POST':
        raise ValueError() #TODO: 404

    request.api_user.logout()
    return HttpResponseRedirect('/')

def about(request):
    return render_to_response('common/about.html', context_instance=RequestContext(request))

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
@simple_form(form_cls=AddCityTypeForm, redirect='/thanks?from=successful_add')
def add_city_type(request, form_data, api):
    return api.add_city_type(form_data)

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
    c = {'criterias': api.get_criteria_titles(), 'header': 'Зарегистрированные критерии'}
    return render_to_response('common/criterias.html', c, context_instance=RequestContext(request))

@ApiUser.admin_required
def cities(request, api):
    c = {'cities': api.get_cities(), 'header': 'Зарегистрированные критерии'}
    return render_to_response('common/cities.html', c, context_instance=RequestContext(request))
