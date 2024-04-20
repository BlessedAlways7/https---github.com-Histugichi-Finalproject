from user_dao import UserDao
from user import User


"""
(message,user) =UserDao.get_one('Diallo123')
print(user[3])

password_hash_db = user[2]
print(password_hash_db)

password = 'gcfhghgfdd'
password = password.encode()
password_hash_db = password_hash_db.encode()

if bcrypt.checkpw(password, password_hash_db):
    print("Password is correct")
else:
    print("Password is incorrect")

    
"""

user= UserDao.get_user_role('Sam4Beru')
print(user)