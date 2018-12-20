from django.shortcuts import render
from django.http import HttpResponse

from .dataset import hangout_functions as hgf
import pandas as pd
import numpy as np
import json

# Create your views here.
def index(request):
	# len(hgf.get_discussions())
	# hg_events = hgf.load_conv_events()
	# hgf.get_types_actions(hg_events, nb=False)
	# [hgf.count_actions_in(evts) for evts in hg_events]
	# hgf.count_actions()

	# hgf.count_actions(msg_type='REGULAR_CHAT_MESSAGE')

	# [hgf.count_actions_in(evts, msg_type='REGULAR_CHAT_MESSAGE') for evts in hgf.load_conv_events()]

	# C = hgf.load_conversations()  

	# participants = hgf.get_participants(C, debug=True)
	# participants.columns
	# participants.groupby('convID').agg(len).pID.values

	# participants.pName.unique()[:4]

	# print(hgf.get_msgs(hg_events).columns)

	E = hgf.load_conv_events()
	allmessages = hgf.get_msgs(E, len_text=True, msg_type='REGULAR_CHAT_MESSAGE')
	# print(allmessages)
	conv = allmessages.loc[:,['ID', 'timestamp']].copy()
	conv.loc[:,'timestamp'] = pd.to_numeric(allmessages.timestamp)
	conv.loc[:,'timestamp2'] = allmessages.timestamp
	gbt= conv.groupby('ID')  # ID c'est ID des conv
	n = len(gbt)
	gbt_dict = gbt['timestamp'].apply(list).to_dict()
	# for f,g in gbt_dict.items():
	# 	print()

	# print('fuck')
	return render(request,'index.html',{'gbt':json.dumps(gbt_dict),'nombre':n})