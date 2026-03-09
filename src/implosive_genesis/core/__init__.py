"""Implosive Genesis – mathematischer Kern: Phi-Skalierung, V_RIG, Type-6."""

from .physics import PHI, PhiScaling
from .type6 import Type6Implosive, cubic_root_jump, inverted_sigmoid
from .vrig import COSMIC_ALPHA, V_RIG_KMS, VRIGResult, compute_vrig, cosmic_alpha_phi

__all__ = [
    "PHI",
    "PhiScaling",
    "COSMIC_ALPHA",
    "V_RIG_KMS",
    "VRIGResult",
    "compute_vrig",
    "cosmic_alpha_phi",
    "Type6Implosive",
    "cubic_root_jump",
    "inverted_sigmoid",
]
