# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect
import settings
from common.forms import RegisterPersonForm, RegisterAccountForm
from api import Api
from django.template import RequestContext

@cache_page(settings.caching_settings['static_page_cache_time'])
def index(request):
    return render_to_response('common/index.html', {}, context_instance=RequestContext(request))

def register_person(request):
    print('sdf')
    if request.method == 'POST':
        print('ee')
        form = RegisterPersonForm(request.POST)
        api = Api()
        if form.is_valid() and api.register_person(form.cleaned_data):
            print('valid')
            return HttpResponseRedirect('/thanks?from=reg_person')
    else:
        print('saf')
        form = RegisterPersonForm()

    c = {'form': form}
    return render_to_response('common/forms/register_person.html', c, context_instance=RequestContext(request))

def register_account(request):
    print('sdf')
    if request.method == 'POST':
        print('ee')
        form = RegisterAccountForm(None, request.POST)
        api = Api()
        if form.is_valid() and api.register_account(form.cleaned_data):
            print('valid')
            return HttpResponseRedirect('/thanks?from=reg_account')
    else:
        print('saf')
        form = RegisterAccountForm(None)

    c = {'form': form}
    return render_to_response('common/forms/register_account.html', c, context_instance=RequestContext(request))


@cache_page(settings.caching_settings['static_page_cache_time'])
def thanks(request):
    ref = request.GET['from']
    ref2msg = {'reg_person': 'Пользователь успешно зарегистрирован.'}
    return render_to_response('common/thanks.html', {'message': ref2msg[ref]}, context_instance=RequestContext(request))

def account_login(request):
    print('got request')
    if request.method != 'POST':
        raise ValueError() #TODO: 404

    api = Api()
    session_id = api.account_login(request.POST)
    if session_id:
        print('valid login')
        request.session['id'] = session_id
    else:
        print('invalid login')
    return HttpResponseRedirect('/')

