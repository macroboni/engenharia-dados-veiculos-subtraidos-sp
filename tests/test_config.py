import pytest

from veiculos_subtraidos.config import ProjectConfig


def test_schema_por_ambiente_e_camada() -> None:
    config = ProjectConfig(environment="hml")

    assert config.schema("bronze") == "veiculos_hml_bronze"
    assert config.schema("silver") == "veiculos_hml_silver"
    assert config.schema("gold") == "veiculos_hml_gold"


def test_nome_completo_da_tabela() -> None:
    config = ProjectConfig(catalog="workspace", environment="prod")

    assert (
        config.table("silver", "ocorrencias")
        == "workspace.veiculos_prod_silver.ocorrencias"
    )


def test_caminho_da_landing_zone() -> None:
    config = ProjectConfig(catalog="workspace", environment="hml")

    assert config.volume_path(
        "arquivos", "veiculos_subtraidos/2024"
    ) == (
        "/Volumes/workspace/veiculos_hml_landing/"
        "arquivos/veiculos_subtraidos/2024"
    )


@pytest.mark.parametrize("environment", ["dev", "qa", "producao"])
def test_rejeita_ambiente_invalido(environment: str) -> None:
    with pytest.raises(ValueError, match="Ambiente inválido"):
        ProjectConfig(environment=environment)


def test_rejeita_camada_invalida() -> None:
    config = ProjectConfig()

    with pytest.raises(ValueError, match="Camada inválida"):
        config.schema("raw")
