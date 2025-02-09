-- Create tables

CREATE TABLE `boletos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codcli` varchar(20) NOT NULL,
  `numnfv` varchar(20) NOT NULL,
  `numdfs` varchar(20) NOT NULL,
  `vlrabe` varchar(20) NOT NULL,
  `vlrori` varchar(20) NOT NULL,
  `vlrbco` varchar(20) NOT NULL,
  `vctori` varchar(30) NOT NULL,
  `datemi` varchar(30) NOT NULL,
  `titban` varchar(20) NOT NULL,
  `rpside` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB

CREATE TABLE `clientes_emails` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codcli` varchar(20) NOT NULL,
  `email` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB

CREATE TABLE `clientes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codcli` varchar(20) NOT NULL,
  `cgccpf` varchar(20) NOT NULL,
  `nomcli` varchar(200) NOT NULL,
  `apecli` varchar(100) NOT NULL,
  `usu_emanfe` varchar(500) NOT NULL,
  `senha_cli` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB



-- Todos clientes que possuem boletos emitidos esse mes
select distinct(c.nomcli), c.codcli
FROM clientes c
JOIN boletos b ON c.codcli = b.codcli
WHERE 
    MONTH(STR_TO_DATE(b.datemi, '%Y-%m-%d')) = MONTH(CURRENT_DATE())
    AND YEAR(STR_TO_DATE(b.datemi, '%Y-%m-%d')) = YEAR(CURRENT_DATE())
ORDER by c.nomcli;

-- Todos clientes que possuem boletos emitidos nos ultimos 30 dias 
SELECT DISTINCT c.nomcli, c.codcli
FROM clientes c
JOIN boletos b ON c.codcli = b.codcli
WHERE 
    STR_TO_DATE(b.datemi, '%Y-%m-%d') >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
ORDER BY c.nomcli;

-- Todos emails do cliente 11848
select * from clientes_emails where codcli = 11848

-- Todos boletos emitidos esse mes e nao pagos
select count(*) 
from boletos
where vlrbco > 0 
  and vlrabe > 0
  and MONTH(STR_TO_DATE(datemi, '%Y-%m-%d')) = MONTH(CURRENT_DATE())
  and YEAR(STR_TO_DATE(datemi, '%Y-%m-%d')) = YEAR(CURRENT_DATE())

-- Todos boletos emitidos esse mes e pagos
select count(*) 
from boletos
where vlrbco > 0 
  and vlrabe = 0
  and MONTH(STR_TO_DATE(datemi, '%Y-%m-%d')) = MONTH(CURRENT_DATE())
  and YEAR(STR_TO_DATE(datemi, '%Y-%m-%d')) = YEAR(CURRENT_DATE())

-- Boletos nao pagos vencendo em 3 dias
SELECT *
FROM boletos
WHERE vlrbco > 0 
  and vlrabe > 0
  and STR_TO_DATE(vctori, '%Y-%m-%d') = DATE_ADD(CURRENT_DATE(), INTERVAL 3 DAY);

-- Boletos vencendo hoje
SELECT *
FROM boletos
WHERE vlrbco > 0 
  and vlrabe > 0
  and STR_TO_DATE(vctori, '%Y-%m-%d') = CURRENT_DATE();


-- Boletos vencidos a 5 dias atras
SELECT *
FROM boletos
WHERE vlrbco > 0 
  and vlrabe > 0
  and STR_TO_DATE(vctori, '%Y-%m-%d') = DATE_SUB(CURRENT_DATE(), INTERVAL -5 DAY);

