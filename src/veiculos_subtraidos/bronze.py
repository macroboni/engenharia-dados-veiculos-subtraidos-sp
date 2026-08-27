"""Ingestão incremental da Landing Zone para a camada Bronze."""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from veiculos_subtraidos.config import ProjectConfig
from veiculos_subtraidos.schema import BRONZE_COLUMNS, validate_source_columns


def create_landing_and_bronze_objects(
    spark: SparkSession,
    config: ProjectConfig,
    volume_name: str = "arquivos",
) -> None:
    """Cria schemas e o Volume necessários para a ingestão."""
    landing_schema = config.schema("landing")
    bronze_schema = config.schema("bronze")

    spark.sql(
        f"CREATE SCHEMA IF NOT EXISTS "
        f"`{config.catalog}`.`{landing_schema}`"
    )
    spark.sql(
        f"CREATE SCHEMA IF NOT EXISTS "
        f"`{config.catalog}`.`{bronze_schema}`"
    )
    spark.sql(
        f"CREATE VOLUME IF NOT EXISTS "
        f"`{config.catalog}`.`{landing_schema}`.`{volume_name}`"
    )


def read_excel_with_auto_loader(
    spark: SparkSession,
    source_path: str,
    schema_location: str,
) -> DataFrame:
    """Lê somente arquivos Excel ainda não processados."""
    return (
        spark.readStream
        .format("cloudFiles")
        .option("cloudFiles.format", "excel")
        .option("cloudFiles.inferColumnTypes", "false")
        .option("cloudFiles.schemaLocation", schema_location)
        .option("cloudFiles.schemaEvolutionMode", "none")
        .option("headerRows", 1)
        .load(source_path)
    )


def prepare_bronze_dataframe(
    source_df: DataFrame,
    environment: str,
) -> DataFrame:
    """Padroniza nomes e adiciona metadados técnicos."""
    validate_source_columns(source_df.columns)

    with_source_file = source_df.withColumn(
        "_source_file",
        F.col("_metadata.file_path"),
    )
    bronze_df = with_source_file.toDF(
        *BRONZE_COLUMNS,
        "_source_file",
    )

    return (
        bronze_df
        .withColumn("_ingestion_timestamp", F.current_timestamp())
        .withColumn("_ingestion_date", F.current_date())
        .withColumn("_environment", F.lit(environment))
    )


def write_bronze_incrementally(
    bronze_df: DataFrame,
    target_table: str,
    checkpoint_location: str,
) -> None:
    """Grava novos arquivos em Delta e encerra ao concluir o lote disponível."""
    query = (
        bronze_df.writeStream
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", checkpoint_location)
        .trigger(availableNow=True)
        .toTable(target_table)
    )
    query.awaitTermination()


def run_landing_to_bronze(
    spark: SparkSession,
    config: ProjectConfig,
    volume_name: str = "arquivos",
) -> None:
    """Executa a ingestão completa da Landing Zone para Bronze."""
    create_landing_and_bronze_objects(spark, config, volume_name)

    source_path = config.volume_path(
        volume_name,
        "veiculos_subtraidos",
    )
    schema_location = config.volume_path(
        volume_name,
        "_schemas/veiculos_subtraidos_bronze",
    )
    checkpoint_location = config.volume_path(
        volume_name,
        "_checkpoints/veiculos_subtraidos_bronze",
    )
    target_table = config.table(
        "bronze",
        "veiculos_subtraidos",
    )

    source_df = read_excel_with_auto_loader(
        spark,
        source_path,
        schema_location,
    )
    bronze_df = prepare_bronze_dataframe(
        source_df,
        config.environment,
    )
    write_bronze_incrementally(
        bronze_df,
        target_table,
        checkpoint_location,
    )
