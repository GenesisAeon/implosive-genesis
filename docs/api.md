# API Reference

Complete reference for all public modules and classes of Implosive Genesis.

---

## `implosive_genesis.core.physics`

### Constant `PHI`

```python
PHI: float  # ≈ 1.6180339887
```

The golden ratio $\Phi = \frac{1 + \sqrt{5}}{2}$.

### Class `PhiScaling`

Phi-scaled coupling parameter with minimised geometric waste.

```python
from implosive_genesis.core.physics import PhiScaling

scaler = PhiScaling(beta_0=1.0)

scaler.beta_n(n=3)           # β_3 = β_0 · Φ^(3/3) ≈ 1.618
scaler.geometric_waste(n=3)  # W(3) = 1 − 1/Φ ≈ 0.382
scaler.beta_series(n_max=5)  # [β_0, β_1, …, β_5]
scaler.waste_series(n_max=5) # [W(0), W(1), …, W(5)]
```

**Formulae:**

$$\beta_n = \beta_0 \cdot \Phi^{n/3}$$

$$W(n) = 1 - \frac{1}{\Phi^{n/3}}$$

---

## `implosive_genesis.core.vrig`

### Constants

| Name | Value | Unit |
|------|-------|------|
| `V_RIG_KMS` | `1352.0` | km/s |
| `COSMIC_ALPHA` | `1/137.035999084` | – |

### Function `cosmic_alpha_phi`

```python
from implosive_genesis.core.vrig import cosmic_alpha_phi

alpha_phi = cosmic_alpha_phi()  # α · Φ ≈ 0.011800
```

$$\alpha_\Phi = \alpha \cdot \Phi$$

### Function `compute_vrig`

```python
from implosive_genesis.core.vrig import compute_vrig

result = compute_vrig(beta_0=1.0, n=3, samples=10_000, seed=42)
print(result.v_rig)      # ≈ 2187 km/s
print(result.alpha_phi)  # ≈ 0.01180
print(result.std_dev)    # Monte-Carlo standard deviation
```

### Class `VRIGResult`

| Attribute | Type | Description |
|-----------|------|-------------|
| `v_rig` | `float` | Mean implosion velocity [km/s] |
| `alpha_phi` | `float` | Phi-scaled fine-structure constant |
| `std_dev` | `float` | Standard deviation (Monte Carlo) [km/s] |
| `samples` | `int` | Number of Monte Carlo samples |

---

## `implosive_genesis.core.type6`

Type-6 models recursive self-perception as a physical state.

```python
from implosive_genesis.core.type6 import Type6State

state = Type6State(recursion_level=3)
print(state.self_reference_index())  # S_6(n)
print(state.consciousness_density())  # ρ_6(n)
```

---

## `implosive_genesis.theory.frameprinciple`

### Class `OIPKernel`

The Orthogonal Impulse Photon Kernel – minimal photonic unit of a stable frame.

```python
from implosive_genesis.theory.frameprinciple import OIPKernel

kernel = OIPKernel(lambda_m=1e-9)         # λ_OIPK in metres
kernel.angular_frequency()                # ω_F = 2πc/λ [rad/s]
kernel.energy()                           # E = ℏ · ω_F · α_Φ [J]
kernel.frame_stability()                  # S_F = Φ²/α_Φ
kernel.orthogonality_angle_deg()          # θ_⊥ ≈ 128.17°
```

**Formulae:**

$$\omega_F = \frac{2\pi c}{\lambda_{OIPK}}$$

$$E_{OIPK} = \hbar \cdot \omega_F \cdot \alpha_\Phi$$

$$S_F = \frac{\Phi^2}{\alpha_\Phi}$$

$$\cos(\theta_\perp) = -\frac{1}{\Phi} \Rightarrow \theta_\perp \approx 128.17°$$

### Class `FramePrinciple`

Derives recursive properties at level $n$ from an `OIPKernel`.

```python
from implosive_genesis.theory.frameprinciple import FramePrinciple, OIPKernel

fp = FramePrinciple(kernel=OIPKernel())
fp.coherence_length(n=3)   # L_n = λ · Φ^(n/3) [m]
fp.impulse_energy(n=3)     # I_n = E · Φ^(n/3) [J]
fp.stability_at(n=3)       # S_F · Φ^(n/3)
```

---

## `implosive_genesis.theory.tesseract`

### Class `Tesseract`

4-dimensional time structure with Phi-scaled time slices.

```python
from implosive_genesis.theory.tesseract import Tesseract

ts = Tesseract(t_0=1.0)
ts.time_slice(n=3)          # T_n = t_0 · Φ^n
ts.volume_4d(n=3)           # V_4D = T_n^4
ts.resonance_frequency(n=3) # f_R = V_RIG / T_n [Hz]
ts.slice_series(n_max=5)    # [T_0, …, T_5]
ts.volume_series(n_max=5)   # [V_4D(0), …, V_4D(5)]
```

**Formulae:**

$$T_n = t_0 \cdot \Phi^n$$

$$V_{4D}(n) = T_n^4$$

$$f_R(n) = \frac{V_{RIG}}{T_n}$$

### Class `CREP`

Collapse-Resonance-Entropy-Price – thermodynamic cost of the implosive collapse.

```python
from implosive_genesis.theory.tesseract import CREP

crep = CREP()
crep.crep_value(s_total=1.0)               # CREP value
crep.entropy_price(n=3, temperature=2.725) # P_E [J]
crep.entropy_price_series(n_max=5, temperature=300.0)
crep.cumulative_crep([0.5, 1.0, 1.5, 2.0])
```

**Formulae:**

$$CREP = \frac{S_{total} \cdot V_{RIG}}{\Phi \cdot c^2}$$

$$P_E(n, T) = n \cdot k_B \cdot T \cdot \ln(\Phi)$$

---

## `implosive_genesis.theory.models`

### Class `ImplosiveGenesisModel`

Fully integrated model – combines all theory components.

```python
from implosive_genesis.theory.models import ImplosiveGenesisModel

model = ImplosiveGenesisModel()
summary = model.full_summary(n=3, temperature=2.725)
```

**Output:**

```
FullSummary(n=3)
  β_n            = 1.618034
  V_RIG          = 2187.34 ± 12.02 km/s
  α_Φ            = 0.01180450
  L_n            = 2.218e-04 m
  I_n            = 1.543e-27 J
  S_F(n)         = 358.90
  T_n            = 4.236068
  V_4D(n)        = 3.210e+01
  P_E(n,T)       = 1.540e-23 J  (T=2.725 K)
  CREP(S=1)      = 7.598e-12
```

---

## `implosive_genesis.simulation`

### `entropy_governance`

```python
from implosive_genesis.simulation.entropy_governance import EntropyGovernor

gov = EntropyGovernor(n_max=10)
gov.run()         # run simulation
gov.report()      # print result
```

### `cosmic_moments`

```python
from implosive_genesis.simulation.cosmic_moments import CosmicMomentSimulator

sim = CosmicMomentSimulator(steps=100)
sim.evolve()
sim.snapshot(step=50)
```

---

## `implosive_genesis.preset`

```python
from implosive_genesis.preset import load_preset, list_presets

presets = list_presets()
config = load_preset("genesis")
```

---

## `implosive_genesis.validator`

```python
from implosive_genesis.validator import validate_project

result = validate_project(path="./my-project")
result.is_valid    # bool
result.errors      # List[str]
result.warnings    # List[str]
```
