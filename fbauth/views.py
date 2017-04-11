# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.shortcuts import render
import facebook
from social_django.utils import psa
from social_core.pipeline.partial import partial
from django.contrib.auth import login
import requests
import json
import facebook
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from .forms import UpdateForm
from facepy import GraphAPI

def home(request):
		return render(request, 'index.html')

@login_required
def listings(request):
	access_token=User.objects.get(email=request.user.email, password="1234")
	if request.user.is_authenticated():
		graph = GraphAPI(access_token)

		accounts = graph.get("me/accounts")
		args = {'fields' : 'id, name, phone, access_token, single_line_address'}
		page_info = []
		for i in accounts["data"]:
			page_id = i['id']
			graph_data = graph.get(page_id, **args)
			page_info.append(graph_data)

		return render(request, 'listings.html', {'data' : page_info})

def save_profile(backend, user, response, *args, **kwargs):
	access_token = response['access_token']
	user_id = response['id']
	user_name = response['name']
	try:
		user_obj = User.objects.get(email=user.email, password="1234")
	except ObjectDoesNotExist:
		user_obj = User(username=access_token, email=user.email, password="1234")
		user_obj.save()

def update_profile(form_data):
	page_access_token = form_data['page_access_token']
	graph = GraphAPI(page_access_token)
	graph.post(
    path = form_data['page_id'],
    phone = form_data['phone']
  )	

def update(request, page_id, page_access_token):
	if request.method == 'POST':
		form = UpdateForm(data=request.POST)
		form_data = {}
		# form_data['name'] = request.POST.get('name')
		# form_data['email'] = request.POST.get('email')
		form_data['phone'] = request.POST.get('phone')
		form_data['page_id'] = page_id
		form_data['page_access_token'] = page_access_token

		if(len(form_data['phone']) > 0):
			update_profile(form_data)
		return redirect('listings')
	else:
		form_class = UpdateForm()
		return render(request, 'update.html', {'form': form_class})
