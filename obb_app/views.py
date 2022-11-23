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
import dateutil.parser , string, shortuuid

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
def administrator_index(request, *args, **kwargs):
    template_name = 'app/admin/index.html'
    user = get_object_or_404(models.User, email=request.user.email)

    total_bus = models.Bus.objects.all().count()
    total_routes  = models.Route.objects.all().count()
    total_daily_schedule = models.DailySchedule.objects.all().count()


    booking =  models.Booking.objects.all()
    total_bookings = booking.count()
    total_approved = booking.filter(Q(status=models.Booking.APPROVED))
    total_pending = booking.filter(Q(status=models.Booking.PENDING))
    total_cost = booking.aggregate(Sum('total_cost')).get('total_cost__sum')
    total_paid = booking.filter(Q(is_paid=True)).count()
    total_unpaid = booking.filter(Q(is_paid=False)).count()
 

    context = {
        'user': user,
        'total_bus': total_bus,
        'total_routes': total_routes,
        'total_daily_schedule': total_daily_schedule,
        'total_bookings': total_bookings,
        'total_approved': total_approved,
        'total_pending': total_pending,
        'total_paid': total_paid,
        'total_unpaid': total_unpaid,
        'total_cost': total_cost,


    }

    return render(request,template_name,context)

@login_required
def administrator_schedules(request, *args, **kwargs):
    template_name = 'app/admin/schedules/schedule.html'
    user = get_object_or_404(models.User, email=request.user.email)
 
    search = request.GET.get('search','')

    objects = models.Booking.objects.all().order_by('-date_created') 

    if request.method == 'GET':
        if search.strip(): 
            objects = objects.filter(
                Q(booking__icontains=search) |
                Q(id__icontains=search) |  

                Q(scheduled_route__source__name__icontains=search) | 
                Q(scheduled_route__destination__name__icontains=search) | 
                Q(scheduled_route__via__name__icontains=search) | 

                Q(bus__name__icontains=search) |  
                Q(bus__driver_name__icontains=search) |  
                Q(bus__conductor_name__icontains=search) |  
                Q(bus__type__icontains=search) |  
                Q(bus__plate_no__icontains=search) |  
                Q(reference_id__icontains=search) 
                )

    page = request.GET.get('page', 1)
    
    paginator = Paginator(objects, 5)

    try:
        query = paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)
     
    context = {
        'user': user,  
        'query': query,
    }

  

    return render(request,template_name,context)


@login_required
def administrator_schedules_manage(request, *args, **kwargs):
    template_name = 'app/admin/schedules/manage.html'
    user = get_object_or_404(models.User, email=request.user.email)
    id = kwargs.get('id')
    booking = get_object_or_404(models.Booking, id=id)


    if request.method == 'POST':
        _approve = request.POST.get('_approve', None)
        _delete = request.POST.get('_delete', None)
        _send_mail = request.POST.get('_send_mail', None)
 
        if isinstance(_approve, str):
            booking.status = models.Booking.APPROVED if booking.status == models.Booking.PENDING else models.Booking.PENDING 
            booking.save()
            messages.success(request, f"Booking status has been changed to: {booking.status}")
        if isinstance(_delete, str): 
            booking.delete()
            messages.error(request, "Booking has been deleted!")
        if isinstance(_send_mail, str): 
                
            mail_subject = 'CISCO Bus Inc Schedule Notification'  
            to_email = [
                i.get('email') for i in booking.seat_person
            ] 
            html_message = render_to_string('email_notifications/email_template.html', {    
                'booking': booking, 
            })     
            email = EmailMessage(  
                mail_subject, 
                html_message, 
                to=to_email, 
            )  
            email.content_subtype = 'html'  
            email.send()  
            messages.info(request, "Email has been sent to each users!")
        return HttpResponseRedirect(reverse('obb_app:administrator_schedules'))

    context = {
        'user': user,  
        'booking': booking,
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


def search_results(request, *args, **kwargs):
    template_name = 'app/client/booking_search_result.html'

    if request.method == 'GET':
        search_val = request.GET.get('search_val') 
        booking_list = models.Booking.objects.filter(Q(booking=search_val))


    context = { 
        'booking_list': booking_list,
    }

    return render(request, template_name, context)

def __get_bus_booking_seats(booking):
    bus_seats = [
        s.name for s in booking.bus.fk_bs_bus.all()
    ] 
    allocated_seats = [
        s.get('seat')  for s in booking.seat_person
    ]

    diff = set(bus_seats) - set(allocated_seats)
    diff = len(list(diff))

    # if diff < len(bus_seats):
    #     return ''

    if diff <= 0:
        return {
            "date": booking.date.strftime("%Y-%m-%d"),
            "badge": True,
            "title": "Full Schedule", 
            "classname": 'full-schedule-date'
        }
      

    return {
            "date": booking.date.strftime("%Y-%m-%d"),
            "badge": False,
            "title": "With Schedule",  
    }
  

def step1(request, *args, **kwargs):
    template_name = 'app/client/step1.html' 
    schedule = models.DailySchedule.objects.all().order_by('time')
    data = dict()
    
 
    if request.is_ajax():
        if request.method == 'POST': 
            
            now = datetime.now()
            date = request.POST.get('date', now) 

            d = datetime.strptime(date, '%m/%d/%Y')   
 
            timetoday = now.strftime("%H:%M:%S")  
            schedule = [
                {
                    'id': s.id,
                    'source': s.source,
                    'destination': s.destination,
                    'via': s.via,
                    'time': s.time, 
                    # 'available': True,
                    # ! do not forget th
                    'available': s.time > datetime.strptime(timetoday, "%H:%M:%S").time() if d.date() == now.date() else True,
                } for s in schedule
            ]
            data['is_valid'] = True
            data['html_routes'] = render_to_string('app/client/step1_route_list.html', {'schedule': schedule}, request)


            eventData = [
                __get_bus_booking_seats(e) for e in models.Booking.objects.filter(Q(status=models.Booking.APPROVED))
            ]

            data['eventData'] = eventData
            # print(eventData)
        return JsonResponse(data)

    context = {
        'schedule': schedule,
    }

    return render(request, template_name, context)


def __get_bus_seat_availables(booking, bus):
    match_bus = list(filter(lambda i: i.bus == bus, booking))
    bus_seat_count = bus.fk_bs_bus.all().count() 
     
    if bool(match_bus): 
        return (bus_seat_count - len(match_bus[0].seat_person)) 
    return bus_seat_count



def step2(request, *args, **kwargs):
    template_name = 'app/client/step2.html' 
    data = dict()
    if request.is_ajax():
        if request.method == 'POST':
            date = request.POST.get('date','')
            route = request.POST.get('route','')  

            d = datetime.strptime(date, '%m/%d/%Y')        
            schedule = get_object_or_404(models.DailySchedule, id=route)  
            bookings = models.Booking.objects.filter(Q(date=d) & Q(scheduled_route=schedule) & Q(status=models.Booking.APPROVED))#.values('bus', 'seat_person')
 
            schedule = [
                {   
                    'id': s.id,
                    'name': s.name,   
                    'driver_name': s.name,   
                    'conductor_name': s.conductor_name,   
                    'type': s.type,   
                    'plate_no': s.plate_no,  
                    'total_seat_no': s.fk_bs_bus.all().count(),
                    # ! occupied must reflect
                    'total_avail_seat_no': __get_bus_seat_availables(bookings, s)
                } for s in schedule.bus.all()
            ] 
            data['html_buses'] = render_to_string('app/client/step2_bus_list.html', {'schedule': schedule}, request)
            data['is_valid'] = True
        return JsonResponse(data)
    context = { 
    }

    return render(request, template_name, context)



def __get_occupied_seats(bookings, seat):
    if bookings:
        occupied_seats = [s.get('seat') for s in bookings[0].seat_person]
        return False if seat in occupied_seats else True
    return True

def step3(request, *args, **kwargs):
    template_name = 'app/client/step3.html'  
    data = dict()

    if request.is_ajax():
        if request.method == 'POST':
            date = request.POST.get('date','')
            route = request.POST.get('route','')
            bus = request.POST.get('bus','')
               
            # d = dateutil.parser.isoparse(date)
            d = datetime.strptime(date, '%m/%d/%Y')
            schedule = get_object_or_404(models.DailySchedule, id=route)
            bus = get_object_or_404(models.Bus, id=bus) 

            bookings = models.Booking.objects.filter(Q(date=d) & Q(scheduled_route=schedule) & Q(bus=bus) & Q(status=models.Booking.APPROVED)) 
     
         
            # NOTE if booking bus is existing
 
            bus_seat = [
                {
                    'id': b.id,
                    'name': b.name,
                    'enabled':  __get_occupied_seats(bookings, b.name),
                } for b in models.BusSeat.objects.all().filter(bus=bus)
            ]
 
 
            sorted_bus_seat = sorted(bus_seat, key=lambda i : int(re.sub('\D', '', i.get('name'))))
 
            data['html_seats'] = render_to_string('app/client/step3_seat_list.html', 
            {'sorted_bus_seat': sorted_bus_seat}, request)
            data['is_valid'] = True

        return JsonResponse(data)
 
    context = { 
        
    }

    return render(request, template_name, context)


def __check_mail(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return True if re.fullmatch(regex, email) else False


def __generate_unique_id():
    alphabet = string.ascii_lowercase + string.digits
    su = shortuuid.ShortUUID(alphabet=alphabet)
    return su.random(length=8)


def step4(request, *args, **kwargs):
    template_name = 'app/client/step4.html' 
    data = dict()
    
    if request.is_ajax():
        if request.method == 'POST': 
            route = request.POST.get('route','')
            bus = request.POST.get('bus','')
            now = datetime.now()
            selectedDate = request.POST.get('selectedDate',now)
            seat_details = request.POST.get('seat_details','')

            try:
                d = datetime.strptime(selectedDate, '%m/%d/%Y') 
                d = make_aware(d)

             
                # d = dateutil.parser.parse(selectedDate)
                # print(d.strftime('%Y-%m-%d %I:%M:%S %p')) 
                route = get_object_or_404(models.DailySchedule, id=route, bus__id=bus)
                bus = get_object_or_404(models.Bus, id=bus)


                if d.date() == now.date():
                    if datetime.now().time() > route.time:
                        raise Exception('Invalid Time')

                bookings = models.Booking.objects.filter(Q(date=d) & Q(scheduled_route=route) & Q(bus=bus) & Q(status=models.Booking.APPROVED)) 
            
         
                # NOTE: check the seat allocation
                seat_details = json.loads(seat_details) 

                for s in seat_details:
                    if not __get_occupied_seats(bookings, s.get('seat')):
                        raise Exception('Seat has been occupied')

                    if not __check_mail(s.get('email')):
                        raise Exception('Invalid Email') 
                    
                    int(s.get('age'))

                # NOTE: After validation
                # NOTE: Computing for the total
                # print(seat_details)
                # seat_details = map(lambda i: {
                #     'name': i.get('name'),
                #     'email': i.get('email'),
                #     'age': i.get('age'),
                #     'discount': '20%' if (int(i.get('age')) <= 18 or int(i.get('age')) >= 60 ) else '0',
                #     'sub_total': (route.price * 0.20) if (int(i.age) <= 18 or int(i.get('age')) >= 60) else route.price
                # }, seat_details)

                # total = map(lambda i: float(i.get('sub_total')), seat_details)

                booking_id = __generate_unique_id()
                # NOTE Setting the details on the page
                booking_data = {
                    'booking_id': booking_id,
                    'route': route,
                    'bus': bus, 
                    'datetoday': datetime.now().strftime('%b %d,  %Y %I:%M %p'),
                    'seat_details': seat_details, 
                    'total_amt': route.price * len(seat_details),
                    'total_passengers': len(seat_details),
                }

                data['html_booking_confirmation'] = render_to_string('app/client/step4_booking_confirmation.html', 
                {'booking_data': booking_data}, request)
                
                data['passenger_details'] = seat_details 
                data['bookid'] = booking_id
                data['is_valid'] = True
 
            except Exception as e:
                data['is_valid'] = False
                data['message'] = f'Error cannot proceed! {e}'  
        return JsonResponse(data)
    context = { 
    }

    return render(request, template_name, context)


def step5(request, *args, **kwargs):
    template_name = 'app/client/step5.html' 
    data = dict()   

    if request.is_ajax():
        if request.method == 'POST':
            route = request.POST.get('route','')
            bus = request.POST.get('bus','')
            booking = request.POST.get('booking','')
            now = datetime.now()
            selectedDate = request.POST.get('selectedDate',now)
            seat_details = request.POST.get('seat_details','')

            try:
                d = datetime.strptime(selectedDate, '%m/%d/%Y') 
                d = make_aware(d) 

                route = get_object_or_404(models.DailySchedule, id=route, bus__id=bus)
                bus = get_object_or_404(models.Bus, id=bus)
                if d.date() == now.date():
                    if datetime.now().time() > route.time:
                        raise Exception('Invalid Time')

                bookings = models.Booking.objects.filter(Q(date=d) & Q(scheduled_route=route) & Q(bus=bus) & Q(status=models.Booking.APPROVED)) 
               
                # NOTE: check the seat allocation
                seat_details = json.loads(seat_details) 

                for s in seat_details:
                    if not __get_occupied_seats(bookings, s.get('seat')):
                        raise Exception('Seat has been occupied')
                    if not __check_mail(s.get('email')):
                        raise Exception('Invalid Email') 
                    int(s.get('age'))


                models.Booking.objects.create(
                    booking=booking,
                    scheduled_route=route,
                    bus=bus,
                    date=d,
                    time=route.time,
                    total_cost=len(seat_details) * route.price,
                    seat_person=seat_details,
                )
                data['is_valid'] = True

            except Exception as e:
                data['is_valid'] = False
                data['message'] = f'Error cannot proceed! {e}' 
                print(e)
        
        return JsonResponse(data)

    
    context = { 
    }

    return render(request, template_name, context)


def step_final(request, *args, **kwargs):
    data = dict()


    if request.is_ajax():
        if request.method == 'POST':
            booking_id = request.POST.get('booking_id')
            try:
                booking = get_object_or_404(models.Booking, booking=booking_id, is_paid=False, reference_id=None)


                data['html_booking_details'] = render_to_string('app/client/step5_booking_details.html', 
                                        {'booking': booking}, request)
                data['booking_id'] = booking_id
                data['is_valid'] = True
                data['message'] = f'Booking ID has been found! Please proceed to your payment!'
            except Exception as e:
                data['is_valid'] = False
                data['message'] = f'There\'s an Error: {e} encountered!'
        return JsonResponse(data)
    else:
        raise Http404



def update_ref_id(request, *args, **kwargs):
    data = dict()

    if request.is_ajax():
        if request.method == 'POST':
            booking_id = request.POST.get('booking_id')
            payment_ref_id = request.POST.get('payment_ref_id')
            try:
                booking = get_object_or_404(models.Booking, booking=booking_id, is_paid=False, reference_id=None)
                booking.is_paid = True
                booking.datetime_paid = timezone.now()
                booking.reference_id = payment_ref_id
                booking.save()
 
                data['is_valid'] = True
                data['message'] = f'Your payment details has been successful!'
            except Exception as e:
                data['is_valid'] = False
                data['message'] = f'There\'s an Error: {e} encountered!' 
        return JsonResponse(data)
    else:
        raise Http404()