from django.shortcuts import render
from django.http import HttpResponse

from .dataset import hangout_functions as hgf
import pandas as pd
import numpy as np
import json
from django.db import connection

# Create your views here.
def index(request):
	E = hgf.load_conv_events()
	allmessages = hgf.get_msgs(E, len_text=True, msg_type='REGULAR_CHAT_MESSAGE')
	# print(allmessages)
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
	user = 'tdelille'
	# with connection.cursor() as cursor:
		# cursor.execute("SELECT * FROM transition")
		# row = cursor.fetchall()
	query = 'select * from transition'
	df_traceforum = pd.read_sql(query, connection)
	# to do nb d'utilisateur qui cite le message

	# A = df_traceforum.groupby('Utilisateur')
	#Nombre de message cité par un utilisateur donné
	df2 = df_traceforum.copy()
	B = df2[df2['Titre'].str.contains("Citer un message")].groupby('Utilisateur').size().reset_index(name='nb_message_cite')
	print(dict(zip(B['Utilisateur'],B['nb_message_cite'])))
	nb_message_cite = df2[ df2['Titre'].str.contains("Citer un message") & df2['Utilisateur'].str.contains(user)].shape[0]
	


	
	return render(request,'traceforum.html',{'historique':json.dumps(dict(zip(B['Utilisateur'],B['nb_message_cite'])))})



