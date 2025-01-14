# import-nfe.py

## Setting the variables

In order to run the script locally you need to define the following shell variables

```
export MYSQL_HOST=mysql.altmeyer.local
export MYSQL_DB=vida_nfe_nofity_sandbox
export MYSQL_USER=vida_nfe_nofity_sandbox
#export MYSQL_PASS=<PASS>

export MSSQL_HOST=mssql.altmeyer.local
export MSSQL_DB=Sapiens_Prod
export MSSQL_USER=sa
#export MSSQL_PASS=<PASS>
```

## Running locally using venv
```
cd app/import-nfe
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
./venv/bin/python import-nfe.py
```


## Running Locally using docker
```
docker  buildx build --platform  linux/amd64 -t vidatec_nfe_notify_import -f ./pipeline/docker/import-nfe.Dockerfile .

docker run -it --rm \
    -e MYSQL_HOST=$MYSQL_HOST \
    -e MYSQL_DB=$MYSQL_DB \
    -e MYSQL_USER=$MYSQL_USER \
    -e MYSQL_PASS=$MYSQL_PASS \
    -e MSSQL_HOST=$MSSQL_HOST \
    -e MSSQL_DB=$MSSQL_DB \
    -e MSSQL_USER=$MSSQL_USER \
    -e MSSQL_PASS=$MSSQL_PASS \
    vidatec_nfe_notify_import
```

## Manually upload the image to regitry
```
docker tag vidatec_nfe_notify_import registry.altmeyer.local:5000/vidatec_nfe_notify_import
docker push registry.altmeyer.local:5000/vidatec_nfe_notify_import
```

## Testar kustomize
Para testar o kustomize localmente:

Get a generated kustomize.yaml from the ADO Agent server
```
cd pipeline/kustomize
kustomize build overlays/sandbox 
kustomize build overlays/production
```

Exemplo de aplicar manualmente no cluster
```
kubectx <sandbox>
cd pipeline/kustomize
kubectl apply -k overlays/sandbox
```
