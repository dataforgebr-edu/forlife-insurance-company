## Forlife Insurance Company
Empresa do ramo de seguros que vende apolices de tres segmentos: vida, automovel e residencia.
Com o crescimento, surgiram problemas de dados como indicadores divergentes, silos entre areas e lentidao no acesso a informacoes para decisao.

# Missao
Criar um ambiente de dados que permita analise e compartilhamento rapido das informacoes de diferentes sistemas da companhia, mantendo governanca sobre os ativos de dados.

* Etapa 1 - Criar a estrutura de dados da companhia usando Faker.

## Populacao continua com regras de negocio
Foi adicionado o script `src/populate_data.py` para geracao continua de dados coerentes entre as tabelas.

Regras implementadas:
- Fluxo de carga: corretor -> cliente -> apolice -> parcelas -> sinistro.
- Datas de parcelas respeitam o periodo de vigencia da apolice.
- Tabelas de dominio sao carregadas automaticamente quando vazias.

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
