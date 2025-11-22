from models.database import mysql
import MySQLdb.cursors
from datetime import datetime
import random
import string

class Operations:
    @staticmethod
    def generate_reference(prefix):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"{prefix}-{timestamp}-{random_str}"

    @staticmethod
    def create_receipt(supplier, warehouse_id, items, created_by):
        cursor = mysql.connection.cursor()
        try:
            reference = Operations.generate_reference('REC')
            
            # Create receipt
            cursor.execute('''
                INSERT INTO receipts (reference, supplier, created_by)
                VALUES (%s, %s, %s)
            ''', (reference, supplier, created_by))
            receipt_id = cursor.lastrowid
            
            # Add receipt items
            for item in items:
                cursor.execute('''
                    INSERT INTO receipt_items (receipt_id, product_id, quantity, warehouse_id)
                    VALUES (%s, %s, %s, %s)
                ''', (receipt_id, item['product_id'], item['quantity'], warehouse_id))
                
                # Update stock
                Operations.update_stock(item['product_id'], warehouse_id, item['quantity'], 'receipt', receipt_id)
            
            mysql.connection.commit()
            return True
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def create_delivery_order(customer, warehouse_id, items, created_by):
        cursor = mysql.connection.cursor()
        try:
            reference = Operations.generate_reference('DO')
            
            # Create delivery order
            cursor.execute('''
                INSERT INTO delivery_orders (reference, customer, created_by)
                VALUES (%s, %s, %s)
            ''', (reference, customer, created_by))
            delivery_id = cursor.lastrowid
            
            # Add delivery items
            for item in items:
                cursor.execute('''
                    INSERT INTO delivery_order_items (delivery_order_id, product_id, quantity, warehouse_id)
                    VALUES (%s, %s, %s, %s)
                ''', (delivery_id, item['product_id'], item['quantity'], warehouse_id))
                
                # Update stock (negative quantity for delivery)
                Operations.update_stock(item['product_id'], warehouse_id, -item['quantity'], 'delivery', delivery_id)
            
            mysql.connection.commit()
            return True
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def create_internal_transfer(from_warehouse_id, to_warehouse_id, items, created_by):
        cursor = mysql.connection.cursor()
        try:
            reference = Operations.generate_reference('TRF')
            
            # Create transfer
            cursor.execute('''
                INSERT INTO internal_transfers (reference, from_warehouse_id, to_warehouse_id, created_by)
                VALUES (%s, %s, %s, %s)
            ''', (reference, from_warehouse_id, to_warehouse_id, created_by))
            transfer_id = cursor.lastrowid
            
            # Add transfer items
            for item in items:
                cursor.execute('''
                    INSERT INTO internal_transfer_items (transfer_id, product_id, quantity)
                    VALUES (%s, %s, %s)
                ''', (transfer_id, item['product_id'], item['quantity']))
                
                # Update stock for both warehouses
                Operations.update_stock(item['product_id'], from_warehouse_id, -item['quantity'], 'transfer', transfer_id)
                Operations.update_stock(item['product_id'], to_warehouse_id, item['quantity'], 'transfer', transfer_id)
            
            mysql.connection.commit()
            return True
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def create_stock_adjustment(reason, items, created_by):
        cursor = mysql.connection.cursor()
        try:
            reference = Operations.generate_reference('ADJ')
            
            # Create adjustment
            cursor.execute('''
                INSERT INTO stock_adjustments (reference, reason, created_by)
                VALUES (%s, %s, %s)
            ''', (reference, reason, created_by))
            adjustment_id = cursor.lastrowid
            
            # Add adjustment items
            for item in items:
                cursor.execute('''
                    INSERT INTO stock_adjustment_items (adjustment_id, product_id, warehouse_id, quantity_before, quantity_after)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (adjustment_id, item['product_id'], item['warehouse_id'], item['current_quantity'], item['new_quantity']))
                
                # Calculate difference and update stock
                quantity_diff = item['new_quantity'] - item['current_quantity']
                if quantity_diff != 0:
                    Operations.update_stock(item['product_id'], item['warehouse_id'], quantity_diff, 'adjustment', adjustment_id)
            
            mysql.connection.commit()
            return True
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cursor.close()

    @staticmethod
    def update_stock(product_id, warehouse_id, quantity_change, movement_type, reference_id):
        cursor = mysql.connection.cursor()
        try:
            # Get current stock
            cursor.execute('''
                SELECT quantity FROM stock 
                WHERE product_id = %s AND warehouse_id = %s
            ''', (product_id, warehouse_id))
            current_stock = cursor.fetchone()
            
            if current_stock:
                new_quantity = current_stock[0] + quantity_change
                cursor.execute('''
                    UPDATE stock 
                    SET quantity = %s 
                    WHERE product_id = %s AND warehouse_id = %s
                ''', (new_quantity, product_id, warehouse_id))
            else:
                new_quantity = quantity_change
                cursor.execute('''
                    INSERT INTO stock (product_id, warehouse_id, quantity)
                    VALUES (%s, %s, %s)
                ''', (product_id, warehouse_id, new_quantity))
            
            # Log movement
            cursor.execute('''
                INSERT INTO stock_movements (product_id, warehouse_id, movement_type, reference_id, quantity_change, quantity_after)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (product_id, warehouse_id, movement_type, reference_id, quantity_change, new_quantity))
            
        except Exception as e:
            raise e