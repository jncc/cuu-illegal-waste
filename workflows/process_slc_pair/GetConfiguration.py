import logging
import luigi
import json
import os

from process_slc_pair.Common import getLocalStateTarget, getOutputFolderFromInputs

log = logging.getLogger('luigi-interface')

class GetConfiguration(luigi.Task):
  paths = luigi.DictParameter()
  firstInput = luigi.Parameter()
  secondInput = luigi.Parameter()
  outputBaseFolder = luigi.Parameter()
  
  def run(self):
    with self.output().open('w') as outFile:
      outFile.write(json.dumps({
        'executablePath': self.paths['executable'],
        'configXMLPath': os.path.join(self.paths['toolchain'], self.paths['toolchainXML']),
        'firstInputPath': self.firstInput,
        'secondInputPath': self.secondInput,
        'outputBaseFolder': self.outputBaseFolder,
        'outputFolder': getOutputFolderFromInputs(self.firstInput, self.secondInput)
      }))
  
  def output(self):
    return getLocalStateTarget(self.paths['state'], 'GetConfiguration.json')