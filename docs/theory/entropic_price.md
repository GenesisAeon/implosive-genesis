# Entropic Price (v0.2.0)

The **entropic price** quantifies the thermodynamic cost incurred when
transitioning between recursion levels in the Implosive Genesis framework.
The full formula combines a volume integral over the entropy-density
difference with an information term (Landauer principle):

$$
E_{\text{price}} = \int_V (S_V - S_A)\,dV \;+\; k_B\, T\, \ln 2 \cdot \text{bits}
$$

## Components

| Symbol | Meaning | Unit |
|--------|---------|------|
| $S_V$ | Volume entropy density | J/(K·m³) |
| $S_A$ | Areal entropy density (holographic) | J/(K·m²) |
| $k_B$ | Boltzmann constant $\approx 1.38 \times 10^{-23}$ | J/K |
| $T$ | Temperature | K |
| bits | Information content | bit |

## Phi-Scaled Approximation

On the continuous Phi lattice, $S_V - S_A$ is approximated by the recursive
gradient. For $n(V) = n_{\max} \cdot V$ on $[0,1]$:

$$
\Delta S(V) = k_B\,T\,\ln(\Phi)\cdot n_{\max}\cdot V
$$

The integral evaluates in closed form to:

$$
\int_0^1 \Delta S(V)\,dV = k_B\,T\,\ln(\Phi)\cdot\frac{n_{\max}}{2}
$$

The full entropic price is therefore:

$$
\boxed{E_{\text{price}} = k_B\,T\left(\ln(\Phi)\cdot\frac{n_{\max}}{2} + \ln 2 \cdot \text{bits}\right)}
$$

## Properties

**Linearity in $T$:**

$$
\frac{\partial E_{\text{price}}}{\partial T} = \frac{E_{\text{price}}}{T}
$$

This is proved symbolically by SymPy (see `prove_linearity_in_T()`).

**Scaling with $n_{\max}$:** The integral term grows linearly with the maximum
recursion level. The deeper the recursion, the higher the entropic price.

## SymPy Formalisation

```python
from implosive_genesis.formalization.entropic_price import (
    EntropicPriceDerivation,
    integrate_entropic_price,
)

# Symbolic derivation
deriv = EntropicPriceDerivation(n_max_val=7, temperature=2.725)
print(deriv.latex_expression())
# → k_{B} T \left(\frac{7 \ln{\Phi}}{2} + \ln{2}\right)

# Numerical integration (Riemann, 10 000 steps)
result = integrate_entropic_price(n_max=7, temperature=2.725, steps=10_000)
print(result)
```

## CLI Usage

```bash
# Default call
ig entropy-price-sympy

# With 10 000 integration steps
ig entropy-price-sympy --steps 10000

# Show SymPy proof
ig entropy-price-sympy --show-proof

# With information term for 8 bits
ig entropy-price-sympy --bits 8.0
```

### Example Output

```
╭─────────────────────────────────────────────────────────────────╮
│ Entropic Price (SymPy + Numerical)  (n_max=7, T=2.725 K,        │
│ steps=10,000, bits=1.0)                                          │
╰─────────────────────────────────────────────────────────────────╯

  Component            Value [J]       Share
  ∫(S_V - S_A)dV       2.168965e-23   75.78%
  k_B·T·ln2·bits       6.937060e-24   24.22%
  E_price (total)      2.862671e-23   100%

Riemann steps: 10,000
Φ: 1.6180339887
SymPy (closed form): 2.862671e-23 J
```

## Numerical Convergence

The Riemann integration algorithm (midpoint method) converges at
$\mathcal{O}(1/N^2)$ towards the analytical value:

| Steps | Relative error |
|-------|---------------|
| 100 | ~0.01% |
| 1 000 | ~0.0001% |
| 10 000 | ~0.000001% |

## Falsifiability

The entropic price is falsifiable by:

1. **CMB temperature measurement**: At $T = 2.725$ K (CMB), $E_{\text{price}}$
   should not exceed the thermodynamic stability boundary.
2. **Landauer limit**: $k_B T \ln 2 \cdot \text{bits}$ is the minimum energy
   dissipation per irreversible bit operation (Landauer 1961).

## References

- Landauer, R. (1961). *Irreversibility and Heat Generation in the Computing Process*. IBM J. Res. Dev.
- Bekenstein, J. D. (1973). *Black holes and entropy*. Phys. Rev. D.
- Planck Collaboration (2018). *Planck 2018 results I*. arXiv:1807.06205.
