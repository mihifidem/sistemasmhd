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


class TechnicianPortalAccessForm(forms.ModelForm):
    technician_portal_password = forms.CharField(
        required=False,
        min_length=6,
        label='Contraseña acceso técnicos',
        widget=forms.PasswordInput(render_value=False),
        help_text='Mínimo 6 caracteres. Déjalo vacío si no quieres cambiarla.',
    )
    technician_portal_password_confirm = forms.CharField(
        required=False,
        label='Confirmar contraseña técnicos',
        widget=forms.PasswordInput(render_value=False),
    )

    class Meta:
        model = Distributor
        fields = ('technician_portal_username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['technician_portal_username'].required = False

    def clean_technician_portal_username(self):
        username = (self.cleaned_data.get('technician_portal_username') or '').strip().lower()
        if not username:
            return ''

        user_model = get_user_model()
        if user_model.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Este usuario ya existe en la plataforma.')

        qs = Distributor.objects.filter(technician_portal_username__iexact=username)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Este usuario ya está asignado a otro distribuidor.')

        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('technician_portal_username') or ''
        password = cleaned_data.get('technician_portal_password') or ''
        password_confirm = cleaned_data.get('technician_portal_password_confirm') or ''

        if password and not password_confirm:
            self.add_error('technician_portal_password_confirm', 'Confirma la contraseña para técnicos.')
        if password_confirm and not password:
            self.add_error('technician_portal_password', 'Introduce la contraseña para técnicos.')
        if password and password_confirm and password != password_confirm:
            self.add_error('technician_portal_password_confirm', 'Las contraseñas no coinciden.')

        if username and not (password or (self.instance and self.instance.technician_portal_password_hash)):
            self.add_error('technician_portal_password', 'Define una contraseña inicial para habilitar el acceso técnico.')

        if not username:
            cleaned_data['technician_portal_password'] = ''
            cleaned_data['technician_portal_password_confirm'] = ''

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        username = (self.cleaned_data.get('technician_portal_username') or '').strip().lower()
        password = self.cleaned_data.get('technician_portal_password') or ''

        if not username:
            instance.technician_portal_username = None
            instance.technician_portal_password_hash = ''
        else:
            instance.technician_portal_username = username
            if password:
                instance.set_technician_password(password)

        if commit:
            instance.save()
        return instance


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