from django import forms
from .models import Youngling


class YounglingForm(forms.ModelForm):
    class Meta:
        model = Youngling
        exclude = ['teacher']
        widgets = {
            'birthday': forms.DateInput(format('%Y/%m/%d'), attrs={'placeholder': 'Электронный адрес',}),
        }


# class JediChooseForm(forms.Form)
#     j_ch_field = forms.ChoiceField(required=True, widget=forms.Select, choices=)
#     # class Meta:
#     #     model = Jedi
#     #     fields = ['']


# class AnsweringForm(forms.ModelForm):
#
#     class Meta:
#         model = QAns
#         fields = ['answer']
