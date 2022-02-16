import glob
import json
from importlib_metadata import requires
import luigi
import logging
import os
import subprocess

from process_pair.get_configuration import GetConfiguration

log = logging.getLogger('luigi-interface')


@requires(GetConfiguration)
class ProcessSLCPair(luigi.Task):
    paths = luigi.DictParameter()

    def checkInputFilesExist(self, file):
        if not os.path.isfile(file):
            raise Exception('{0}: Does not exist'.format(file))
        return True

    def runProcess(self, executable, processXML, firstInput, secondInput, outputDir, runAsShell=True):
        return subprocess.run(
            "{0} {1} -Pinput1={2} -Pinput2={3} -Poutput={4}".format(
                executable, processXML, firstInput, secondInput, outputDir)
        )

    def getOutputFolderNameFromInputs(self, first, second):
        file = os.path.basename(first)

        satellite = file[0:3]
        startDate = file[17:25]

        file = os.path.basename(second)
        endDate = file[17:25]

        return '{0}_coh_vv_{1}_{2}'.format(satellite, startDate, endDate)

    def getOutputFolder(self, outputBase, firstInput, secondInput):
        outputFolder = os.path.join(
            outputBase, self.getOutputFolderNameFromInput(firstInput, secondInput))

        log.info('Output folder is set to {0}'.format(outputFolder))

        return outputFolder

    def run(self):
        config = {}
        with self.input().open('r') as getConfiguration:
            config = json.load(getConfiguration)

        retcode = self.runProcess(config['executablePath'], config['processXMLPath'],
                                  config['firstInputPath'], config['secondInputPath'],
                                  self.getOutputFolder(config['outputBaseDir'], config['firstInputPath'], config['secondInputPath']))

        if retcode != 0:
            raise "Return code from snap process not 0, code was: {0}".format(
                retcode)
