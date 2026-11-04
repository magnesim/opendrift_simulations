# OpenDrift Radionuclide & Surface Drift Simulations (NMBU-RAD320)

This repository provides example scripts for simulating oceanic drift and radionuclide dispersion in Norwegian coastal waters using [OpenDrift](https://opendrift.github.io). It is designed as educational material and practical exercises for students in the **RAD320** course (Radioecology) at the Norwegian University of Life Sciences (**NMBU**).

---

## Overview

The exercises demonstrate how Lagrangian particle tracking models simulate the transport, vertical mixing, speciation, and concentration of radioactive contaminants and surface drifters in the marine environment. The simulations utilize operational ocean model data (Norkyst) retrieved directly via OPeNDAP from the Norwegian Meteorological Institute (MET Norway) THREDDS server.

### Key Capabilities

- **Surface Drift**: Basic 2D particle tracking to study advection by ocean currents and horizontal diffusion.
- **Radionuclide Transport**: 3D particle tracking incorporating speciation (Low Molecular Mass vs. particulate fractions), vertical turbulence/mixing, and radioactive activity budgets (Becquerels).
- **Trajectory & Concentration Analysis**: Gridding Lagrangian trajectory files into volumetric activity concentrations ($\text{Bq/m}^3$), applying spatial smoothing, mapping with Cartopy, and extracting time-series at point locations.

---

## Repository Structure

```text
opendrift_simulations/
├── rad320_surface.py          # 2D surface drift simulation (OceanDrift)
├── rad320_radionuclides.py    # 3D radionuclide dispersion simulation (RadionuclideDrift)
├── rad320_trajan_analysis.py  # Trajectory analysis and concentration mapping (trajan/xarray)
├── LICENSE                    # License terms
└── README.md                  # Documentation
```

---

## Installation & Setup

We recommend setting up a dedicated [Conda](https://docs.conda.io/) or [Mamba](https://mamba.readthedocs.io/) environment with the required dependencies.

```bash
# Clone the repository
git clone https://github.com/magnesim/opendrift_simulations.git
cd opendrift_simulations

# Create environment with OpenDrift and analysis tools
conda create -n opendrift -c conda-forge python=3.11 opendrift trajan xarray cartopy netcdf4 matplotlib

# Activate the environment
conda activate opendrift
```

> **Note**: An active internet connection is required during simulations to stream hydrodynamic forcing data from the MET Norway THREDDS server.

---

## Exercises & Usage

### 1. Basic Surface Drift (`rad320_surface.py`)

Simulates passive surface drifters driven by ocean surface currents:

- **Model used**: `OceanDrift`
- **Forcing**: Norkystv3 800m via OPeNDAP (`https://thredds.met.no/...`)
- **Key Concepts**: Release location/timing, horizontal diffusivity, coastline interaction (`previous` vs `stranding`).

Run the script:
```bash
python rad320_surface.py
```

---

### 2. Radionuclide Dispersion Simulation (`rad320_radionuclides.py`)

Simulates a 3D release of radionuclides with speciation and vertical dynamics:

- **Model used**: `RadionuclideDrift`
- **Key Settings**:
  - `seed:LMM_fraction`: Fraction of radionuclide in Low Molecular Mass (dissolved) form.
  - `seed:particle_fraction`: Fraction bound to particles/colloids.
  - `seed:total_release`: Total activity released (in $\text{Bq}$).
  - `drift:vertical_mixing`: Enables vertical mixing and diffusivity model.
- **Output**: Writes trajectories to `radionuclide.nc`. Optionally creates density maps (`concentration_rad320.nc`).

Run the script:
```bash
python rad320_radionuclides.py
```

---

### 3. Trajectory & Concentration Analysis (`rad320_trajan_analysis.py`)

Performs post-processing on the trajectory output netCDF file (`radionuclide.nc`):

- Calculates activity per element based on `total_release` metadata.
- Converts trajectory particles into gridded 3D concentrations ($\text{Bq/m}^3$) across a regular spatial grid using `trajan`.
- Applies spatial rolling smoothing and renders geographic maps with Cartopy.
- Extracts concentration time series at specific monitoring coordinates (e.g., monitoring stations or aquaculture sites).

Run the script:
```bash
python rad320_trajan_analysis.py
```

---

## Hydrodynamic Forcing Data

The simulations connect to MET Norway's Norkystv3 ocean model:
- **Dataset**: `norkystv3_800m_m00_be`
- **URL**: `https://thredds.met.no/thredds/dodsC/fou-hi/norkystv3_800m_m00_be`
- High-resolution alternative (160m) can be configured by updating the THREDDS URL in the scripts.

---

## Contact & Credits

- **Course**: NMBU RAD320 (Radioecology)
- **Contact**: Magne Simonsen (magnes@met.no)
- **Framework**: [OpenDrift Documentation](https://opendrift.github.io)
