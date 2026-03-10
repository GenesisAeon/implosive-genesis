"""Vollständige 10-Teile-Chronologie-Integration – Mapping aller V_RIG-Module.

Dieses Paket enthält den Chronologie-Validator, der alle 10 Teile des
ursprünglichen Implosive-Genesis-Dokuments als Code-Validator abbildet
und mit den Implementierungsmodulen verknüpft.
"""

from .integration import (
    ChronologyPart,
    ChronologyResult,
    ChronologyValidator,
    CHRONOLOGY_PARTS,
)

__all__ = [
    "ChronologyPart",
    "ChronologyResult",
    "ChronologyValidator",
    "CHRONOLOGY_PARTS",
]
