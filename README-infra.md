# Infra-estrutura e deployment

## Promoções

Para promover uma release para ambientes:

A seguinte sequencia de comandos irá executar a promoção do codigo para o branch sandbox, e a pipeline desse ambiente será inicializada, acompanha-la no [ADO](https://dev.azure.com/raltmeyer/Altmeyer/_build).
```
git checkout main
git pull --rebase
git push -f origin main^{commit}:sandbox
```

Para o ambiente de produção
```
git checkout main
git pull --rebase
git push -f origin main^{commit}:production 
```


## DNS

Foi criado um terraform que aplica IPs fixos dos cluster disponiveis durante a pipeline

[Atualizando DNS](./pipeline/terraform_dns/)

Nota: o terraform foi configurado para usar o state no postgree no database chamado 'tf_dns_myevents'

Para testar localmente voce precisará das credenciais do PG, segue exemplo de execução local:

```
export PGHOST=<host_ip>
export PGUSER=<user>
export PGPASSWORD=<pass>
export PGDATABASE=tf_dns_myevents
terraform init
terraform validate
terraform plan -compact-warnings
```

## Kustomize

Todos os manifestos de kubernetes são gerados utilizando kustomize no seguinte folder [kustomize tree](./pipeline/kustomize/)

```
??? pipeline/kustomize
  ??? base
    ?   ??? manifesto1.yaml
    ?   ??? manifesto2.yaml
    ?   ??? kustomization.yaml
    ? overlays
        ??? sandbox
        ?   ??? patch1-sandbox.yaml
        |   ??? patch2-sandbox.yaml
        ?   ??? kustomization.yaml
        ??? production
            ??? patch1-prod.yaml
            ??? patch2-prod.yaml
            ??? kustomization.yaml
```

Os manifestos no folder base são manipulados pelo kustomize utilizando os patches dentro de overlays, configurando os recursos difentes em cada ambiente.

Para testar o kustomize localmente:
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


## Permissoes mysql

Para reproduzir as permissoes no servidor mysql

Sandbox
```
CREATE USER 'myevents_sandbox'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON myevents_sandbox.* TO 'myevents_sandbox'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

SHOW GRANTS FOR 'myevents_sandbox'@'%'
ALTER USER 'myevents_sandbox'@'%' IDENTIFIED BY 'password';
```

Production
```
CREATE USER 'myevents_production'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON myevents_production.* TO 'myevents_production'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

ALTER USER 'myevents_production'@'%' IDENTIFIED BY 'password';
```
