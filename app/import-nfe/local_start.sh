export mysql_host=mysql.altmeyer.local
export mysql_db=vida_nfe_nofity_sandbox
export mysql_user=vida_nfe_nofity_sandbox
#export mysql_pass=

export mssql_host=10.10.1.23
export mssql_db=Sapiens_Prod
export mssql_user=sa
#export mssql_pass=

python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt