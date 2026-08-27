import pytest

from veiculos_subtraidos.schema import (
    BRONZE_COLUMNS,
    validate_source_columns,
)


def test_schema_bronze_possui_56_colunas() -> None:
    assert len(BRONZE_COLUMNS) == 56


def test_schema_bronze_nao_possui_nomes_duplicados() -> None:
    assert len(BRONZE_COLUMNS) == len(set(BRONZE_COLUMNS))


def test_cidades_duplicadas_na_fonte_recebem_nomes_distintos() -> None:
    assert BRONZE_COLUMNS[8] == "CIDADE_REGISTRO"
    assert BRONZE_COLUMNS[33] == "CIDADE_OCORRENCIA"


def test_valida_quantidade_correta_de_colunas() -> None:
    validate_source_columns([f"coluna_{index}" for index in range(56)])


@pytest.mark.parametrize("column_count", [0, 55, 57, 59])
def test_rejeita_mudanca_na_quantidade_de_colunas(
    column_count: int,
) -> None:
    with pytest.raises(ValueError, match="Schema inesperado"):
        validate_source_columns(
            [f"coluna_{index}" for index in range(column_count)]
        )
