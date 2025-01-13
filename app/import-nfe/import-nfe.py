#################################
# Vida Tecnologia Ambiental
# Rogerio Altmeyer - 2025
#################################

import os
import pytds
import mysql.connector
from mysql.connector import errorcode
import csv
#https://python-tds.readthedocs.io/en/latest/

mysql_host = os.getenv('mysql_host')
mysql_db   = os.getenv('mysql_db')
mysql_user = os.getenv('mysql_user')
mysql_pass = os.getenv('mysql_pass')
mssql_host = os.getenv('mssql_host')
mssql_db   = os.getenv('mssql_db')
mssql_user = os.getenv('mssql_user')
mssql_pass = os.getenv('mssql_pass')

# MySQL tables definition
TABLES = {}

TABLES['boletos'] = (
    "CREATE TABLE `boletos` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `codcli` varchar(20) NOT NULL,"
    "  `numnfv` varchar(20) NOT NULL,"
    "  `numdfs` varchar(20) NOT NULL,"
    "  `vlrabe` varchar(20) NOT NULL,"
    "  `vlrori` varchar(20) NOT NULL,"
    "  `vlrbco` varchar(20) NOT NULL,"
    "  `vctori` varchar(30) NOT NULL,"
    "  `datemi` varchar(30) NOT NULL,"
    "  `titban` varchar(20) NOT NULL,"
    "  `rpside` varchar(100) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['clientes_emails'] = (
    "CREATE TABLE `clientes_emails` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `codcli` varchar(20) NOT NULL,"
    "  `email` varchar(200) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['clientes'] = (
    "CREATE TABLE `clientes` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `codcli` varchar(20) NOT NULL,"
    "  `cgccpf` varchar(20) NOT NULL,"
    "  `nomcli` varchar(200) NOT NULL,"
    "  `apecli` varchar(100) NOT NULL,"
    "  `usu_emanfe` varchar(500) NOT NULL,"
    "  `senha_cli` varchar(20) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")


##################
##

# MySQL connection
mysql_conn = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_pass,
    database=mysql_db
)
mysql_cursor = mysql_conn.cursor()


# create tables if not exists 
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        mysql_cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

# clean-up tables
print ("Cleaning up data for all tables...")
sql = 'delete from clientes'
mysql_cursor.execute(sql)
sql = 'delete from clientes_emails'
mysql_cursor.execute(sql)
sql = 'delete from boletos'
mysql_cursor.execute(sql)
mysql_conn.commit()


print ("Extract data from Sapiens DB")
with pytds.connect(mssql_host, 
                    mssql_db, 
                    mssql_user, 
                    mssql_pass) as mssql_conn:

    #Boletos
    print ("Boletos ...")
    with mssql_conn.cursor() as mssql_cur:
        query = "select nf.codcli, nf.numnfv, nf.numdfs, nf.vlrabe, nf.vlrori, nf.vlrbco, \
                    nf.vctori, nf.datemi, nf.titban, bol.RPSIDE \
                from Sapiens_Prod..E085Cli as cli \
                left join Sapiens_Prod..E301TCR as nf on cli.codcli = nf.codcli \
                    and nf.codemp = 81 \
                left join SDE_Prod..N140NFS as bol on bol.numnfv = nf.numnfv \
                    and cli.cgccpf = bol.cgccpf \
                where nf.datemi >= '2025-01-01' \
                and cli.usu_gerres = 'S' \
                order by nf.numdfs desc"
        mssql_cur.execute(query)
        tudo = mssql_cur.fetchall()
        
    insert_query = """
        INSERT INTO boletos (codcli, numnfv, numdfs, vlrabe, vlrori, vlrbco, vctori, datemi, titban, RPSIDE)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    for row in tudo:
        mysql_cursor.execute(insert_query, row)
    mysql_conn.commit()
    print("Data inserted into MySQL table 'boletos'")


    #Clientes
    print ("Clientes ...")
    with mssql_conn.cursor() as mssql_cur:
        query = "select codcli, CONVERT(bigint, CGCCPF) as cgccpf, \
                  nomcli, apecli, usu_emanfe, USU_SenCli \
                from E085Cli \
                where usu_gerres = 'S'"
        mssql_cur.execute(query)
        tudo = mssql_cur.fetchall()

    insert_query = """
        INSERT INTO clientes (codcli, cgccpf, nomcli, apecli, usu_emanfe, senha_cli)
        VALUES (%s, %s, %s, %s, %s, %s)"""
    for row in tudo:
        # Replace NULL values in senha_cli with a default value, e.g., an empty string
        row = list(row)
        if row[5] is None:
            row[5] = ''
        mysql_cursor.execute(insert_query, row)
    mysql_conn.commit()
    print("Data inserted into MySQL table 'clientes'")


    #Clientes emails
    print ("Cliente emails ...")
    with mssql_conn.cursor() as mssql_cur:
        query = "select codcli, usu_emanfe \
                from E085Cli \
                where usu_gerres = 'S'"
        mssql_cur.execute(query)
        db = mssql_cur.fetchall()
    insert_query = """
        INSERT INTO clientes_emails (codcli, email)
        VALUES (%s, %s)"""

    for cliid, emaildb in db:
        emails = emaildb.split(';')
        for email in emails:
            clean_email = email.strip().lower()
            if ("multtiservicos.com.br" in clean_email or
                "vidatecambiental.com.br" in clean_email or
                "iemercurio.com.br" in clean_email or
                len(clean_email) < 5):
                continue
            mysql_cursor.execute(insert_query, (cliid, clean_email))
    mysql_conn.commit()
    print("Data inserted into MySQL table 'clientes_emails'")

mysql_cursor.close()
mysql_conn.close()
mssql_conn.close()
print ("Database import finished")
