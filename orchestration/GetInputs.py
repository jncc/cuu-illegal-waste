from glob import glob
from math import prod
import luigi
import os
import logging
import glob
import json

log = logging.getLogger('luigi-interface')

class GetInputs(luigi.Task):
    inputLocation = luigi.Parameter()
    stateLocation = luigi.Parameter()

    def run(self):
        log.info(self.inputLocation)

        filePaths = []
        for file in glob.glob(os.path.join(self.inputLocation, 'S1*_SLC_*.zip')):
            filePaths.append(file)

        count = len(filePaths)
        if count < 2:
            raise Exception(f'Need at least two products in the basket, found {count}')

        output = {
            'files': filePaths
        }
        with self.output().open("w") as outFile:
            outFile.write(json.dumps(output, indent=4, sort_keys=True))

    def output(self):
        return luigi.LocalTarget(os.path.join(self.stateLocation, 'GetInputs.json'))
