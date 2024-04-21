from flask import Flask, render_template, request, session, url_for, redirect
import bcrypt

from users.user_dao import UserDao
from users.user import User
from evenements.evenement import Evenement
from evenements.evenement_dao import EvenementDao
from paiements.paiement import Paiement
from paiements.paiement_dao import PaiementDao
from reservations.reservation_dao import ReservationDao
from reservations.reservation import Reservation
from reservations.statut import ReservationStatut


app = Flask(__name__,)
app.secret_key = 'secretkey'
salt = bcrypt.gensalt(rounds=12)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/accueil')
def accueil():
    return render_template('accueil.html')

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
                         
                        if user[4] ==1: #verifier si c'est un admin, sinon rediriger vers la page de reservation
                            session["is_admin"]=user[4]
                            return redirect(url_for('admin'))
                        else:
                            return redirect(url_for("accueil"))  
        print(message)
    return render_template('login.html', message=message, user=None)

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

@app.route('/evenement')
def evenement():
    message, evenements=EvenementDao.get_all()
    return render_template('event/evenement.html', message=message, evenements=evenements)

@app.route('/add_event', methods= ['POST', 'GET'])
def add_event():
    if "is_admin" not in session:
        return redirect(url_for('login'))
    req = request.form
    message=None
    evenement=None

    if request.method == "POST":
        nom = req ['nom']
        date = req ['date']
        emplacement = req ['emplacement']
        prix = req ['prix']
        id_evenement = req ['id']
        
        if nom=="" or date=="" or emplacement=="" or prix=="" or id_evenement=="":
            message="error"
        else:
            evenement = Evenement(nom,date,emplacement,prix,id_evenement)
            message = EvenementDao.create_evenement(evenement)
        print(message)
    return render_template('event/add_event.html', message=message, evenement=evenement)

@app.route('/modify_event', methods= ['POST', 'GET'])
def modify_event():
    if "is_admin" not in session:
        return redirect(url_for('login'))
    message=None
    evenement=None
    
    if request.method == "POST":
        id_evenement=request.form['id_evenement']
        id_evenement=id_evenement,
        nom= request.form['nom'],
        date = request.form ['date'],
        emplacement = request.form ['emplacement'],
        prix = request.form['prix']  
       
        if nom=="" or date=="" or emplacement=="" or prix=="":
            message="error"
        else:
            nouveau_evenement=Evenement(
                id_evenement=id_evenement,
                nom=nom,
                date=date,
                emplacement=emplacement,
                prix=prix
            )
            message =EvenementDao.modifier_evenement(id_evenement,nouveau_evenement)    
            if message=='success':
                message="Modification successful"
    else:
        id_evenement= request.args.get('id_evenement')
        evenement = EvenementDao.recuperer_evenement_par_id(id_evenement)
    return render_template('event/modify_event.html', message=message, evenement=evenement)


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
        prix = request.form['prix']
        id_evenement = request.form['id_evenement']

        if nom=="" or date=="" or emplacement=="" or prix=="" or id_evenement=="":
            message="error"
        else:
            evenement = Evenement(nom, date,emplacement,prix,id_evenement)
            message = EvenementDao.supprimer_evenement(id_evenement)
        print(message)
    return render_template('event/delete_event.html', message=message, evenement=evenement)


@app.route('/liste_reservation')
def liste_reservation():
    if "is_admin" not in session:
        return redirect(url_for('login'))
    message, reservations=ReservationDao.get_all()
    return render_template('reservation/liste_reservation.html', message=message, reservations=reservations)

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

@app.route('/statut')
def statut():
    if "is_admin" not in session:
        return redirect(url_for('login'))
    reservations = ReservationDao.afficher_statut_reservations()
    return render_template('reservation/statut.html',  reservations=reservations)


@app.route("/logout")
def logout():
    session.clear() # On vide la session
    return redirect(url_for('login'))


@app.route('/reservations', methods=['POST', 'GET'])
def reservations():
    if 'username' not in session and "is_admin" not in session:
        return redirect(url_for('login'))
    
    message=None
    reservation=None
    id_evenement = request.form.get('id_evenement') 
    id_user= request.form.get('id_user')
    
    
    if request.method == 'POST':
        nom = request.form['nom']
        date = request.form['date']
        place = request.form['place']

        if nom=="" or date=="" or place=="" :
            message="error"
        else:
            id_reservation =1
            statut = ReservationStatut.EN_ATTENTE
            
            reservation = Reservation(nom, date, place,id_evenement,id_user,id_reservation,statut)
            message = ReservationDao.reserver_place(reservation)
            if message =='success':
                return redirect(url_for('paiement'))
            else:
                message= "Une erreur s'est produite lors de la réservation. Veuillez réessayer."
    
    evenement = EvenementDao.recuperer_evenement_par_id(id_evenement) if id_evenement else None
    user = UserDao.recuperer_user_par_id(id_user) if id_user else None
    
    return render_template('reservation/reservations.html',message=message, reservation=reservation,evenement=evenement,user=user,id_evenement=id_evenement,id_user=id_user)


@app.route('/historique')
def historique():
    if 'username' not in session and "is_admin" not in session:
        return redirect(url_for('login'))
    id_user=request.args.get('id_user')
    message, reservations = ReservationDao.filtrer_reservations_id_user(id_user)
    return render_template('reservation/historique.html', message=message, reservations=reservations)

@app.route('/confirmation')
def confirmation():
    id_reservation= request.args.get('id_reservation')
    message=ReservationDao.confirmer_reservation(id_reservation)
    if message== 'success':
        return redirect(url_for('confirmation'))
    else:
        return render_template('paiement.html',message=message)

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

@app.route('/add-users', methods= ['POST', 'GET'])
def add_user():
    if 'username' not in session:
        return redirect(url_for('login'))
    req = request.form
    message =None
    user= None

    if request.method == "POST":
        nom_complet = req ['nom_complet']
        username = req ['username']
        password = req ['password']
        type = req ['type']

        password = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password, salt)
        
        if nom_complet=="" or username=="" or password=="" or type=="":
            message="error"
        else:
            user = User(nom_complet,username,hashed_password, type)
            message = UserDao.create(user)
        print(message)
    return render_template('user/add_users.html', message= message, user=user)


@app.route('/paiement', methods=['POST','GET'])
def paiement():
    message=None
    montant = request.args.get('montant')
   
    if request.method == 'POST':
        
        mode_paiement= request.form['mode_paiement']
        numero_carte=request.form['numero_carte']
        date_expiration=request.form['date_expiration']
        cvv = request.form['cvv']

        if  mode_paiement=="" or numero_carte=="" or date_expiration=="" or cvv=="":
            message="error"
        else:
            paiement= Paiement(montant,mode_paiement,numero_carte,date_expiration,cvv)
            message = PaiementDao.ajouter_paiement(paiement)
            return redirect(url_for('confirmation'))
        id_evenement = request.args.get('id_evenement')
        evenement = EvenementDao.recuperer_evenement_par_id(id_evenement)
    if evenement:
        montant = evenement[4]
    return render_template('paiement.html', message=message, paiement=paiement, montant=montant)


if __name__ == "__main__":
    app.run(debug=True)
