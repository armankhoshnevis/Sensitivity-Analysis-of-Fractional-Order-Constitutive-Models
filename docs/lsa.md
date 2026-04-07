# Local Sensitivity Analysis (LSA)

Local Sensitivity Analysis (LSA) evaluates how uncertainty in model output is apportioned to specific sources of uncertainty in the model input, focused around a nominal parameter value. This analysis is vital for determining factor prioritization—quantifying the contribution of model inputs to output uncertainty—and factor fixing, which identifies non-influential parameters that can be treated deterministically.

## Methodology

The framework utilizes partial derivatives as local sensitivity measures. To allow for direct comparison between parameters with different physical units and magnitudes, indices are normalized as follows:

$$\overline{S}_{E',q_{i}} = \frac{q_{i}^{0}}{E'(q^{0};x)} \cdot \frac{\partial E'(q^{0};x)}{\partial q_{i}}$$

$$\overline{S}_{E'',q_{i}} = \frac{q_{i}^{0}}{E''(q^{0};x)} \cdot \frac{\partial E''(q^{0};x)}{\partial q_{i}}$$

Where $q_{i}^{0}$ represents the realized baseline value of the $i$-th parameter.

### Complex Modulus Magnitude
To simplify prioritization by considering both storage and loss moduli simultaneously, the magnitude of the normalized local sensitivity index for the complex modulus is calculated:

$$|\overline{S}_{E^{*},q_{i}}| = \frac{q_{i}^{0}}{|E^{*}(q^{0};x)|} \cdot \sqrt{\left(\frac{\partial E'(q^{0};x)}{\partial q_{i}}\right)^{2} + \left(\frac{\partial E''(q^{0};x)}{\partial q_{i}}\right)^{2}}$$

### Quantitative Assessment via Norms
Because sensitivity indices vary across the frequency domain, we employ $L_1$ norm to evaluate total parameter significance:

$$\|\overline{S}_{E',q_{i}}\|_{L_{1}} = \int |\overline{S}_{E',q_{i}}| d \log(a_{T}\omega)$$

## Parameter Prioritization Results
Based on the local sensitivity analysis, parameters are prioritized by their impact on model variability:

| **Model** | **Least influential parameters** | **Most influential parameters** |
| :--- | :--- | :--- |
| FMG-FMG | $\tau_{c_{2}}$ <br> — | $\alpha_{1}$ <br> $E_{c_{1}}$ |
| FMM-FMG | $\tau_{c_{2}}$ <br> $\beta_{1}$ | $\alpha_{1}$ <br> $E_{c_{1}}$ |