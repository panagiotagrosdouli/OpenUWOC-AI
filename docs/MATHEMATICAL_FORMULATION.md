# Mathematical Formulation

## Research question

How can AI improve the robustness, reliability, and adaptability of underwater optical wireless communication under absorption, scattering, turbulence, misalignment, and noise?

## Signal model

For an intensity-modulation/direct-detection UWOC link, binary or M-ary symbols are mapped to non-negative optical intensities

\[
x_k \in \mathcal{X}, \qquad P_t[k] = f(x_k) \ge 0.
\]

A scalar simulation baseline uses

\[
y_k = h_k P_t[k] + P_{amb} + n_{shot,k} + n_{th,k},
\]

where \(y_k\) is the received electrical/optical sample after photodetection scaling, \(P_{amb}\) is ambient-light contribution, and

\[
h_k = h_{BL}(d,\lambda) h_p(k) h_t(k).
\]

## Absorption, scattering, and attenuation

The beam attenuation coefficient is

\[
c(\lambda)=a(\lambda)+b(\lambda),
\]

where \(a\) is absorption and \(b\) is scattering. The implemented deterministic path gain is the Beer-Lambert term

\[
h_{BL}(d,\lambda)=\exp[-c(\lambda)d].
\]

The repository presets for clear ocean, coastal water, and turbid harbor water are simulation profiles only. They are not calibrated measurements.

## Pointing error

A Gaussian beam pointing-loss scaffold is implemented as

\[
h_p = \exp\left[-2\left(\frac{r}{w}\right)^2\right],
\]

where \(r\) is radial misalignment and \(w\) is a beam-waist parameter.

## Turbulence

Weak irradiance fluctuations are represented by a unit-mean lognormal scaffold:

\[
h_t \sim \mathrm{LogNormal}\left(-\frac{\sigma^2}{2},\sigma^2\right).
\]

This is a prototype model, not a validated underwater turbulence model.

## Noise

Thermal noise is modeled as

\[
n_{th,k} \sim \mathcal{N}(0,\sigma_{th}^2).
\]

Shot noise is approximated by a Gaussian variance proportional to received optical power:

\[
n_{shot,k} \sim \mathcal{N}(0,\alpha \max(h_k P_t[k],0)).
\]

## Metrics

Bit error rate is

\[
\mathrm{BER}=\frac{1}{N}\sum_{k=1}^{N}\mathbf{1}\{\hat{b}_k\ne b_k\}.
\]

For reporting uncertainty, the implemented metric module includes a Wilson score interval for error probability estimates.

## AI receiver

A neural equalizer can be written as

\[
\hat{b}_k = \mathbf{1}\{g_\theta(\mathbf{y}_{k-L:k+L}) \ge \tau\},
\]

where \(g_\theta\) is trained on simulation-generated or measured datasets. In this repository, neural receivers are prototypes until benchmarked against classical threshold, matched-filter, and linear-equalizer baselines.

## Adaptive transmission

A future adaptive modulation policy can be formulated as

\[
\pi_\phi(s_t) \rightarrow m_t,
\]

where the state \(s_t\) may include estimated channel gain, turbidity class, SNR, pointing error, and recent BER, while \(m_t\) is a modulation/coding/power action. This is currently planned/prototype functionality.
