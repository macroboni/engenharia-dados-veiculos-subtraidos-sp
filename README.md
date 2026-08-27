# Engenharia de Dados — Veículos Subtraídos em São Paulo

Projeto de Engenharia de Dados com Databricks, Python e PySpark para processar dados de veículos roubados e furtados no Estado de São Paulo.

## Objetivo

Simular o ciclo de trabalho de um engenheiro de dados:

- Landing Zone para preservação dos arquivos recebidos;
- arquitetura medalhão com camadas Bronze, Silver e Gold;
- ingestão incremental com Auto Loader;
- orquestração com Lakeflow Jobs;
- testes automatizados e controles de qualidade;
- CI/CD com ambientes de homologação e produção;
- desenvolvimento por branches, commits e Pull Requests.

## Fluxo

```text
Excel recebido
    ↓
Landing Zone
    ↓
Auto Loader / Notebook PySpark
    ↓
Bronze → Silver → Gold
    ↓
Tabelas analíticas e indicadores
```

## Dados

Os arquivos brutos não serão versionados no GitHub porque contêm placas e endereços. Eles serão armazenados em um Volume do Unity Catalog no Databricks.

## Ambiente de estudo

O projeto será compatível com o Databricks Free Edition. Como essa edição possui somente um workspace, homologação e produção serão separadas logicamente por schemas e targets de implantação.
