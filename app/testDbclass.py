#################################
# Vida Tecnologia Ambiental
# Rogerio Altmeyer - 2025
#################################

import os
from classDatabaseQueries import DatabaseQueries

db = DatabaseQueries()
db.connect()

# Get all emails for a specific client
client_emails = db.get_client_emails(11848)
print("Client Emails:", client_emails)

# Count all unpaid boletos issued this month
unpaid_nfe_count = db.count_unpaid_nfes_this_month()
print("Unpaid NFes This Month:", unpaid_nfe_count)

# Disconnect from the database
db.disconnect()