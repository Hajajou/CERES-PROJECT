#Connexion au serveur
import mysql.connector
from datetime import timedelta

conn = mysql.connector.connect(host="localhost",user="root",password="GDX47OYY", database="ceres")
print(conn)
cursor = conn.cursor()
#conn.close()

cursor.execute("""SELECT IDAct, Titre, TypeAct,IDCat FROM activite""")
rows = cursor.fetchall()
for row in rows:
    print('{0} : {1} - {2} - {3}'.format(row[0], row[1], row[2], row[3]))

print("------------------")


#utilisateur avction ->connexion
cursor.execute("""SELECT distinct(Utilisateur), Titre FROM transition WHERE Titre = 'Connexion'""")
ligne = cursor.fetchall()
for ligne in ligne:
    print('{0} : {1}'.format(ligne[0], ligne[1]))

print("------------------")


#Nombre de message initié par un utilisateur donné
cursor.execute("SELECT  Utilisateur, count(Utilisateur) FROM transition WHERE Titre = 'Poster un nouveau message' AND Utilisateur = 'tdelille'")
ligne = cursor.fetchall()
for ligne in ligne:
    print('{0} a initié {1} messages'.format(ligne[0],ligne[1]))

#Nombre de message répondu par un utilisateur donné
cursor.execute("SELECT  Utilisateur, count(Utilisateur) FROM transition WHERE Titre = 'Répondre à un message' AND Utilisateur = 'tdelille' ")
ligne = cursor.fetchall()
for ligne in ligne:
    print('{0} a répondu à {1} messages'.format(ligne[0],ligne[1]))

#Nombre de message cité par un utilisateur donné
cursor.execute("SELECT  Utilisateur, count(Utilisateur) FROM transition WHERE Titre = 'Citer un message' AND Utilisateur = 'tdelille' ")
ligne = cursor.fetchall()
for ligne in ligne:
    print('{0} a cité {1} messages'.format(ligne[0],ligne[1]))



#Nombre de message totaux par un utilisateur donné
cursor.execute("""SELECT  Utilisateur, count(Utilisateur) FROM transition WHERE Utilisateur = 'tdelille' AND Titre IN ('Répondre à un message', 'Poster un nouveau message', 'Citer un message')  """)
ligne = cursor.fetchall()
for ligne in ligne:
    print('{0} a ecrit au total {1} messages'.format(ligne[0],ligne[1]))

#  select * from transition where Utilisateur='" + name + "' and Date >= '" + date11 + "' and Date <= '" + date22 + "'"

print("------------------")

#Nombre de message posté par un utilisateur donné à une date donné
cursor.execute("SELECT Utilisateur, count(Utilisateur), Date FROM transition WHERE Date between '2009-02-12' AND '2009-12-12' AND Utilisateur = 'mmay' AND Titre IN ('Répondre à un message', 'Poster un nouveau message', 'Citer un message') group by Date")
ligne = cursor.fetchall()
for ligne in ligne:
    print('{0} a écrit {1} messages le {2}'.format(ligne[0],ligne[1], ligne[2]))

print("----------")

#Nombre de connexion effectué par un utilisateur par JOUR donné à une date donné
cursor.execute("SELECT Utilisateur, count(Utilisateur), Date FROM transition WHERE Date between '2009-02-12' AND '2009-12-12' AND Utilisateur = 'mmay' AND Titre IN ('Connexion') group by Date")
ligne = cursor.fetchall()
for ligne in ligne:
    print('{0} était connecté {1} fois le {2}'.format(ligne[0],ligne[1], ligne[2]))

print("----------")

#Nombre de connexion effectué par HEURE par un utilisateur donné à un jour donné
cursor.execute("SELECT Utilisateur, count(Utilisateur), Heure FROM transition WHERE Date = '2009-02-13' AND Utilisateur = 'mmay' AND Titre IN ('Connexion') group by Heure")
ligne = cursor.fetchall()
print('Le 2009-02-13:')
for ligne in ligne:
    print('{0} connecté {1} fois à {2}'.format(ligne[0],ligne[1], ligne[2]))


#Heure de connexion from vue_sebastien
text = ("Connexion",)
cursor.execute("select Utilisateur from vue_sebastien where Titre = %s  ",(text))
ligne = cursor.fetchone()
print(ligne)
conn.close()


"""
#Heure de connexion from vue_sebastien
heure = ("13:31:59",)
cursor.execute("select Titre from vue_sebastien where Heure = %s ",(heure))
ligne = cursor.fetchone()
print(ligne)
"""


#cursor.execute("SELECT nom FROM proprietaire where nom like ?", ('%' + text + '%',))

#cursor.execute('SELECT * FROM "maTable" WHERE "Nom" LIKE \'%' + mavariable + '%\'');




#curseur.execute("""SELECT ANNIV_Nom FROM ANNIV WHERE ANNIV_Mois = ? AND ANNIV_JOUR = ?""", (Today_Mois,Today_Jour))



"""
def convert_timedelta(ligne):
    days, seconds = ligne.days, ligne.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds
td = datetime.timedelta(2, 7743, 12345)
hours, minutes, seconds = convert_timedelta(td)
print('{} minutes, {} hours'.format(minutes, hours))
def convert_timedelta(ligne):
    days, seconds = ligne.days, ligne.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return days, hours, minutes, seconds
    print (' {} minutes, {} hours, {} days'.format(minutes, hours, days))
"""



"""
#Utilisateur, nombre de fois qu'il affiche un message
SELECT Utilisateur,count(Utilisateur),Titre
FROM transition
WHERE Titre in ( "Afficher le contenu d'un message", "Répondre à un message")
Group by Titre
;

"""
def getUsername():
        username = 'tdelille'
        result = cursor.execute("select * from transition where Utilisateur ='" + username +"'")
        return result


""""

#Utilisateur, nombre de fois qu'il affiche un message
SELECT Utilisateur,count(Utilisateur),Titre
FROM transition
WHERE Titre= "Afficher le contenu d'un message"
Group by Utilisateur
;

SELECT count(Utilisateur)
FROM transition
WHERE Date between '2009-02-12' AND '2009-12-12'
AND Utilisateur = 'mmay'
AND Titre IN ('Répondre à un message', 'Poster un nouveau message', 'Citer un message')

SELECT count(Utilisateur)
FROM transition
WHERE Date between '2009-02-12' AND '2009-12-12'
AND Utilisateur = 'mmay'
AND Titre IN ('Répondre à un message', 'Poster un nouveau message', 'Citer un message');


getUsername()












from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base ()


#Base = sqlalchemy.ext.declarative.declarative_base()
#Base.metadata
#MetaData(None)

metadata = MetaData()
metadata.reflect(bind=engine)
for table in metadata.sorted_tables:
    print(table)


for table_name in engine.table_names():
    print(table_name)


class User ( Base ):
   __tablename__ = 'users'

   id = Column ( Integer , primary_key = True )
   name = Column ( String )
   fullname = Column ( String )
   password = Column ( String )

   def __repr__ ( self ):
      return "<User(name=' %s ', fullname=' %s ', password=' %s ')>" % (
                           self . name , self . fullname , self . password )


print(User . __table__)


# cross table for user-forum
favorite_series = db.Table('transition',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('forum_id', db.Integer, db.ForeignKey('forum.id'))
)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    favorite_series = db.relationship('forum', secondary=favorite_series,
     backref=db.backref('users', lazy='dynamic'))


class Series(db.Model):
    __tablename__ = 'series'
    id = db.Column(db.Integer, primary_key=True)

class Episode(db.Model):
    __tablename__ = 'episode'
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    series = db.relationship('Series',
     backref=db.backref('episodes', lazy='dynamic'))
"""
