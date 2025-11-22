from models.database import mysql
import MySQLdb.cursors

class Warehouse:
    def __init__(self, id, name, location, created_at):
        self.id = id
        self.name = name
        self.location = location
        self.created_at = created_at

    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM warehouses ORDER BY name')
        warehouses = cursor.fetchall()
        cursor.close()
        return warehouses

    @staticmethod
    def get_by_id(warehouse_id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM warehouses WHERE id = %s', (warehouse_id,))
        warehouse = cursor.fetchone()
        cursor.close()
        return warehouse

    @staticmethod
    def create(name, location):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO warehouses (name, location)
                VALUES (%s, %s)
            ''', (name, location))
            mysql.connection.commit()
            return True
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def update(warehouse_id, name, location):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''
                UPDATE warehouses 
                SET name = %s, location = %s
                WHERE id = %s
            ''', (name, location, warehouse_id))
            mysql.connection.commit()
            return True
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def delete(warehouse_id):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('DELETE FROM warehouses WHERE id = %s', (warehouse_id,))
            mysql.connection.commit()
            return True
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cursor.close()