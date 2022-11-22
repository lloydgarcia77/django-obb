from django.db import models
from django.db.models import Q
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.conf import settings 
from django.utils.text import slugify
from django.urls import reverse
from django.utils.timezone import make_aware, now  
from datetime import date, datetime  
from django.utils import timezone
import uuid, os



class UserManager(BaseUserManager):
    """Manger for user profiles"""

    def create_user(self, email, f_name, m_name, l_name, gender, dob, age, contact_no, address, password=None):
        """Create a new user profile"""

        if not email:
            raise ValueError('User must have email address')

        email = self.normalize_email(email)
        user = self.model(email=email, f_name=f_name, m_name=m_name, l_name=l_name, gender=gender, dob=dob, age=age, contact_no=contact_no, address=address,  password=password)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_staffuser(self, email, f_name, m_name, l_name, gender, dob, age, contact_no, address, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(email=email, f_name=f_name, m_name=m_name, l_name=l_name, gender=gender, dob=dob, age=age, contact_no=contact_no, address=address,  password=password)
        user.staff = True
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, f_name, m_name, l_name, gender, dob, age, contact_no, address, password):
        """Create and save a new superuser with the given details"""
        user = self.create_user(email=email, f_name=f_name, m_name=m_name, l_name=l_name, gender=gender, dob=dob, age=age, contact_no=contact_no, address=address,  password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Customized model for user in django"""
    MALE = 'male'
    FEMALE = 'female'

    GENDER_LIST = (
        (MALE,'MALE'),
        (FEMALE,'FEMALE'),
    )
 
    email = models.EmailField(max_length=50, unique=True)    
    s_name =  models.CharField(max_length=50, blank=True, null=True)
    f_name = models.CharField(max_length=50, verbose_name="First Name")
    m_name = models.CharField(max_length=50, verbose_name="Middle Name", blank=True, null=True)
    l_name = models.CharField(max_length=50, verbose_name="Last Name")
    gender =  models.CharField(max_length=10, choices=GENDER_LIST, default=MALE)
    dob = models.DateField()
    age = models.IntegerField()
    contact_no =  models.CharField(max_length=15,  unique=True)
    address  = models.TextField()
    date_added = models.DateTimeField(auto_now=True) 
    is_valid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['f_name','m_name','l_name','age','gender', 'dob','contact_no', 'address',] # Email & Password are required by default.

    def get_encrpted_id(self):
        return settings.SIGNER.sign(self.id)

    
    def get_full_name(self):
        return f'{self.l_name}, {self.f_name} {self.m_name}'
    
    
    def get_short_name(self):
        return self.f_name
    
    
    def __str__(self):
        return self.email
      
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
     
 
class Bus(models.Model):
    BUS_TYPE = (
        ('ordinary', 'ordinary'),
        ('aircon', 'aircon'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4) 
    name = models.CharField(max_length=255) 
    driver_name = models.CharField(max_length=255) 
    conductor_name = models.CharField(max_length=255)  
    type = models.CharField(max_length=255, choices=BUS_TYPE, default='aircon')  
    plate_no = models.CharField(max_length=255, unique=True)  
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return self.name
    

    def save(self, *args, **kwargs):
        seats = [f's-{i}' for i in range(1,50)]
        bus_seats = BusSeat.objects.all().filter(bus=self)
        bus_seats = [s.name for s in bus_seats]
        additional_seats = set(seats) - set(bus_seats)
        removalble_seats = set(bus_seats) - set(seats) 

        if removalble_seats:
            for s in removalble_seats:
                BusSeat.objects.get(Q(bus=self) & Q(name=s))
        
        if additional_seats:
            bulk_create = [
                BusSeat(
                    bus=self,
                    name=s
                ) for s in additional_seats
            ]

            BusSeat.objects.bulk_create(bulk_create) 
        super(Bus, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date_created']


# NOTE 49 seats
class BusSeat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4) 
    bus = models.ForeignKey(Bus, related_name='fk_bs_bus', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # occupied = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return self.name
    
    class Meta:
        ordering = ['name']
        unique_together = ('bus','name')

class Route(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)   
    name = models.CharField(max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return self.name

    class Meta:
        ordering = ['-date_created']

 

class DailySchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)    
    source = models.ForeignKey(Route, related_name='fk_ds_source', on_delete=models.CASCADE)
    destination = models.ForeignKey(Route, related_name='fk_ds_destination', on_delete=models.CASCADE)
    via = models.ForeignKey(Route, related_name='fk_ds_via', on_delete=models.CASCADE)
    bus = models.ManyToManyField(Bus, related_name='fk_sd_m2m_bus')
    price = models.FloatField(default=0)
    time = models.TimeField() 
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return self.source.name

    class Meta:
        ordering = ['-date_created']
    

class Booking(models.Model):
    PENDING = 'pending' 
    APPROVED = 'approved'

    STATUS_LIST = (
        (PENDING,'pending'), 
        (APPROVED,'approved'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4) 
    booking = models.CharField(max_length=250, unique=True, blank=True, null=True)
    scheduled_route = models.ForeignKey(DailySchedule, related_name='fk_booking_route', on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, related_name='fk_booking_bus', on_delete=models.CASCADE)
    # ! https://bobbyhadz.com/blog/python-add-time-to-datetime-object
    date = models.DateField(blank=True, null=True) 
    time = models.TimeField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    total_cost = models.FloatField()
    seat_person = models.JSONField()
    reference_id = models.CharField(blank=True, max_length=50, null=True)
    status = models.CharField(max_length=50, choices=STATUS_LIST, default=PENDING)
    datetime_paid = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.scheduled_route.source.name + " -> " + self.scheduled_route.destination.name 

    class Meta:    
        
        ordering = ['-date_created']
        unique_together = ('date', 'time',)
 
class Receipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4) 
    booking = models.ForeignKey(Booking, related_name="fk_receipt_booking", on_delete=models.SET_NULL, blank=True, null=True)
    # NOTE: Source -> Destination VIA 
    route = models.CharField(max_length=200)
    total_cost = models.FloatField()
    date = models.DateField()
    seat_person = models.JSONField()
    date_created = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.route

    class Meta:    
        
        ordering = ['-date_created']
