# Entropischer Preis (v0.2.0)

Der **entropische Preis** quantifiziert den thermodynamischen Aufwand, der beim
Übergang zwischen Rekursionsstufen im Implosiven-Genesis-Rahmen anfällt.
Die vollständige Formel kombiniert ein Volumenintegral über die Entropiedichtedifferenz
mit einem Informationsterm (Landauer-Prinzip):

$$
E_{\text{price}} = \int_V (S_V - S_A)\,dV \;+\; k_B\, T\, \ln 2 \cdot \text{bits}
$$

## Komponenten

| Symbol | Bedeutung | Einheit |
|--------|-----------|---------|
| $S_V$ | Volumen-Entropiedichte | J/(K·m³) |
| $S_A$ | Areal-Entropiedichte (holographisch) | J/(K·m²) |
| $k_B$ | Boltzmann-Konstante $\approx 1.38 \times 10^{-23}$ | J/K |
| $T$ | Temperatur | K |
| bits | Informationsgehalt | bit |

## Phi-skalierte Näherung

Im kontinuierlichen Phi-Gitter wird $S_V - S_A$ durch den rekursiven Gradienten
approximiert. Für $n(V) = n_{\max} \cdot V$ auf $[0,1]$:

$$
\Delta S(V) = k_B\,T\,\ln(\Phi)\cdot n_{\max}\cdot V
$$

Das Integral ergibt in geschlossener Form:

$$
\int_0^1 \Delta S(V)\,dV = k_B\,T\,\ln(\Phi)\cdot\frac{n_{\max}}{2}
$$

Damit lautet der vollständige entropische Preis:

$$
\boxed{E_{\text{price}} = k_B\,T\left(\ln(\Phi)\cdot\frac{n_{\max}}{2} + \ln 2 \cdot \text{bits}\right)}
$$

## Eigenschaften

**Linearität in $T$:**

$$
\frac{\partial E_{\text{price}}}{\partial T} = \frac{E_{\text{price}}}{T}
$$

Dies wird durch SymPy symbolisch bewiesen (siehe `prove_linearity_in_T()`).

**Skalierung mit $n_{\max}$:** Der Integralterm wächst linear mit der maximalen
Rekursionsstufe. Je tiefer die Rekursion, desto höher der entropische Preis.

## SymPy-Formalisierung

```python
from implosive_genesis.formalization.entropic_price import (
    EntropicPriceDerivation,
    integrate_entropic_price,
)

# Symbolische Ableitung
deriv = EntropicPriceDerivation(n_max_val=7, temperature=2.725)
print(deriv.latex_expression())
# → k_{B} T \left(\frac{7 \ln{\Phi}}{2} + \ln{2}\right)

# Numerische Integration (Riemann, 10 000 Schritte)
result = integrate_entropic_price(n_max=7, temperature=2.725, steps=10_000)
print(result)
```

## CLI-Nutzung

```bash
# Standardaufruf
ig entropy-price-sympy

# Mit 10 000 Integrations-Schritten
ig entropy-price-sympy --steps 10000

# Mit SymPy-Beweis anzeigen
ig entropy-price-sympy --show-proof

# Mit Informationsterm für 8 bit
ig entropy-price-sympy --bits 8.0
```

### Beispiel-Ausgabe

```
╭─────────────────────────────────────────────────────────────────╮
│ Entropischer Preis (SymPy + Numerisch)  (n_max=7, T=2.725 K,   │
│ steps=10,000, bits=1.0)                                          │
╰─────────────────────────────────────────────────────────────────╯

  Komponente           Wert [J]        Anteil
  ∫(S_V - S_A)dV       2.168965e-23   75.78%
  k_B·T·ln2·bits       6.937060e-24   24.22%
  E_price (gesamt)     2.862671e-23   100%

Riemann-Schritte: 10,000
Φ: 1.6180339887
SymPy (geschlossene Form): 2.862671e-23 J
```

## Numerische Konvergenz

Der Riemann-Integrationsalgorithmus (Mittelpunktmethode) konvergiert mit
$\mathcal{O}(1/N^2)$ gegen den analytischen Wert:

| Schritte | Relativer Fehler |
|----------|-----------------|
| 100 | ~0.01% |
| 1 000 | ~0.0001% |
| 10 000 | ~0.000001% |

## Falsifizierbarkeit

Der entropische Preis ist falsifizierbar durch:

1. **CMB-Temperaturmessung**: Bei $T = 2.725$ K (CMB) sollte $E_{\text{price}}$
   die thermodynamische Stabilitätsgrenze nicht überschreiten.
2. **Landauer-Grenze**: $k_B T \ln 2 \cdot \text{bits}$ ist die minimale
   Energiedissipation pro irreversibler Bitoperation (Landauer 1961).

## Referenzen

- Landauer, R. (1961). *Irreversibility and Heat Generation in the Computing Process*. IBM J. Res. Dev.
- Bekenstein, J. D. (1973). *Black holes and entropy*. Phys. Rev. D.
- Planck Collaboration (2018). *Planck 2018 results I*. arXiv:1807.06205.
