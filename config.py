<<<<<<< HEAD
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-this')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
    MYSQL_DB = os.getenv('MYSQL_DB', 'inventory_management')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    # Add connection timeout and pool settings
    MYSQL_CONNECT_TIMEOUT = 10
=======
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-this')
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
    MYSQL_DB = os.getenv('MYSQL_DB', 'inventory_management')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    # Add connection timeout and pool settings
    MYSQL_CONNECT_TIMEOUT = 10
>>>>>>> ad037788d016f07a4048a89b262d999f5d561f95
    MYSQL_READ_DEFAULT_FILE = '/etc/my.cnf'