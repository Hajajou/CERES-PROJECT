#-*-coding:utf-8-*-
import json
import pandas as pd
import logging

import json
import os

hangoutspath = os.path.dirname(os.path.abspath(__file__))

# check These/Models/models_UML.org"""
def len_msgsll(df):
    """compte la longeur totale des messages"""
    return df.loc[:, 'len_text'].sum()


def duree_conv(s):
    """calcule la durée d'une conversation"""
    older, newer = s.sort_values().iloc[[0, -1]]
    return (newer - older)


def simplify_names(s):
    """Regroupe les noms de la série s en une chaine """
    rep = ''
    for x in s:
        if not x in rep:
            rep += x
    return rep


def concat_text(sgts, len_text=False):
    """given a sgements return the text in one piece, including links
mettre len_text à vrai pour avoir la longueur du text.  retourne alors un tuple (content, longueur)"""
    # ajouter attachement gestion
    rep = ''
    longueur = 0
    for sgt in sgts:
        if sgt['type'] == 'TEXT':
            rep += sgt['text']
            longueur += len(sgt['text'])
        elif sgt['type'] == 'LINE_BREAK':
            rep += '\n'
        elif sgt['type'] == 'LINK':
            rep += ('(voir lien: %s' % sgt['text'])
    if len_text :
        return (rep, longueur)
    return (rep,)


def load_conversations(fname='hangouts.json'):
    """Load le fichier des conversations à partir du json de hangouts
    Retourne une liste des conversations"""
    fname = 'hangouts.json'  if fname is None else fname
    with open(os.path.join(hangoutspath, 'hangouts.json'), 'r') as f:
        raw_cvs = json.load(f)['conversations']

    list_cvs = [conv['conversation']['conversation'] for conv in raw_cvs]
    # renvoie raw_cvs is list_cvs is None
    return list_cvs


def get_discussions(fname='hangouts.json'):
    """Charges les conversations depuis un fichiers de sauvegarde."""
    with open(os.path.join(hangoutspath, 'hangouts.json'), 'r') as f:
        dsc = json.load(f)['conversations']
    return dsc


def load_conv_events(fname='hangouts.json'):
    """ load the events containing the messages from the json
    into a dataframe"""
    fname = 'hangouts.json'  if fname is None else fname
    with open(os.path.join(hangoutspath, 'hangouts.json'), 'r') as f:
        conversations = json.load(f)['conversations']

    L = list()
    for i in range(len(conversations)):
        L.append(conversations[i]['events'])

    conv_events = pd.Series(data=L, index=range(len(conversations)))
    #        conv_events.iloc[i] = conversations[i]['events']
    return conv_events


def nb_type_par_conv(conversations, msg_type='REGULAR_CHAT_MESSAGE', seuil=4):
    # les nombre d'events par conversation
    M = list()
    for i in range(len(conversations)):
        evts = conversations[i]
        k = 0
        for y in range(len(evts)):
            e = evts[y]
            if e['event_type'] == msg_type:
                k += 1
        if k > seuil:
            M.append(
                ((i, k))
            )
    M.sort(key=lambda x: x[1], reverse=True)
    return M


def get_types_actions(conv_events, nb=True):
    S = set()
    for i in range(len(conv_events)):
        for e in conv_events[i]:
            S.add((e['event_type'], i)) if nb is True else S.add(e['event_type'])
    L = list(S)
    L.sort()
    return L


def longueur_message(conv_events, seuil=4):
    L = list()
    for i in range(len(conv_events)):
        evts = conv_events[i]
        for y in range(len(evts)):
            e = evts[y]
            if e['event_type'] == 'REGULAR_CHAT_MESSAGE':
                try:
                    sgts = e['chat_message']['message_content']['segment']
                    if len(sgts) > seuil:
                        L.append(
                            (i, y, len(sgts))
                        )
                except KeyError:
                    pass
    L.sort(key=lambda x: x[2], reverse=True)
    return L


def count_actions(fname=None, msg_type=None):
    """Count le nombre total d'actions"""
    k = 0
    for evts in load_conv_events(fname):
        for e in evts:
            if e['event_type'] == msg_type or msg_type is None:
                k += 1
    return k


def get_msgs(conv_events, msg_type=None, len_text=False):
    """Retourne une df avec le contenu d'un message, son id, son auteur et le time stamp
    Ce limite aux message d'une même conversation."""

    def membership_change(mbc):
        """Given a membership change instance, renvoie une string avec l'action la raison et le nom des touchés"""
        members = list()
        for m in mbc['participant_id']:
            members.append(m['gaia_id'])
        return '%s %s %s' % (members, mbc['leave_reason'], mbc['type'])

    #### mains loops ####
    cols = ['ID', 'debugID', 'convID', 'senderID', 'timestamp', 'evtID', 'evtType', 'content']
    cols += ['len_text'] if len_text else []  # ajoute une colonne pour la longueur message
    D = pd.DataFrame(data=None, columns=cols, index=range(count_actions()))
    k = 0
    for i in range(len(conv_events)):  # on keep track des indices
        evts = conv_events[i]
        for y in range(len(evts)):  
            e = evts[y]
            D.iloc[k].loc['ID'] = 'conv' + str(i)
            D.iloc[k].loc['debugID'] = (i, y)
            D.iloc[k].loc['convID'] = e['conversation_id']['id']
            D.iloc[k].loc['senderID'] = e['sender_id']['gaia_id']
            D.iloc[k].loc['timestamp'] = e['timestamp']
            D.iloc[k].loc['evtID'] = e['event_id']
            D.iloc[k].loc['evtType'] = e['event_type']
            if e['event_type'] in ['ADD_USER', 'REMOVE_USER']:
                mbc = e['membership_change']
                D.iloc[k].loc['content'] = membership_change(mbc)
            if e['event_type'] == 'HANGOUT_EVENT':
                D.iloc[k].loc['content'] = e['hangout_event']['event_type']
            if e['event_type'] == 'REGULAR_CHAT_MESSAGE':
                msg_keys = e['chat_message']['message_content'].keys()
                try:
                    if 'segment' in msg_keys:
                        sgts = e['chat_message']['message_content']['segment']
                        D.iloc[k].loc['content'] = concat_text(sgts)[0]
                        if len_text:
                            D.iloc[k].loc['len_text'] = concat_text(sgts, True)[1]
                    if 'attachment' in msg_keys:
                        D.iloc[k].loc['content'] = str(D.iloc[k].loc['content']) + ' + Pièce jointe.'
                except KeyError:
                    sgts = e['chat_message']['message_content']['segment']
                    pass
            if e['event_type'] == 'RENAME_CONVERSATION':
                new_name = e['conversation_rename']['new_name']
                old_name = e['conversation_rename']['old_name']
                D.iloc[k].loc['content'] = 'old %s -> new %s' % (old_name, new_name)
                pass
            k += 1
    # import ipdb
    # ipdb.set_trace()
    D = D.dropna(how='all')

    if msg_type is not None:
        D = D[(D.evtType == msg_type)]

    D.loc[:, 'timestamp'] = (D.loc[:, 'timestamp']
                             .apply(lambda x: pd.Timestamp(int(x), unit='us').round('s')))
    
    return D


def get_participants(conversations, debug=False):
    """Renvois tous les participants de toutes les conversations"""
    Ds = list()
    for i in range(len(conversations)):
        dsc = conversations[i]
        if debug:
            Ds.append(get_participants_in(dsc, debug=i))
        else:
            Ds.append(get_participants_in(dsc))
    return pd.concat(Ds)


def get_participants_in(dsc, json=False, debug=None):
    ID, NAME, STATUS = [], [], []
    convID = dsc['id']['id']
    convType = dsc['type']
    y = 0
    for p in dsc['participant_data']:
        ID.append(p['id']['gaia_id'])
        STATUS.append(p['new_invitation_status'])
        NAME.append(p['fallback_name'])
        y += 1

    if debug is not None:
        D = pd.DataFrame(data={'pName': NAME, 'pStatus': STATUS,
                               'pID': ID, 'convID': convID, 'convType': convType,
                               'debugID': '%s_%s' % (debug, y)})  # need to be string
    else:
        D = pd.DataFrame(data={'pName': NAME, 'pStatus': STATUS,
                               'pID': ID, 'convID': convID, 'convType': convType})
    if json:
        D = D.to_json(orient='records')

    return D


def count_actions_in(evts, msg_type=None):
    """given event of a conversation, return the number of event of specified type"""
    cpt = 0
    try:
        for e in evts:
            if (msg_type == e['event_type']):
                cpt += 1
            elif msg_type is None:
                cpt += 1
    except Exception as ex:
        print('%s__ e=%s' % (ex.__repr__(), e))
    return cpt



