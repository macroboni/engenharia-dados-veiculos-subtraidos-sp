# Databricks notebook source
# MAGIC %md
# MAGIC # Landing Zone para Bronze
# MAGIC
# MAGIC Este notebook é executado por um Lakeflow Job.
# MAGIC Ele identifica novos arquivos Excel na Landing Zone e os grava
# MAGIC incrementalmente em uma tabela Delta da camada Bronze.

# COMMAND ----------

from pathlib import Path
import sys

src_path = Path.cwd().parent / "src"
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

from veiculos_subtraidos.bronze import run_landing_to_bronze
from veiculos_subtraidos.config import ProjectConfig

# COMMAND ----------

dbutils.widgets.text("catalog", "workspace")
dbutils.widgets.dropdown("environment", "hml", ["hml", "prod"])

catalog = dbutils.widgets.get("catalog")
environment = dbutils.widgets.get("environment")

config = ProjectConfig(
    catalog=catalog,
    environment=environment,
)

# COMMAND ----------

landing_path = config.volume_path(
    "arquivos",
    "veiculos_subtraidos",
)
target_table = config.table(
    "bronze",
    "veiculos_subtraidos",
)

print(f"Landing Zone: {landing_path}")
print(f"Tabela Bronze: {target_table}")

# COMMAND ----------

run_landing_to_bronze(
    spark=spark,
    config=config,
)

print("Ingestão Landing Zone para Bronze concluída.")
