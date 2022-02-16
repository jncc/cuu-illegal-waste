import glob
import json
import luigi
import logging
import os
import subprocess

from common import getLocalStateTarget, getOutputFolderPath
from importlib_metadata import requires
from process_pair.get_configuration import GetConfiguration

log = logging.getLogger('luigi-interface')

@requires(GetConfiguration)
class ProcessSLCPair(luigi.Task):
    def checkInputFilesExist(self, file):
        if not os.path.isfile(file):
            raise Exception('{0}: Does not exist'.format(file))
        return True

    def runProcess(self, executable, processXML, firstInput, secondInput, outputDir, runAsShell=True):
        cmd = '{0} {1} -Pinput1={2} -Pinput2={3} -Poutput={4}'.format(
                executable, processXML, firstInput, secondInput, outputDir)
        log.info('Running command: {0}'.format(cmd))
        return subprocess.run(cmd)

    def run(self):
        config = {}
        with self.input().open('r') as getConfiguration:
            config = json.load(getConfiguration)

        outputFolderPath = getOutputFolderPath(config['outputBaseFolder'], config['outputFolder'])
        log.info('Writing outputs to {0}'.format(outputFolderPath))

        retcode = self.runProcess(config['executablePath'], config['processXMLPath'],
                                  config['firstInputPath'], config['secondInputPath'],
                                  outputFolderPath)

        if retcode != 0:
            raise "Return code from snap process not 0, code was: {0}".format(
                retcode)

        with self.output().open('w') as output:
          output.write(json.dumps({
            'executablePath': config['executablePath'],
            'configXMLPath': config['configXMLPath'],
            'firstInputPath': config['firstInputPath'],
            'secondInputPath': config['secondInputPath'],
            'outputBaseFolder': config['outputBaseFolder'],
            'outputFolder': config['outputFolder']
          }))

    def output(self):
      return getLocalStateTarget(self.paths['state'], 'ConvertToTif.json')
