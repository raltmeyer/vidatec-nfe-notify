#################################
# Vida Tecnologia Ambiental
# Rogerio Altmeyer - 2025
#################################

from datetime import datetime

# Convert date from MySQL format (YYYY-MM-DD) to a readable format (DD/MM/YYYY).
def convert_date_to_readable(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return date_obj.strftime('%d/%m/%Y')
    except ValueError:
        return date_str

# Format the given value to Brazilian Reais format.
def format_to_brazilian_reais(value):
    try:
        return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except ValueError:
        return value