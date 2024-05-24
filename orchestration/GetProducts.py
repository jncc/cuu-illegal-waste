from glob import glob
import luigi
import os
import logging
import glob
import json
import shutil

log = logging.getLogger('luigi-interface')

class GetProducts(luigi.Task):
    inputLocation = luigi.Parameter()
    stateLocation = luigi.Parameter()

    def run(self):
        log.info(self.inputLocation)

        folderPaths = []
        for file in glob.glob(os.path.join(self.inputLocation, 'S1*_SLC_*.SAFE')):
            folderPaths.append(file)

        filePaths = []
        for folderPath in folderPaths:
            zipPath = folderPath.replace("SAFE", "zip")
            shutil.make_archive(zipPath, 'zip', folderPath)
            shutil.rmtree(folderPath)

            filePaths.append(zipPath)

        output = {
            'files': filePaths
        }
        with self.output().open("w") as outFile:
            outFile.write(json.dumps(output, indent=4, sort_keys=True))

    def output(self):
        basketDirName = os.path.basename(os.path.normpath(self.inputLocation))
        return luigi.LocalTarget(os.path.join(self.stateLocation, f'GetProducts_{basketDirName}.json'))
