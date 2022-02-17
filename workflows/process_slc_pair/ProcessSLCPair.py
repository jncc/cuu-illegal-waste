import glob
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

    def runProcess(self, executable, processXML, firstInput, secondInput, outputDir, runAsShell=True):
        cmd = '{0} {1} -Pinput1={2} -Pinput2={3} -Poutput={4}'.format(
                executable, processXML, firstInput, secondInput, outputDir)
        log.info('Running command: {0}'.format(cmd))
        return subprocess.run(cmd)

    def run(self):
        config = {}
        with self.input().open('r') as getConfiguration:
            config = json.load(getConfiguration)

        outputFolderPath = os.path.join(config['outputBaseFolder'], config['outputFolder'])
        outputFolderPathWithPattern = os.path.join(outputFolderPath, config['outputFilePattern'])
        log.info('Writing outputs as pattern {0}'.format(outputFolderPathWithPattern))

        retcode = self.runProcess(config['executablePath'], config['configXMLPath'],
                                  config['firstInputPath'], config['secondInputPath'],
                                  outputFolderPathWithPattern)

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
            'outputFilePattern': config['outputFilePattern'],
            'outputFolderPath': outputFolderPath,
            'outputFolderPathWithPattern': outputFolderPathWithPattern
          }))

    def output(self):
      return getLocalStateTarget(self.paths['state'], 'ProcessSLCPair.json')
