import json
import luigi
import logging
import os
import subprocess

from luigi.util import requires
from process_slc_pair.Common import getLocalStateTarget
from process_slc_pair.GetConfiguration import GetConfiguration

log = logging.getLogger('luigi-interface')

@requires(GetConfiguration)
class ProcessSLCPair(luigi.Task):
    def checkInputFilesExist(self, file):
        if not os.path.isfile(file):
            raise Exception('{0}: Does not exist'.format(file))
        return True

    def runProcess(self, executable, processXML, firstInput, secondInput, workingDir, runAsShell=True):
        cmd = '{0} {1} -Pinput1={2} -Pinput2={3} -Poutput={4}'.format(
                executable, processXML, firstInput, secondInput, workingDir)
        log.info('Running command: {0}'.format(cmd))
        return subprocess.run(cmd, shell=runAsShell)

    def run(self):
        config = {}
        with self.input().open('r') as getConfiguration:
            config = json.load(getConfiguration)

        workingFolderWithPattern = os.path.join(config['workingFolder'], config['outputFilePattern'])
        proc = self.runProcess(config['executablePath'], config['configXMLPath'],
                                  config['firstInputPath'], config['secondInputPath'],
                                  workingFolderWithPattern)

        if proc.returncode != 0:
            raise Exception("Return code from snap process not 0, code was: {0}".format(
                proc.returncode))

        with self.output().open('w') as output:
            output.write(json.dumps({
                'executablePath': config['executablePath'],
                'configXMLPath': config['configXMLPath'],
                'inputFolder': config['inputFolder'],
                'firstInputPath': config['firstInputPath'],
                'secondInputPath': config['secondInputPath'],
                'outputFolder': config['outputFolder'],
                'outputFilePattern': config['outputFilePattern'],
                'workingFolder': config['workingFolder'],
                'workingFolderWithPattern': workingFolderWithPattern
            }, indent=4))

    def output(self):
      return getLocalStateTarget(self.paths['state'], 'ProcessSLCPair.json')
