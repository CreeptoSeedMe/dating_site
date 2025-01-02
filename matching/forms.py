from django import forms
from users.models import Profile

class SearchFiltersForm(forms.Form):
    min_age = forms.IntegerField(
        min_value=18,
        max_value=100,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    max_age = forms.IntegerField(
        min_value=18,
        max_value=100,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=[('', 'Any')] + Profile.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    distance = forms.IntegerField(
        min_value=1,
        max_value=500,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    has_photo = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    online_now = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    interests = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter interests (comma separated)'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        min_age = cleaned_data.get('min_age')
        max_age = cleaned_data.get('max_age')

        if min_age and max_age and min_age > max_age:
            raise forms.ValidationError("Minimum age cannot be greater than maximum age")

        return cleaned_data
