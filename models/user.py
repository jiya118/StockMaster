from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import mysql
import MySQLdb.cursors

class User(UserMixin):
    def __init__(self, id, name, email, password, role, created_at):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.created_at = created_at

    @staticmethod
    def get_by_id(user_id):
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
            user_data = cursor.fetchone()
            cursor.close()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    password=user_data['password'],
                    role=user_data['role'],
                    created_at=user_data['created_at']
                )
            return None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None

    @staticmethod
    def get_by_email(email):
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user_data = cursor.fetchone()
            cursor.close()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    name=user_data['name'],
                    email=user_data['email'],
                    password=user_data['password'],
                    role=user_data['role'],
                    created_at=user_data['created_at']
                )
            return None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None

    @staticmethod
    def create(name, email, password, role='staff'):
        try:
            cursor = mysql.connection.cursor()
            hashed_password = generate_password_hash(password)
            
            cursor.execute('''
                INSERT INTO users (name, email, password, role)
                VALUES (%s, %s, %s, %s)
            ''', (name, email, hashed_password, role))
            
            mysql.connection.commit()
            user_id = cursor.lastrowid
            cursor.close()
            
            print(f"✅ User created successfully with ID: {user_id}")
            return User.get_by_id(user_id)
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            mysql.connection.rollback()
            return None

    def check_password(self, password):
        return check_password_hash(self.password, password)