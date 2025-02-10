#################################
# Vida Tecnologia Ambiental
# Rogerio Altmeyer - 2025
#################################

import logging
from classDatabaseQueries import DatabaseQueries
from utils import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BoletosTable:

    def clientesVencimentoByAddDate(self, add_date):
        db = DatabaseQueries()
        db.connect()

        boletos = db.get_boletos_by_date(add_date)

        # Generate HTML table for boletos due in 3 days
        boletos_table_rows = ""
        for boleto in boletos:
            boletos_table_rows += f"""
            <tr>
                <td>{boleto['codcli']} - {boleto['nomcli']}</td>
                <td>{convert_date_to_readable(boleto['datemi'])}</td>
                <td>{convert_date_to_readable(boleto['vctori'])}</td>
                <td>{format_to_brazilian_reais(boleto['vlrori'])}</td>
            </tr>
            """

        boletos_table_html = f"""
        <table border="1">
            <tr>
                <th>Cliente</th>
                <th>Emitido</th>
                <th>Vencimento</th>
                <th>Valor</th>
            </tr>
            {boletos_table_rows}
        </table>
        """

        db.disconnect()
        return boletos_table_html
    
