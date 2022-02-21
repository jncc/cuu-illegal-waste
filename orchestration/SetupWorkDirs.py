import luigi
import os
import logging
import json

from luigi.util import requires
from orchestration.PairProducts import PairProducts

log = logging.getLogger('luigi-interface')

@requires(PairProducts)
class SetupWorkDirs(luigi.Task):
    stateLocation = luigi.Parameter()
    workingLocation = luigi.Parameter()

    def run(self):
        productPairs = []
        with self.input().open('r') as inputFile:
            productPairs = json.load(inputFile)

        workDirs = []
        for pair in productPairs:
            workDir = os.path.join(self.workingLocation, pair['pairName'])
            os.mkdir(workDir)

            # create sbatch file and subdirs

            workDirs.append(workDir)

        output = {
            'workDirs': workDirs
        }
        with self.output().open('w') as outFile:
            outFile.write(json.dumps(output, indent=4, sort_keys=True))

    def output(self):
        return luigi.LocalTarget(os.path.join(self.stateLocation, 'SetupWorkDirs.json'))