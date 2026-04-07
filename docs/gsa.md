# Global Sensitivity Analysis (GSA)

Global Sensitivity Analysis (GSA) explores model output variability by systematically altering all uncertain input parameters across their entire range. This framework employs the variance-based Sobol' method, which is a standard approach for identifying influential factors without constraints on the model form.

## Sobol' Sensitivity Indices

The framework evaluates parameter influence using two primary indices derived from the Analysis of Variances (ANOVA) decomposition.

### First-Order Index ($S_i$)
The first-order index measures the isolated main effect contribution of each input factor to the total variance of the model output:

$$S_{i} = \frac{\mathbb{V}_{q_{i}}(\mathbb{E}_{q_{\sim i}}(y|q_{i}))}{\mathbb{V}(y)}$$

### Total-Order Index ($S_{Ti}$)
The total-order index accounts for the first-order effect along with all higher-order interaction effects between the parameter and the rest of the model inputs:

$$S_{Ti} = \frac{\mathbb{E}_{q_{\sim i}}(\mathbb{V}_{q_{i}}(y|q_{\sim i}))}{\mathbb{V}(y)} = 1 - \frac{\mathbb{V}_{q_{\sim i}}(\mathbb{E}_{q_{i}}(y|q_{\sim i}))}{\mathbb{V}(y)}$$

$S_{Ti} = 0$ is a necessary and sufficient condition for a parameter to be considered non-influential. In the present study, however, $S_{Ti} \approx S_i$, indicating that the interaction effects are absolute minimal. Additionally, by considering practical implications for determining the least influential parameters, $S_i \approx 0$, or $S_i < 0.1$ is assumed to be the threshold distinguishing between influential and non-influential parameters.

## Computation and Tools

### SALib Integration
For the computationally efficient evaluation of these indices, the **SALib** Python library is utilized. This package provides robust implementations of sensitivity analysis algorithms, allowing for precise estimation of Sobol' indices via low-discrepancy sampling sequences.

## Factor Prioritization and Fixing
GSA results for the FMM-FMG and FMG-FMG models identify the following parameters:

| **Model** | **Least influential parameters** | **Most influential parameters** |
| :--- | :--- | :--- |
| FMG-FMG | $\tau_{c_{2}}$ <br> $\tau_{c_{1}}$ | $E_{c_{1}}$ <br> $\alpha_{1}$ |
| FMM-FMG | $\tau_{c_{2}}$ <br> $\beta_{1}$ <br> $\tau_{c_{1}}$ | $E_{c_{1}}$ <br> $\alpha_{1}$ |

* **Influential Parameters:** $E_{c_1}$, $\alpha_1$, and $E_{c_2}$ consistently demonstrate high sensitivity indices, requiring careful calibration.

* **Non-Influential Parameters:** $\tau_{c_2}$, $\tau_{c_1}$, and $\beta_1$ exhibit negligible effects on output variance, allowing them to be fixed deterministically to reduce problem dimensionality.