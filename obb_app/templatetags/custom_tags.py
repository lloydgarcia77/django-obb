from django import template
from django.shortcuts import get_object_or_404
from django.utils import timezone 
import os, pytz, datetime, random 
from django.db.models import Q, Max, Min, Sum, F  

register = template.Library()



  

@register.simple_tag(takes_context=True)
def get_total(context, query):
    
    discounts = ['student', 'senior']
    discount = 0.20

    total_price = 0
    total_passengers = 0
    total_amount = 0
    total_f = 0

    for q in query:
        with_discount = filter(lambda i : i.get('discount_type').lower() in discounts, q.seat_person)
        total_dis_count = len(list(with_discount))
        total_dis_count = total_dis_count * discount
        total_amt = q.scheduled_route.price * len(q.seat_person)
        
    
        total_dis_amt = total_amt * total_dis_count
        total =total_amt - total_dis_amt

        total_price+=q.scheduled_route.price
        total_passengers+=len(q.seat_person)
        total_amount+=total_amt
        total_f+=total
 


    return {
        'total_price':total_price,
        'total_amount':total_amount,
        'total_passengers':total_passengers,
        'total_f':total_f,
    }
 

@register.simple_tag(takes_context=True)
def get_discount_total(context, obj, price):

    discounts = ['student', 'senior']
    discount = 0.20
    with_discount = filter(lambda i : i.get('discount_type').lower() in discounts, obj)
    total_dis_count = len(list(with_discount))
    total_dis_count = total_dis_count * discount
    total_amt = price * len(obj)
    
 
    total_dis_amt = total_amt * total_dis_count
    total =total_amt - total_dis_amt


 
    return {'total':total, 'discount':"{:.0%}".format(total_dis_count)}


@register.simple_tag
def custom_date_format(date, date_only=False): 
    
    tz = pytz.timezone('Asia/Manila') 
    if date != None:     
        # Only date with date and time
        if isinstance(date, datetime.datetime): 
            date = timezone.localtime(date, tz) 
            if date_only: 
                date = date.strftime("%b. %d, %Y") 
            else:
                date = date.strftime("%b. %d, %Y, %I:%M %p")  
        elif isinstance(date, datetime.date): 
            date = date.strftime("%b. %d, %Y") 
                
    return date

 
@register.filter
def custom_time_format(time):
    if time != None:       
        time = time.strftime("%I:%M %p")   
    return time

@register.filter
def custom_date_only_format(date, args=None):
    if date != None:       
        date = date.strftime("%b. %d, %Y") 
 
        if args is not None:  
            parsed_dt = datetime.datetime.strptime(date, '%b. %d, %Y')
            date = parsed_dt.strftime(args)  

    return date
  


