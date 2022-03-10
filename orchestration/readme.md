# 'cuu-illegal-waste'

This code was developed by JNCC under the Copernicus User Uptake Work Package 6 project focussing on monitoring illegal waste using Sentinel-1 imagery. This project is joint-funded by Scottish Government through the JNCC Simple Analysis Ready Data Service Project. 

## Setup venv

```
cd orchestration
python -m venv .venv
source .venv/bin/activate
```

## Running Luigi script

Create a `illegal-waste-orchestration-luigi.cfg` file using the template and run it like so:

```
LUIGI_CONFIG_PATH=orchestration/illegal-waste-orchestration-luigi.cfg PYTHONPATH='.' luigi --module orchestration SubmitJobs --testProcessing --local-scheduler
```

Use the `--testProcessing` flag to test locally or it will try and actually submit the jobs.

The inputs can be dummy files, e.g. the following:

```
S1B_IW_SLC__1SDV_20201216T175827_20201216T175854_024731_02F107_7A4B.zip
S1B_IW_SLC__1SDV_20201204T175828_20201204T175855_024556_02EB54_47B6.zip
S1B_IW_SLC__1SDV_20201122T175828_20201122T175855_024381_02E5CA_0DC7.zip
S1B_IW_SLC__1SDV_20201110T175829_20201110T175856_024206_02E040_D8A8.zip
S1B_IW_SLC__1SDV_20201228T175827_20201228T175854_024906_02F6B2_FD92.zip
```