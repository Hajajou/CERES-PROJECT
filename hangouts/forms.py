from django import forms
from django.db import connection
import pandas as pd
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class UserMultiSelectForm(forms.Form):
	query = "select * from transition"
	df_traceforum = pd.read_sql(query, connection)
	CHOICES_USERS = [(x,x) for x in set(df_traceforum['Utilisateur'])]
	CHOICES_ACTIVITY = [(x,x) for x in set(df_traceforum['Titre'])]
	users = forms.MultipleChoiceField(required=False,choices=CHOICES_USERS, label="Users",widget=forms.SelectMultiple(attrs={'class':'form-control selectpicker','id':'form_users'}))
	activities = forms.MultipleChoiceField(required=False, choices=CHOICES_ACTIVITY, label="Activities", widget=forms.SelectMultiple(attrs={'class':'form-control selectpicker','id':'form_activities'}))

