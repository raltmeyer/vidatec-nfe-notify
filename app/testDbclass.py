import os
from classDatabaseQueries import DatabaseQueries

host = os.getenv('MYSQL_HOST')
database = os.getenv('MYSQL_DB')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASS')

db = DatabaseQueries(host=host, database=database, user=user, password=password)
db.connect()

# Get all emails for a specific client
client_emails = db.get_client_emails(11848)
print("Client Emails:", client_emails)

# Count all unpaid boletos issued this month
unpaid_boletos_count = db.count_unpaid_boletos_this_month()
print("Unpaid Boletos This Month:", unpaid_boletos_count)

# Count all paid boletos issued this month
paid_boletos_count = db.count_paid_boletos_this_month()
print("Paid Boletos This Month:", paid_boletos_count)

# Get all clients with boletos issued in the last 30 days
#clients_with_boletos = db.get_clients_with_boletos_last_30_days()
#print("Clients with Boletos in the Last 30 Days:", clients_with_boletos)

# Disconnect from the database
db.disconnect()