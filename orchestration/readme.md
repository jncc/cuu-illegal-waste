# 'cuu-illegal-waste'

This code was developed by JNCC under the Copernicus User Uptake Work Package 6 project focussing on monitoring illegal waste using Sentinel-1 imagery. This project is joint-funded by Scottish Government through the JNCC Simple Analysis Ready Data Service Project. 

## Setup venv

```
cd orchestration
python -m venv .venv
source .venv/bin/activate
```

## Running Luigi script

```sh
luigi --module orchestration GetInputs
  --inputDir=/path/to/input/dir
```
