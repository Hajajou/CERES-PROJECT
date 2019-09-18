from django.shortcuts import render
from django.http import HttpResponse

from .dataset import hangout_functions as hgf
import pandas as pd
import numpy as np
import json
from django.db import connection
from .forms import *

# Create your views here.
def index(request):
	E = hgf.load_conv_events()
	allmessages = hgf.get_msgs(E, len_text=True, msg_type='REGULAR_CHAT_MESSAGE')
	print(allmessages)
	conv = allmessages.loc[:,['ID', 'timestamp']].copy()
	conv.loc[:,'timestamp'] = pd.to_numeric(allmessages.timestamp)
	conv.loc[:,'timestamp2'] = allmessages.timestamp
	gbt= conv.groupby('ID')  # ID c'est ID des conv
	n = len(gbt)
	gbt_dict = gbt['timestamp'].apply(list).to_dict()

	lAt  = allmessages.groupby('ID')['len_text'].sum()
	# print(lAt.to_dict())
	
	# tAt  = allmessages.groupby('ID').agg([hgf.duree_conv, min, max]).drop([('len_text', 'duree_conv')], axis=1)
	
	return render(request,'index.html',{'gbt':json.dumps(gbt_dict),'nombre':n,'js_len_message':json.dumps(lAt.to_dict())})

def traceforum(request):
	users_l = []
	activities_l = []
	if request.method == 'POST':
		print("ok post")
		form = UserMultiSelectForm(request.POST)
		if form.is_valid():
			users_l = form.cleaned_data.get('users')
			activities_l = form.cleaned_data.get('activities')
			# do something with your results
			
	else:
		form = UserMultiSelectForm()

	# with connection.cursor() as cursor:
		# cursor.execute("SELECT * FROM transition")
		# row = cursor.fetchall()
	query = 'select * from transition'
	df_traceforum = pd.read_sql(query, connection)
	df_traceforum.loc[:,'Date'] = pd.to_datetime(df_traceforum.Date.astype(str)+' '+df_traceforum.Heure.astype(str))

	# to do nb d'utilisateur qui cite le message
	# A = df_traceforum.groupby('Utilisateur')
	#Nombre de message cité par un utilisateur donné

	df2 = df_traceforum.copy()
	if len(users_l) > 0:
		df2 = df2[df2["Utilisateur"].isin(users_l)]
	if len(activities_l) >0:
		df2 = df2[df2["Titre"].isin(activities_l)]


	B = df2[df2['Titre'].str.contains("Citer un message")].groupby('Utilisateur').size().reset_index(name='nb_message_cite')
	# print(dict(zip(B['Utilisateur'],B['nb_message_cite'])))
	users = list(set(df2['Utilisateur']))

	# nb_message_cite = df2[ df2['Titre'].str.contains("Citer un message") & df2['Utilisateur'].str.contains(user)].shape[0]
	# historique_message_cite = df2[df2['Titre'].str.contains("Citer un message")].sort_values(by=['Utilisateur','Date'])
	# historique_message_cite = historique_message_cite.drop(['Commentaire','Attribut','IDTran','Heure','Titre','Delai','RefTran'],axis=1)

	all_activities = df2.sort_values(by=['Utilisateur','Date'])
	activities = list(set(all_activities['Titre']))
	# dict_historique_message = dict()
	# for user in users:
	# 	dict_historique_message.update(zip(user,historique_message_cite[historique_message_cite['Utilisateur'] == user]))
	# print(historique_message_cite['Date'].first().__class__)
	# print(dict_historique_message)
	# historique_message_cite['time'] = historique_message_cite[['Date','Heure']].apply(lambda x: ' '.join(x.strftime('%Y-%m-%d')),axis=1)
	# print(historique_message_cite['time'])
	# historique_message_cite[['Date','Heure']].apply(lambda x: print(x.__class__),axis=1)

	users_dict = {e:users.index(e) for e in users }
	activities_dict = {e:activities.index(e) for e in activities}
	# print(users_dict)
	# print(historique_message_cite['Utilisateur'].apply(lambda x: users_dict.get(x)))

	return render(request,'traceforum.html',{'historique':json.dumps(dict(zip(B['Utilisateur'],B['nb_message_cite']))),
		'dataMessageCite':list(zip(all_activities['Utilisateur'],all_activities['Date'], all_activities['Titre'].apply(lambda x: activities_dict.get(x)))),
		'usersDict':users_dict,
		'activitiesDict':activities_dict,
		'form':form,
		})



