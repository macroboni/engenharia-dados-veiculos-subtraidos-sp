"""Configurações centralizadas do projeto."""

from dataclasses import dataclass


VALID_ENVIRONMENTS = frozenset({"hml", "prod"})
VALID_LAYERS = frozenset({"landing", "bronze", "silver", "gold"})


@dataclass(frozen=True)
class ProjectConfig:
    """Constrói nomes padronizados para objetos do Unity Catalog."""

    catalog: str = "workspace"
    environment: str = "hml"
    domain: str = "veiculos"

    def __post_init__(self) -> None:
        if self.environment not in VALID_ENVIRONMENTS:
            valid_values = ", ".join(sorted(VALID_ENVIRONMENTS))
            raise ValueError(
                f"Ambiente inválido: {self.environment}. Use um destes: {valid_values}."
            )

    def schema(self, layer: str) -> str:
        """Retorna o schema de uma camada para o ambiente atual."""
        if layer not in VALID_LAYERS:
            valid_values = ", ".join(sorted(VALID_LAYERS))
            raise ValueError(
                f"Camada inválida: {layer}. Use uma destas: {valid_values}."
            )
        return f"{self.domain}_{self.environment}_{layer}"

    def table(self, layer: str, table_name: str) -> str:
        """Retorna o nome completo de uma tabela."""
        return f"{self.catalog}.{self.schema(layer)}.{table_name}"

    def volume_path(self, volume: str, relative_path: str = "") -> str:
        """Retorna o caminho de um Volume na Landing Zone."""
        base_path = (
            f"/Volumes/{self.catalog}/{self.schema('landing')}/{volume}"
        )
        clean_path = relative_path.strip("/")
        return f"{base_path}/{clean_path}" if clean_path else base_path
