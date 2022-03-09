from glob import glob
import luigi
import os
import logging
import glob
import json

log = logging.getLogger('luigi-interface')

class GetProducts(luigi.Task):
    inputLocation = luigi.Parameter()
    stateLocation = luigi.Parameter()

    def run(self):
        log.info(self.inputLocation)

        filePaths = []
        for file in glob.glob(os.path.join(self.inputLocation, 'S1*_SLC_*.zip')):
            filePaths.append(file)

        output = {
            'files': filePaths
        }
        with self.output().open("w") as outFile:
            outFile.write(json.dumps(output, indent=4, sort_keys=True))

    def output(self):
        basketDirName = os.path.basename(os.path.normpath(self.inputLocation))
        return luigi.LocalTarget(os.path.join(self.stateLocation, f'GetProducts_{basketDirName}.json'))
