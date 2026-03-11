# Anesthesia Tests – Frame-Buffer Simulation During Loss of Consciousness

The **anesthesia simulation** models the stepwise collapse of the frame buffer
during loss of consciousness (anesthesia state) within the Implosive Genesis
framework. It quantifies when and how the recursive field medium falls below
the anesthesia threshold.

---

## Concept

In the V_RIG framework, consciousness is modelled as a coherent frame buffer:
a set of $N$ frame amplitudes $F_i$ whose mean $\Phi_{buf}$ must remain above
the **anesthesia threshold** $\Theta_{anes}$:

$$\Phi_{buf} = \frac{1}{N} \sum_{i=0}^{N-1} F_i$$

$$\text{conscious} \iff \Phi_{buf} > \Theta_{anes}$$

---

## Physical Modelling

### Medium Decay Curve

The neural medium is modelled as an exponentially decaying system:

$$M(t) = M_0 \cdot \exp\!\left(-\frac{t}{\tau_M}\right)$$

$$\Delta M(t) = M_0 \cdot \left(1 - \exp\!\left(-\frac{t}{\tau_M}\right)\right)$$

where $\tau_M$ is the characteristic time constant of the medium.

### Anesthesia Threshold

The threshold follows directly from the OIPK parameters:

$$\Theta_{anes} = \frac{\alpha_\Phi}{\Phi^2} = \frac{1}{S_F} \approx 0.004504$$

Since $S_F = \Phi^2 / \alpha_\Phi \approx 221.9$, the threshold is very low –
consciousness is robust against small fluctuations.

### Frame Coherence Loss

Total coherence loss after duration $T$:

$$R_{loss} = 1 - \exp\!\left(-\frac{T}{\tau_M}\right)$$

### Recovery Rate

Recovery after anesthesia follows a Phi-extended time constant:

$$R_{rec} = \exp\!\left(-\frac{T}{\tau_M \cdot \Phi}\right)$$

The Phi-scaling reflects the geometrically optimised recovery profile:
recovery is slower than loss, which explains physiologically observed
wake-up phases.

---

## Simulation Flow

```
t=0: buffer empty → Φ_buf = 0 (anesthesia)
t→: M(t) inserted → buffer fills
    while Φ_buf ≤ Θ_anes: anesthesia event active
    once  Φ_buf > Θ_anes: recovery, event closed
```

---

## API Reference

```python
from implosive_genesis.medium.modulation import (
    MediumModulator,
    run_anesthesia_test,
    ANESTHESIA_THRESHOLD,
    FRAME_BUFFER_SIZE,
)

# Default test (5 minutes, τ_M = 120 s)
result = run_anesthesia_test(duration=300.0)
print(result.summary())

# Custom parameters
mod = MediumModulator(tau_m=60.0)
result = mod.run_anesthesia_simulation(duration=600.0, dt=0.5)
print(f"Events: {result.n_events()}")
print(f"Conscious fraction: {result.consciousness_fraction():.4f}")

# Frame buffer directly
from implosive_genesis.medium.modulation import FrameBuffer
buf = FrameBuffer(size=64)
buf.push(0.9)
print(buf.is_conscious())  # True
```

### CLI

```bash
# Default test (300 s)
ig anesthesia-test

# Custom parameters
ig anesthesia-test --duration 600 --tau-m 60

# With time series
ig anesthesia-test --duration 300 --timeline
```

---

## Parameter Overview

| Parameter | Symbol | Default | Description |
|-----------|--------|---------|-------------|
| Duration | $T$ | 300 s | Test length |
| Time constant | $\tau_M$ | 120 s | Medium decay τ |
| Time step | $\Delta t$ | 1 s | Simulation resolution |
| Buffer size | $N$ | 64 | Frame buffer capacity |
| Threshold | $\Theta_{anes}$ | ≈ 0.004504 | Anesthesia boundary |

---

## Relationship to Other Modules

```
MediumModulator
  └── FrameBuffer             (ring buffer for frame amplitudes)
        ↕
  ANESTHESIA_THRESHOLD        (from OIPK: α_Φ / Φ² = 1/S_F)
        ↕
  OIPKKernel                  (oipk/kernel.py)
        ↕
  FramePrinciple              (theory/frameprinciple.py)
```

---

## Reference

- Module: `implosive_genesis.medium.modulation`
- CLI: `ig anesthesia-test`
- Related concepts: [OIPK](oipk.md), [Frame Principle](frameprinciple.md)
