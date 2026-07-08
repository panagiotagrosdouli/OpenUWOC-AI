# UWOC Channel Model

The implemented channel model is a simulation baseline for intensity-modulation/direct-detection underwater optical links.

## Implemented

- Absorption coefficient `a(lambda)` via water-profile presets.
- Scattering coefficient `b(lambda)` via water-profile presets.
- Beam attenuation `c(lambda)=a(lambda)+b(lambda)`.
- Beer-Lambert gain `exp(-c d)`.
- Gaussian pointing-error loss.
- Thermal noise.
- Gaussian shot-noise approximation.
- Ambient light offset.

## Prototype

- Lognormal weak-turbulence gain.

## Planned

- Validated multipath impulse response.
- Wavelength-dependent coefficient tables from literature and measurements.
- Site-specific calibration workflows.
- Time-varying AUV/ROV pointing dynamics.

## Limitation

The presets are not experimental measurements. They are provided for reproducible software testing and preliminary simulation only.
