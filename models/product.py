from models.database import mysql
import MySQLdb.cursors

class Product:
    def __init__(self, id, name, sku, category_id, unit_of_measure, description, min_stock_level, created_at):
        self.id = id
        self.name = name
        self.sku = sku
        self.category_id = category_id
        self.unit_of_measure = unit_of_measure
        self.description = description
        self.min_stock_level = min_stock_level
        self.created_at = created_at

    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN product_categories c ON p.category_id = c.id 
            ORDER BY p.name
        ''')
        products = cursor.fetchall()
        cursor.close()
        return products

    @staticmethod
    def get_by_id(product_id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''
            SELECT p.*, c.name as category_name 
            FROM products p 
            LEFT JOIN product_categories c ON p.category_id = c.id 
            WHERE p.id = %s
        ''', (product_id,))
        product = cursor.fetchone()
        cursor.close()
        return product

    @staticmethod
    def create(name, sku, category_id, unit_of_measure, description, min_stock_level):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''
                INSERT INTO products (name, sku, category_id, unit_of_measure, description, min_stock_level)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (name, sku, category_id, unit_of_measure, description, min_stock_level))
            mysql.connection.commit()
            return True
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def update(product_id, name, sku, category_id, unit_of_measure, description, min_stock_level):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('''
                UPDATE products 
                SET name = %s, sku = %s, category_id = %s, unit_of_measure = %s, 
                    description = %s, min_stock_level = %s
                WHERE id = %s
            ''', (name, sku, category_id, unit_of_measure, description, min_stock_level, product_id))
            mysql.connection.commit()
            return True
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def delete(product_id):
        cursor = mysql.connection.cursor()
        try:
            cursor.execute('DELETE FROM products WHERE id = %s', (product_id,))
            mysql.connection.commit()
            return True
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cursor.close()