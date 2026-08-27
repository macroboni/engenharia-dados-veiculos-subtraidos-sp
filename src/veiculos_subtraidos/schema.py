"""Schema posicional da fonte de veículos subtraídos."""

from collections.abc import Sequence


BRONZE_COLUMNS = (
    "ID_DELEGACIA",
    "NOME_DEPARTAMENTO",
    "NOME_SECCIONAL",
    "NOME_DELEGACIA",
    "NOME_MUNICIPIO",
    "ANO_BO",
    "NUM_BO",
    "VERSAO",
    "CIDADE_REGISTRO",
    "NOME_DEPARTAMENTO_CIRC",
    "NOME_SECCIONAL_CIRC",
    "NOME_DELEGACIA_CIRC",
    "NOME_MUNICIPIO_CIRC",
    "DATA_OCORRENCIA_BO",
    "HORA_OCORRENCIA",
    "DESCRICAO_APRESENTACAO",
    "DATAHORA_REGISTRO_BO",
    "DATA_COMUNICACAO_BO",
    "DATAHORA_IMPRESSAO_BO",
    "DESCR_PERIODO",
    "AUTORIA_BO",
    "FLAG_INTOLERANCIA",
    "TIPO_INTOLERANCIA",
    "FLAG_FLAGRANTE",
    "FLAG_STATUS",
    "DESC_LEI",
    "FLAG_ATO_INFRACIONAL",
    "RUBRICA",
    "DESCR_CONDUTA",
    "DESDOBRAMENTO",
    "CIRCUNSTANCIA",
    "DESCR_TIPOLOCAL",
    "DESCR_SUBTIPOLOCAL",
    "CIDADE_OCORRENCIA",
    "BAIRRO",
    "CEP",
    "DESC_NATUREZA_LOCAL",
    "LOGRADOURO_VERSAO",
    "LOGRADOURO",
    "NUMERO_LOGRADOURO",
    "LATITUDE",
    "LONGITUDE",
    "CONT_VEICULO",
    "DESCR_OCORRENCIA_VEICULO",
    "DESCR_TIPO_VEICULO",
    "DESCR_MARCA_VEICULO",
    "ANO_FABRICACAO",
    "ANO_MODELO",
    "PLACA_VEICULO",
    "DESC_COR_VEICULO",
    "MES",
    "ANO",
    "CMD",
    "BTL",
    "CIA",
    "CD_IBGE",
)


def validate_source_columns(source_columns: Sequence[str]) -> None:
    """Interrompe a carga quando a quantidade de colunas muda."""
    expected = len(BRONZE_COLUMNS)
    received = len(source_columns)
    if received != expected:
        raise ValueError(
            "Schema inesperado na fonte: "
            f"esperadas {expected} colunas, recebidas {received}."
        )
