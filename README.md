## Forlife Insurance Company
Empresa do ramo de seguros que vende apolices de tres segmentos: vida, automovel e residencia.
Com o crescimento, surgiram problemas de dados como indicadores divergentes, silos entre areas e lentidao no acesso a informacoes para decisao.

# Missao
Criar um ambiente de dados que permita analise e compartilhamento rapido das informacoes de diferentes sistemas da companhia, mantendo governanca sobre os ativos de dados.

* Etapa 1 - Criar a estrutura de dados da companhia usando Faker.

## Populacao continua com regras de negocio
Foi adicionado o script `src/populate_data.py` para geracao continua de dados coerentes entre as tabelas.

Regras de negócio:
- As tabelas de produto, estados, cidades, estatus da apólice, periodicidade de pagamento, meio de pagamento e estatus de sinistro são informações de domínio carregadas na primeira execução.
- Antes de haver qualquer venda de apólice é necessário que um corretor esteja previamente cadastrado, um corretor pode realziar mais de uma venda.
- O cadastro do cliente deve ser feito antes da venda de uma apólice.
- Toda apólice deve ter um corretor associado e um cliente e ambos devem ter o cadastro anterior a data de inclusáo da apólice.
- A apólice tem sua data de início de vigência junto com a data de criação.
- Um cliente por uma ou várias apólice.
- Um corretor pode ter nenhuma ou muitas apólices vendidas.
- O cliente paga N parcelas que devem estar dentro do período de vigência da apólice.
- Nem todas as apólices tem sinistro 

Execucao unica:

```bash
cd src
python populate_data.py --mode once --batch-size 20
```

Execucao continua:

```bash
cd src
python populate_data.py --mode continuous --batch-size 10 --interval-seconds 30
```

# Next Steps

- Implementar decorador para registro de logs
- Criar uma API para expor os dados
