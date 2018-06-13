from django import forms
from .models import Youngling, Jedi


class YounglingForm(forms.ModelForm):
    class Meta:
        model = Youngling
        exclude = ['teacher']


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
