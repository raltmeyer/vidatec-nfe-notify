import mysql.connector
from mysql.connector import Error
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseQueries:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                logging.info("Connected to MySQL database")
        except Error as e:
            logging.info(f"Error connecting to MySQL database: {e}")

    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()
            logging.info("Disconnected from MySQL database")

    def get_client_emails(self, codcli):
        query = "SELECT * FROM clientes_emails WHERE codcli = %s"
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, (codcli,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def count_unpaid_boletos_this_month(self):
        query = """
        SELECT COUNT(*) AS count
        FROM boletos
        WHERE vlrbco > 0 
          AND vlrabe > 0
          AND MONTH(STR_TO_DATE(datemi, '%Y-%m-%d')) = MONTH(CURRENT_DATE())
          AND YEAR(STR_TO_DATE(datemi, '%Y-%m-%d')) = YEAR(CURRENT_DATE())
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result['count']

    def count_paid_boletos_this_month(self):
        query = """
        SELECT COUNT(*) AS count
        FROM boletos
        WHERE vlrbco > 0 
          AND vlrabe = 0
          AND MONTH(STR_TO_DATE(datemi, '%Y-%m-%d')) = MONTH(CURRENT_DATE())
          AND YEAR(STR_TO_DATE(datemi, '%Y-%m-%d')) = YEAR(CURRENT_DATE())
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result['count']

    def get_clients_with_boletos_last_30_days(self):
        query = """
        SELECT DISTINCT c.nomcli, c.codcli
        FROM clientes c
        JOIN boletos b ON c.codcli = b.codcli
        WHERE STR_TO_DATE(b.datemi, '%Y-%m-%d') >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
        ORDER BY c.nomcli
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

