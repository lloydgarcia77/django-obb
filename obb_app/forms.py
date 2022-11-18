from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db.models import Q 
from obb_app import models

User = get_user_model()

 
class UserAdminCreationForms(forms.ModelForm):
    """
        A form for creating new users. Includes all the required
        fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = '__all__'
    
    def clean(self):
        '''
            Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")

        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match!")
        
        return self.cleaned_data
    
    def save(self, commit=True):
        """
            Save the provided password in hashed format
        """
        
        # Invoke the super class save funtion to trigger the save method
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
        
        return user
 

class UserAdminChangeForm(forms.ModelForm):
    """
        A form for updating users. Includes all the fields on
        the user, but replaces the password field with admin's
        password hash display field.
    """

    password = ReadOnlyPasswordHashField()  

    class Meta:
        model = User
        fields = '__all__'
    
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

 
# class BusForm(forms.ModelForm): 
  
#     class Meta:
#         model = models.Bus
#         exclude = ('id', 'date_created', )

#     def __init__(self, *args, **kwargs):
#         super(BusForm, self).__init__(*args, **kwargs) 
     
#         self.fields['name'].widget.attrs = {
#             'class': 'form-control',  
#             'placeholder': 'Name', 
#             'required': 'required'
#         }
#         self.fields['driver_name'].widget.attrs = {
#             'class': 'form-control  ', 
#             'placeholder': 'Driver Name', 
#             'required': 'required'
#         } 
#         self.fields['conductor_name'].widget.attrs = {
#             'class': 'form-control  ', 
#             'placeholder': 'Conductor Name', 
#             'required': 'required'
#         } 
#         self.fields['type'].widget.attrs = {
#             'class': 'form-control  select2',  
#             'required': 'required'
#         } 
#         self.fields['plate_no'].widget.attrs = {
#             'class': 'form-control  ', 
#             'placeholder': 'Plate No', 
#             'required': 'required'
#         } 
 

# class BusSeatForm(forms.ModelForm): 
  
#     class Meta:
#         model = models.BusSeat
#         exclude = ('id', 'date_created', 'bus', 'occupied' )

#     def __init__(self, *args, **kwargs):
#         super(BusSeatForm, self).__init__(*args, **kwargs) 
     
#         self.fields['name'].widget.attrs = {
#             'class': 'form-control',  
#             'placeholder': 'Name', 
#             'required': 'required'
#         }


# class RouteForm(forms.ModelForm): 
  
#     class Meta:
#         model = models.Route
#         exclude = ('id', 'date_created',)

#     def __init__(self, *args, **kwargs):
#         super(RouteForm, self).__init__(*args, **kwargs) 
     
#         self.fields['name'].widget.attrs = {
#             'class': 'form-control',  
#             'placeholder': 'Name', 
#             'required': 'required'
#         }


# class DailyScheduleForm(forms.ModelForm): 
  
    class Meta:
        model = models.DailySchedule
        exclude = ('id', 'date_created', )

    def __init__(self, *args, **kwargs):
        super(DailyScheduleForm, self).__init__(*args, **kwargs) 
     
        self.fields['source'].widget.attrs = {
            'class': 'form-control select2',   
            'required': 'required'
        }
     
        self.fields['destination'].widget.attrs = {
            'class': 'form-control select2',   
            'required': 'required'
        }
     
        self.fields['via'].widget.attrs = {
            'class': 'form-control select2',   
            'required': 'required'
        }
     
        self.fields['bus'].widget.attrs = {
            'class': 'form-control select2',   
            'required': 'required'
        }

        self.fields['time'].widget.attrs = {
            'class': 'form-control',   
            'required': 'required'
        }