from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Distributor


class DistributorProfileForm(forms.ModelForm):
    class Meta:
        model = Distributor
        fields = (
            'company_name', 'contact_person', 'email', 'phone',
            'address', 'city', 'province', 'postal_code',
            'services_offered', 'bio', 'latitude', 'longitude',
        )
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class DistributorRegistrationForm(UserCreationForm):
    username = None
    company_name = forms.CharField(max_length=255)
    cif = forms.CharField(max_length=30, label='CIF/NIF')
    contact_person = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30)
    address = forms.CharField(max_length=255)
    province = forms.CharField(max_length=120)
    city = forms.CharField(max_length=120, required=False)
    postal_code = forms.CharField(max_length=20, required=False)
    company_type = forms.ChoiceField(choices=Distributor.CompanyType.choices)
    services_offered = forms.CharField(max_length=255, required=False)

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email'].lower()
        user.email = self.cleaned_data['email'].lower()
        user.first_name = self.cleaned_data['contact_person']
        if commit:
            user.save()
            Distributor.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                cif=self.cleaned_data['cif'],
                contact_person=self.cleaned_data['contact_person'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
                province=self.cleaned_data['province'],
                city=self.cleaned_data['city'],
                postal_code=self.cleaned_data['postal_code'],
                company_type=self.cleaned_data['company_type'],
                services_offered=self.cleaned_data['services_offered'],
                status=Distributor.Status.PENDING,
            )
        return user