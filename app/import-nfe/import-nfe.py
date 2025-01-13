#################################
# Vida Tecnologia Ambiental
# Rogerio Altmeyer - 2025
#################################

import mysql.connector
from mysql.connector import errorcode
import csv
#https://python-tds.readthedocs.io/en/latest/

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



#Extract data from database
print ("extrai dados do MS-SQL")
with pytds.connect(db_credentials.sql_server, db_credentials.sql_db_sapiens, db_credentials.sql_user, db_credentials.sql_pass) as conn:

    #Boletos
    print ("Boletos ...")
    with conn.cursor() as cur:
        query = "select nf.codcli, nf.numnfv, nf.numdfs, nf.vlrabe, nf.vlrori, nf.vlrbco, \
                    nf.vctori, nf.datemi, nf.titban, bol.RPSIDE \
                from Sapiens_Prod..E085Cli as cli \
                left join Sapiens_Prod..E301TCR as nf on cli.codcli = nf.codcli \
                    and nf.codemp = 81 \
                left join SDE_Prod..N140NFS as bol on bol.numnfv = nf.numnfv \
                    and cli.cgccpf = bol.cgccpf \
                where nf.datemi >= '2023-01-01' \
                and cli.usu_gerres = 'S' \
                order by nf.numdfs desc"
        cur.execute(query)
        tudo = cur.fetchall()
    with open(db_credentials.import_export_files + 'boletos.csv', 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(['codcli', 'numnfv', 'numdfs', 'vlrabe', 'vlrori', 'vlrbco', 'vctori', 'datemi', 'titban', 'rpside'])
        writer.writerows(tudo)

    #Clientes
    print ("Clientes ...")
    with conn.cursor() as cur:
        query = "select codcli, CONVERT(bigint, CGCCPF) as cgccpf, \
                  nomcli, apecli, usu_emanfe, USU_SenCli \
                from E085Cli \
                where usu_gerres = 'S'"
        cur.execute(query)
        tudo = cur.fetchall()
    with open(db_credentials.import_export_files + 'clientes.csv', 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(['codcli', 'cgccpf', 'nomcli', 'apecli', 'usu_emanfe', 'senha_cli'])
        writer.writerows(tudo)

    #Clientes emails
    print ("Cliente emails ...")
    with conn.cursor() as cur:
        query = "select codcli, usu_emanfe \
                from E085Cli \
                where usu_gerres = 'S'"
        cur.execute(query)
        db = cur.fetchall()
    with open(db_credentials.import_export_files + 'clientes_emails.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['codcli', 'email'])
        for cliid, emaildb in db:
            emails = emaildb.split(';')
            for email in emails:
                clean_email = email.strip().lower()
                if ("multtiservicos.com.br" in clean_email or
                    "vidatecambiental.com.br" in clean_email or
                    "iemercurio.com.br" in clean_email or
                    len(clean_email) < 5):
                    continue
                writer.writerow([cliid, email.strip().lower()])
                #print (cliid , ":" , email)



#################################
# Vida Tecnologia Ambiental
# Rogerio Altmeyer - 2023
#################################


##################
##
def connect():
   try:
       cnx = mysql.connector.connect(host=db_credentials.mysql_host,
                                   user=db_credentials.mysql_user,
                                   passwd=db_credentials.mysql_pass)
       if cnx.is_connected():
           print('Connected to MySQL database')
       return cnx
   except errorcode as e:
       print(e)

##################
##
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_credentials.mysql_db))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

##################
##

cnx = connect()
cursor = cnx.cursor()

#create database
try:
    cursor.execute("USE {}".format(db_credentials.mysql_db))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(db_credentials.mysql_db))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(db_credentials.mysql_db))
        cnx.database = db_credentials.mysql_db
    else:
        print(err)
        exit(1)

#create tables
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

#clean-up tables
print ("Cleaning up data for all tables...")
sql = 'delete from clientes'
cursor.execute(sql)
sql = 'delete from clientes_emails'
cursor.execute(sql)
sql = 'delete from boletos'
cursor.execute(sql)
cnx.commit()

#read csv files and inserting to database
print ("Importing data for table clientes...")
with open(db_credentials.import_export_files + 'clientes.csv', mode='r') as csv_file:
    csvFile = csv.reader(csv_file)
    header = next(csvFile)
    headers = map((lambda x: '`'+x+'`'), header)
    insert = 'INSERT INTO clientes (' + ", ".join(headers) + ") VALUES "
    for row in csvFile:
        values = map((lambda x: '"'+x+'"'), row)
        sql = insert +"("+ ", ".join(values) +");"
        cursor.execute(sql)
    csv_file.close()
    cnx.commit()


print ("Importing data for table clientes_email...")
with open(db_credentials.import_export_files + 'clientes_emails.csv', mode='r') as csv_file:
    csvFile = csv.reader(csv_file)
    header = next(csvFile)
    headers = map((lambda x: '`'+x+'`'), header)
    insert = 'INSERT INTO clientes_emails (' + ", ".join(headers) + ") VALUES "
    for row in csvFile:
        values = map((lambda x: '"'+x+'"'), row)
        sql = insert +"("+ ", ".join(values) +");"
        #print (sql)
        cursor.execute(sql)
    csv_file.close()
    cnx.commit()

print ("Importing data for table boletos...")
with open(db_credentials.import_export_files + 'boletos.csv', mode='r') as csv_file:
    csvFile = csv.reader(csv_file)
    header = next(csvFile)
    headers = map((lambda x: '`'+x+'`'), header)
    insert = 'INSERT INTO boletos (' + ", ".join(headers) + ") VALUES "
    for row in csvFile:
        values = map((lambda x: '"'+x+'"'), row)
        sql = insert +"("+ ", ".join(values) +");"
        #print (sql)
        cursor.execute(sql)
    csv_file.close()
    cnx.commit()

cursor.close()
cnx.close()
print ("Database import finished")