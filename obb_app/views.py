from django.shortcuts import render, get_object_or_404
from django.http import (
    JsonResponse,
    Http404,
    HttpResponseRedirect
)  
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login
from django.db.models import Q, Sum, F, Avg
from django.db.utils import IntegrityError, DataError
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone 
from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger
) 
from django.contrib import messages
from datetime import datetime, timedelta
from django.utils.timezone import make_aware  
 
 
from obb_app import (
    models,
    forms,   
)   
from django.conf import settings 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  

# NOTE: Email Activation
from obb_app.tokens import account_activation_token  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.utils.html import strip_tags
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt

import requests, logging, traceback, json, re
import dateutil.parser 

logger = logging.getLogger('django')
# NOTE: Error Pages

def error_404(request, exception):
    return render(request, "error/error_404.html", {})


def error_500(request):
    return render(request, "error/error_500.html", {})


# NOTE: Login 
def login_page(request):
    template_name = "registration/login.html"  
    # NOTE: Redirects to the index page when trying to go back 
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("obb_app:administrator_index"))
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
      
        user = authenticate(email=email, password=password) 
        if user:  
            if user.is_active: 
                login(request, user) 
                # request.session.set_expiry(request.session.get_expiry_age())
                previous_page = request.GET.get('next', reverse("obb_app:administrator_index"))
                return HttpResponseRedirect(previous_page)
            else:
                messages.error(request, "Your account is needs approval, Please contact your administrator!")
        else:
            messages.error(request, "Your account is INVALID!")
        
    return render(request, template_name)


# NOTE Admin
@login_required
def administrator_index(request):
    template_name = 'app/admin/index.html'
    user = get_object_or_404(models.User, email=request.user.email)

    context = {
        'user': user,
    }

    return render(request,template_name,context)



# NOTE Client
def index(request, *args, **kwargs): 
    template_name = 'index.html'
    data = dict()
     
     
    context = {
        'user': request.user,  
    }
    return render(request, template_name, context)


def step1(request, *args, **kwargs):
    template_name = 'app/client/step1.html' 
    schedule = models.DailySchedule.objects.all().order_by('time')
    data = dict()

    # if request.is_ajax():
    #     if request.method == 'POST':

    #         print(request.POST)
    #         data['is_valid'] = True
    #         return JsonResponse(data)
    context = {
        'schedule': schedule,
    }

    return render(request, template_name, context)


def step2(request, *args, **kwargs):
    template_name = 'app/client/step2.html' 
    data = dict()
    if request.is_ajax():
        if request.method == 'POST':
            date = request.POST.get('date','')
            route = request.POST.get('route','')
             
            #  ! msut be apply unti step 4
            d = dateutil.parser.isoparse(date)
            schedule = get_object_or_404(models.DailySchedule, id=route)
            # print(d.strftime('%Y-%m-%d')) 

            schedule = [
                {   
                    'id': s.id,
                    'name': s.name,   
                    'driver_name': s.name,   
                    'conductor_name': s.conductor_name,   
                    'type': s.type,   
                    'plate_no': s.plate_no,  
                    'total_seat_no': s.fk_bs_bus.all().count(),
                    'total_avail_seat_no': models.BusSeat.objects.filter(Q(bus=s) & Q(occupied=False)).count()
                } for s in schedule.bus.all()
            ]
 

            data['html_buses'] = render_to_string('app/client/step2_bus_list.html', {'schedule': schedule}, request)
            data['is_valid'] = True
        return JsonResponse(data)
    context = { 
    }

    return render(request, template_name, context)

def step3(request, *args, **kwargs):
    template_name = 'app/client/step3.html'  
    data = dict()

    if request.is_ajax():
        if request.method == 'POST':
            date = request.POST.get('date','')
            route = request.POST.get('route','')
            bus = request.POST.get('bus','')
              
            #  ! msut be apply unti step 4
            d = dateutil.parser.isoparse(date)
            schedule = get_object_or_404(models.DailySchedule, id=route)
            bus = get_object_or_404(models.Bus, id=bus) 
            
            bus_seat = models.BusSeat.objects.all().filter(bus=bus)
 
            sorted_bus_seat = sorted(bus_seat, key=lambda i : int(re.sub('\D', '', i.name)))

            # for i in sorted_bus_seat:
            #     print(i.name)

            data['html_seats'] = render_to_string('app/client/step3_seat_list.html', 
            {'sorted_bus_seat': sorted_bus_seat}, request)
            data['is_valid'] = True

        return JsonResponse(data)


  
    context = { 
        
    }

    return render(request, template_name, context)

def step4(request, *args, **kwargs):
    template_name = 'app/client/step4.html' 
    
    # ! pass time must not be able to be selcted because
    # ! make a boolean before serving to the front end
    # ! price per seat
    # ! user details
    # ! validate all the data
    context = { 
    }

    return render(request, template_name, context)
