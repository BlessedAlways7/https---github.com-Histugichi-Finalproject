from flask import Flask, render_template, request, session, url_for, redirect
import bcrypt
import os
from dotenv import load_dotenv
from users.user_dao import UserDao
from users.user import User
from evenements.evenement import Evenement
from evenements.evenement_dao import EvenementDao
from paiements.paiement import Paiement
from paiements.paiement_dao import PaiementDao
from reservations.reservation_dao import ReservationDao
from reservations.reservation import Reservation
from reservations.statut import ReservationStatut

load_dotenv()
app = Flask(__name__,)
app.secret_key = os.environ.get('SECRET_KEY')
db_user=os.environ.get('DB_USER')
db_host=os.environ.get('DB_HOST')
db_password=os.environ.get('DB_PASSWORD')
db_database=os.environ.get('DB_DATABASE')

salt = bcrypt.gensalt(rounds=12)

#Afficher la page home.
@app.route('/')
def home():
    return render_template('home.html')

#Affiche la page de défaut admin.
@app.route('/admin')
def admin():
    return render_template('admin.html')

#Afficher la page d'accueil.
@app.route('/accueil')
def accueil():
    return render_template('accueil.html')

# Permet à l'utilisateur ou l'administrateur de se connecter à son compte.
@app.route('/login',methods= ['POST', 'GET'])
def login():
    req = request.form
    message =None
    user = None

    if request.method == "POST":
        username = req ['username']
        password = req ['password']     
        password = password.encode()
        if username=="" or password=="":
            message="error"
        else:
            # Chercher hashed password de la base de donnée base sur username
            message, user = UserDao.get_one(username)
            hashed_password_bd = user[2]
         
            if hashed_password_bd:
                hashed_password_bd = hashed_password_bd.encode()
                # Verifier si le mot de passe est correct
            if bcrypt.checkpw(password, hashed_password_bd):
                    message = 'success'
                   
                    if user:
                        session['nom_complet']=user[0] #On met le nom complet dans notre variable de session
                        session['username']=user[1] # On met le username dans notre variable de session
                        session['id_user']=user[5] 
                        session['email']=user[3]
                        if user[4] ==1: #verifier si c'est un admin, sinon rediriger vers la page de reservation
                            session["is_admin"]=user[4]
                            return redirect(url_for('admin'))
                        else:
                            return redirect(url_for("accueil"))  
        print(message)
    return render_template('login.html', message=message, user=None)

# Permet a un utilisateur de se se créer un compte.
@app.route('/registrer',methods= ['POST', 'GET'])
def registrer():
    req = request.form
    message =None
    user= None

    if request.method == "POST":
        nom_complet = req ['nom_complet']
        username = req ['username']
        password = req ['password']
        email = req ['email']
        #Hash password
        is_admin= 0
        password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, salt)
        
        if nom_complet=="" or username=="" or password=="" or email=='' :
            message="error"
        else:
            user = User(nom_complet, username, hashed_password,email, is_admin)
            message = UserDao.create(user)
        print(message)
    return render_template('user/registrer.html', message=message, user=user)

# Permet d'afficher les évènements.
@app.route('/evenement')
def evenement():
    message, evenements=EvenementDao.get_all()
    return render_template('event/evenement.html', message=message, evenements=evenements)

#Permet d'afficher les places (total,réservées, disponibles) selon l'évènement.
@app.route('/places',methods= ['POST','GET'])
def places():

    event_info=None
    id_evenement= EvenementDao.get_all_id()
    if request.method == "GET":
        nom = request.args.get('nom')
        id_evenement = request.args.get('id_evenement')
        
        if id_evenement and nom:
            event_info=EvenementDao.get_event_info_with_reserved_places(id_evenement, nom)
            if event_info:
                total_seat=int(event_info[5])
                return render_template('places.html', event_info=event_info, total_seat=total_seat)
            else:
                return 'Event information not found.' 
   
    return render_template('places.html',event_info=event_info)

#Permet à l'administrateur d'ajouter un évènement.
@app.route('/add_event', methods= ['POST', 'GET'])
def add_event():
    if "is_admin" not in session:
        return redirect(url_for('login'))
    message=None
    evenement=None

    if request.method == "POST":
        nom = request.form ['nom']
        date = request.form ['date']
        emplacement = request.form ['emplacement']
        total_seat = request.form ['total_seat']
        prix = request.form ['prix']
        id_evenement = request.form ['id']
        
        if nom=="" or date=="" or emplacement=="" or total_seat=="" or prix=="" or id_evenement=="":
            message="error"
        else:
            evenement = Evenement(nom,date,emplacement,total_seat,prix,id_evenement)
            message = EvenementDao.create_evenement(evenement)
        print(message)
    return render_template('event/add_event.html', message=message, evenement=evenement)

#Permet à l'administrateur de voir les évènements.
@app.route('/evenement_admin')
def evenement_admin():
    message, evenements=EvenementDao.get_all()
    return render_template('admin/evenement_admin.html', message=message, evenements=evenements)

#Permet à l'administrateur de modifier les information de l'évènement selon l'id de l'évènement.
@app.route('/modify_event', methods= ['POST', 'GET'])
def modify_event():
    if "is_admin" not in session:
        return redirect(url_for('login'))
    message=None
    evenement=None
    id_evenement = request.args.get('id_evenement')

    if id_evenement:
        evenement = EvenementDao.recuperer_evenement_par_id(id_evenement)
    
    if request.method == "POST":
        nom= request.form['nom']
        date = request.form ['date']
        emplacement = request.form ['emplacement']
        total_seat= request.form ['total_seat']
        prix = request.form['prix']  
        
       
        if nom=="" or date=="" or emplacement=="" or total_seat=="" or prix=="":
            message="error"
            return render_template('reservation/modify_event.html',message=message, reservation=None)
        id_evenement = EvenementDao.get_evenement_id_by_name(nom)
        if id_evenement:
            nouveau_evenement=Evenement(
            id_evenement=id_evenement,
            nom=nom,
            date=date,
            emplacement=emplacement,
            total_seat=total_seat,
            prix=prix
            )
            message =EvenementDao.modifier_evenement(id_evenement,nouveau_evenement)    
            if message=='success':
                message="Modification successful"
                session['id_evenement']=id_evenement
                return redirect(url_for('evenement_admin', id_evenement=id_evenement))
            else:
                message = "Failed to modify event."
        else:
            message = "Event not found."
    return render_template('event/modify_event.html', message=message, evenement=evenement)

#Permet à l'administrateur de supprimer un évènement.
@app.route('/delete_event', methods= ['POST', 'GET'])
def delete_event():
    if "is_admin" not in session:
        return redirect(url_for('login'))
    message=None
    evenement=None

    if request.method == "POST":
        nom= request.form['nom']
        date = request.form ['date']
        emplacement = request.form ['emplacement']
        total_seat=request.form['total_seat']
        prix = request.form['prix']
        id_evenement = request.form['id_evenement']

        if nom=="" or date=="" or emplacement=="" or total_seat==""or prix=="" or id_evenement=="":
            message="error"
        else:
            evenement = Evenement(nom, date,emplacement,total_seat,prix,id_evenement)
            message = EvenementDao.supprimer_evenement(id_evenement)
        print(message)
    return render_template('event/delete_event.html', message=message, evenement=evenement)

#Permet à l'administrateur d'afficher les réservations.
@app.route('/liste_reservation')
def liste_reservation():
    if "is_admin" not in session:
        return redirect(url_for('login'))
    message, reservations=ReservationDao.get_all()
    return render_template('reservation/liste_reservation.html', message=message, reservations=reservations)

#Permet à l'utilisateur de supprimer sa réservation.
@app.route('/delete_reservation', methods= ['POST', 'GET'])
def delete_reservation():
    if 'username' not in session and "is_admin" not in session:
        return redirect(url_for('login'))
    message=None
    reservation=None
    
    if request.method == 'POST':
        id_evenement=request.form['id_evenement']
        id_user= request.form['id_user']
        id_reservation =request.form ['id_reservation']  
 
        if  id_evenement=="" or id_user=="" or id_reservation=="":
            message="error"
        else:           
            message=ReservationDao.annuler_reservation(id_evenement,id_user,id_reservation)
        print(message)
    return render_template('reservation/delete_reservation.html', message=message, reservation=reservation)

#Permet à l'administrateur de voir le statut des réservations.
@app.route('/statut')
def statut():
    if "is_admin" not in session:
        return redirect(url_for('login'))
    reservations = ReservationDao.afficher_statut_reservations()
    return render_template('reservation/statut.html',  reservations=reservations)

#Permet de sortir de la session.
@app.route("/logout")
def logout():
    session.clear() # On vide la session
    return redirect(url_for('login'))

#Permet à l'utilisateur de faire une réservation.
@app.route('/reservations', methods=['POST', 'GET'])
def reservations():
    if 'username' not in session and "is_admin" not in session:
        return redirect(url_for('login'))
    
    message=None
    reservation=None
    id_evenement = request.args.get('id_evenement')
    id_user=session['id_user']
    
    if request.method == 'POST':
        nom = request.form['nom']
        date = request.form['date']
        place = request.form['place']
        id_evenement = EvenementDao.get_evenement_id_by_name(nom)

        if nom=="" or date=="" or place=="" :
            message="error"
            return render_template('reservation/reservations.html',message=message, reservation=None)
    
        elif id_evenement is None:
            message = "L'événement sélectionné n'existe pas."
        else:
            statut = ReservationStatut.EN_ATTENTE.value 
            reservation = Reservation(nom, date, place,id_evenement,id_user,statut)
            (success, message, id_reservation) = ReservationDao.reserver_place(reservation)
            
            if success:
                session['id_evenement']=id_evenement
                session['id_reservation']=id_reservation
                return redirect(url_for('paiement'))    
        if id_evenement:   
            pass
        else:
            message= "Une erreur s'est produite lors de la réservation. Veuillez réessayer."
    return render_template('reservation/reservations.html',message=message, reservation=reservation)

#Permet à l'utilisateur de voir ses réservations.
@app.route('/historique')
def historique():
    if 'username' not in session and "is_admin" not in session:
        return redirect(url_for('login'))   
    id_user = session.get('id_user')    
    reservations = ReservationDao.filtrer_reservations_id_user(id_user)    
    return render_template('reservation/historique.html', reservations=reservations)

#Permet de confirmer une réservation.
@app.route('/confirmation')
def confirmation():
    id_reservation= session['id_reservation']
    id_evenement=session['id_evenement']
    nom_complet=session['nom_complet']
    email= session['email']
    evenement=EvenementDao.recuperer_evenement_par_id(id_evenement)
    message=ReservationDao.confirmer_reservation(id_reservation)
    if message== 'success':
        return redirect(url_for('reservation'))
    else:
        return render_template('confirmation.html',message=message, evenement=evenement, nom_complet=nom_complet,
             email=email,id_evenement=id_evenement, id_reservation=id_reservation)

#Permet à l'administrateur de voir la liste des utilisateurs.
@app.route('/users')
def users():
    if 'username' not in session:
        return redirect(url_for('login'))
    if "is_admin" not in session:
        return redirect(url_for("login"))
    message =None
    users= None  
    message, users = UserDao.list_all()
    return render_template('user/liste_users.html', message= message, users= users)

#Ajoute un nouvel utilisateur à la base de données.
@app.route('/add-users', methods= ['POST', 'GET'])
def add_user():
    if 'username' not in session:
        return redirect(url_for('login'))
    message =None
    user= None

    if request.method == "POST":
        nom_complet = request.form ['nom_complet']
        username = request.form ['username']
        password = request.form ['password']
        type = request.form ['type']

        password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, salt)
        
        if nom_complet=="" or username=="" or password=="" or type=="":
            message="error"
        else:
            user = User(nom_complet,username,hashed_password, type)
            message = UserDao.create(user)
        print(message)
    return render_template('user/add_users.html', message= message, user=user)

#Permet à l'utilisateur de faire un paiement suite à la réservation.
@app.route('/paiement', methods=['POST','GET'])
def paiement():
    if 'username' not in session and "is_admin" not in session:
        return redirect(url_for('login'))
    message=None
    id_evenement= session['id_evenement']
    montant = None
    evenement=None
    paiement=None
    reservation=None
    
    if id_evenement:
        evenement = EvenementDao.recuperer_evenement_par_id(id_evenement)
        if evenement:
            montant = evenement[4]

    print('prix',id_evenement)
    if request.method == 'POST':
        mode_paiement= request.form['mode_paiement']
        numero_carte=request.form['numero_carte']
        date_expiration=request.form['date_expiration']
        cvv = request.form['cvv']

        if  mode_paiement=="" or numero_carte=="" or date_expiration=="" or cvv=="":
            message="error"

        else:
            id_reservation = session.get('id_reservation')
            nouveau_statut= ReservationStatut.CONFIRME.value
            ReservationDao.update_statut_reservation(id_reservation, nouveau_statut)
            paiement= Paiement(montant,mode_paiement,numero_carte,date_expiration,cvv)
            message = PaiementDao.ajouter_paiement(paiement)
            if message=='success':
                return redirect(url_for('confirmation'))
                   
    return render_template('paiement.html', message=message, paiement=paiement, montant=montant,reservation=reservation)

#Permet à l'utilisateur d'envoiyer un email s'il a des question en rencontre des problèmes.
@app.route('/contact')
def contact():
    return render_template('contact.html')


