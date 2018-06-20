from django import forms
from .models import Youngling
import datetime


year = datetime.date.today().year


class YounglingForm(forms.ModelForm):
    """
    Form for new youngling.
    Was made by the Youngling model (know more .models.Youngling).
    """
    class Meta:
        model = Youngling
        exclude = ['teacher']
        widgets = {
            'birthday': forms.SelectDateWidget(years=range(year, year-100, -1))
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
