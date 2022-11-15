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
     