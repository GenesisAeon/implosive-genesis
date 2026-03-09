# Beispiele

Praktische Anwendungsbeispiele für alle Kernkomponenten von Implosive Genesis.

---

## Schnellstart: Neues Projekt

```bash
pip install implosive-genesis

# Minimales Projekt
ig scaffold my-experiment
cd my-experiment && uv sync --dev && uv run pytest

# Genesis-Preset (mit Entropietabellen und Domains)
ig scaffold my-physics-tool --template genesis --author "Ada Lovelace"
```

---

## Phi-Skalierung

```python
from implosive_genesis.core.physics import PHI, PhiScaling

# Goldener Schnitt
print(f"Φ = {PHI:.10f}")  # 1.6180339887

# Kopplungsparameter-Skalierung
scaler = PhiScaling(beta_0=1.0)
for n in range(6):
    beta = scaler.beta_n(n)
    waste = scaler.geometric_waste(n)
    print(f"n={n}: β_n={beta:.4f}, W(n)={waste:.4f}")
```

**Ausgabe:**
```
n=0: β_n=1.0000, W(n)=0.0000
n=1: β_n=1.1677, W(n)=0.1434
n=2: β_n=1.3629, W(n)=0.2665
n=3: β_n=1.6180, W(n)=0.3820
n=4: β_n=1.8899, W(n)=0.4707
n=5: β_n=2.2058, W(n)=0.5466
```

---

## V_RIG-Berechnung mit Monte-Carlo

```python
from implosive_genesis.core.vrig import compute_vrig, cosmic_alpha_phi

# Phi-skalierte Feinstrukturkonstante
alpha_phi = cosmic_alpha_phi()
print(f"α_Φ = {alpha_phi:.8f}")  # ≈ 0.01180450

# V_RIG mit reproduzierbarer Monte-Carlo-Simulation
result = compute_vrig(beta_0=1.0, n=3, samples=50_000, seed=42)
print(result)
# → V_RIG = 2187.3412 ± 12.0231 km/s  (α_Φ = 0.01180450, n=50000)
```

---

## Frame-Prinzip und OIPK

```python
from implosive_genesis.theory.frameprinciple import OIPKernel, FramePrinciple

# Standard-OIPK (λ aus V_RIG abgeleitet)
kernel = OIPKernel()
print(f"ω_F  = {kernel.angular_frequency():.4e} rad/s")
print(f"E    = {kernel.energy():.4e} J")
print(f"S_F  = {kernel.frame_stability():.2f}")
print(f"θ_⊥  = {kernel.orthogonality_angle_deg():.4f}°")

# Rekursive Größen über Frame-Prinzip
fp = FramePrinciple(kernel=kernel)
print("\nRekursive Kohärenzlängen und Impulsenergien:")
for n in range(5):
    L = fp.coherence_length(n)
    I = fp.impulse_energy(n)
    S = fp.stability_at(n)
    print(f"  n={n}: L={L:.3e} m, I={I:.3e} J, S_F={S:.2f}")
```

---

## Tesseract-Zeitscheiben

```python
from implosive_genesis.theory.tesseract import Tesseract

ts = Tesseract(t_0=1.0)

print("Zeitscheiben und 4D-Volumen:")
for n in range(6):
    T = ts.time_slice(n)
    V = ts.volume_4d(n)
    f = ts.resonance_frequency(n)
    print(f"  n={n}: T_n={T:.4f}, V_4D={V:.4f}, f_R={f:.4e} Hz")
```

**Ausgabe:**
```
Zeitscheiben und 4D-Volumen:
  n=0: T_n=1.0000, V_4D=1.0000, f_R=1.3520e+06 Hz
  n=1: T_n=1.6180, V_4D=6.8541, f_R=8.3559e+05 Hz
  n=2: T_n=2.6180, V_4D=46.979, f_R=5.1643e+05 Hz
  n=3: T_n=4.2361, V_4D=321.99, f_R=3.1930e+05 Hz
  n=4: T_n=6.8541, V_4D=2207.1, f_R=1.9737e+05 Hz
  n=5: T_n=11.090, V_4D=15126., f_R=1.2192e+05 Hz
```

---

## CREP – Entropischer Preis

```python
from implosive_genesis.theory.tesseract import CREP

crep = CREP()

# CREP-Wert für normierte Gesamtentropie
print(f"CREP(S=1) = {crep.crep_value(s_total=1.0):.4e}")

# Entropischer Preis bei verschiedenen Temperaturen
print("\nEntropischer Preis P_E(n) bei T_CMB = 2.725 K:")
for n in range(1, 6):
    price = crep.entropy_price(n=n, temperature=2.725)
    print(f"  n={n}: P_E = {price:.4e} J")

# Bei Zimmertemperatur
print("\nEntropischer Preis P_E(n) bei T = 300 K:")
prices = crep.entropy_price_series(n_max=5, temperature=300.0)
for n, p in enumerate(prices, 1):
    print(f"  n={n}: P_E = {p:.4e} J")
```

---

## Vollständiges Modell

```python
from implosive_genesis.theory.models import ImplosiveGenesisModel

model = ImplosiveGenesisModel()

# Vollzusammenfassung für Stufe n=3 bei CMB-Temperatur
summary = model.full_summary(n=3, temperature=2.725)
print(summary)
```

---

## Projektvalidierung

```python
from implosive_genesis.validator import validate_project

# Aktuelles Verzeichnis validieren
result = validate_project(".")

if result.is_valid:
    print("Projekt ist valide.")
else:
    print("Fehler gefunden:")
    for error in result.errors:
        print(f"  [ERROR] {error}")

for warning in result.warnings:
    print(f"  [WARN]  {warning}")
```

Oder über die CLI:

```bash
ig validate my-project/
```

---

## Simulation: Entropiesteuerung

```python
from implosive_genesis.simulation.entropy_governance import EntropyGovernor

gov = EntropyGovernor(n_max=10)
gov.run()
gov.report()
```

---

## Jupyter-Integration

```python
# In einem Jupyter-Notebook:
from implosive_genesis.core.physics import PHI, PhiScaling
import matplotlib.pyplot as plt

scaler = PhiScaling()
ns = range(0, 10)
betas = [scaler.beta_n(n) for n in ns]
wastes = [scaler.geometric_waste(n) for n in ns]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.plot(ns, betas, "o-", label=r"$\beta_n$")
ax1.set_xlabel("Rekursionsstufe n")
ax1.set_ylabel(r"$\beta_n$")
ax1.set_title(r"Phi-Skalierung $\beta_n = \beta_0 \cdot \Phi^{n/3}$")
ax1.legend()

ax2.plot(ns, wastes, "s-", color="orange", label=r"$W(n)$")
ax2.set_xlabel("Rekursionsstufe n")
ax2.set_ylabel("Verschnitt W(n)")
ax2.set_title(r"Geometrischer Verschnitt $W(n) = 1 - 1/\Phi^{n/3}$")
ax2.legend()

plt.tight_layout()
plt.show()
```
