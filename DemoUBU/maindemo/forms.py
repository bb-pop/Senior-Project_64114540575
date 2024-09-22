from django import forms
from maindemo.models import Item, UserProfile


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['prefix', 'first_name', 'last_name', 'email', 'id_student', 'faculty']
        widgets = {
            'prefix': forms.Select(choices=[('นาย', 'นาย'), ('นาง', 'นาง'), ('นางสาว', 'นางสาว')]),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'id_student': forms.TextInput(attrs={'class': 'form-control'}),
            'faculty': forms.Select(choices=[('คณะวิทยาศาสตร์', 'คณะวิทยาศาสตร์'),
                                            ('คณะเกษตรศาสตร์', 'คณะเกษตรศาสตร์'),
                                            ('คณะวิศวกรรมศาสตร์', 'คณะวิศวกรรมศาสตร์'),
                                            ('คณะศิลปศาสตร์', 'คณะศิลปศาสตร์'),
                                            ('คณะเภสัชศาสตร์', 'คณะเภสัชศาสตร์'),
                                            ('คณะบริหารศาสตร์', 'คณะบริหารศาสตร์'),
                                            ('วิทยาลัยแพทยศาสตร์และการสาธารณสุข', 'วิทยาลัยแพทยศาสตร์และการสาธารณสุข'),
                                            ('คณะศิลปประยุกต์และสถาปัตยกรรมศาสตร์', 'คณะศิลปประยุกต์และสถาปัตยกรรมศาสตร์'),
                                            ('คณะนิติศาสตร์', 'คณะนิติศาสตร์'),
                                            ('คณะรัฐศาสตร์', 'คณะรัฐศาสตร์'),
                                            ('คณะพยาบาลศาสตร์', 'คณะพยาบาลศาสตร์'),
                                            ]
                                    )
        }
        
class DateRangeForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    item_id = forms.ModelChoiceField(queryset=Item.objects.all(), required=False, label='Item', empty_label="Select Item")