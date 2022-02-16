import logging
import luigi
import json
import os

from common import getLocalStateTarget, getOutputFolderFromInputs

log = logging.getLogger('luigi-interface')

class GetConfiguration(luigi.Task):
  paths = luigi.DictParameter()
  firstInput = luigi.Parameter()
  secondInput = luigi.Parameter()
  
  def run(self):
    with self.output().open('w') as outFile:
      outFile.write(json.dumps({
        'executablePath': self.paths['executable'],
        'configXMLPath': os.path.join(self.paths['toolchain'], self.paths['toolchainXML']),
        'firstInputPath': self.firstInput,
        'secondInputPath': self.secondInput,
        'outputBaseFolder': self.paths['output'],
        'outputFolder': getOutputFolderFromInputs(self.firstInput, self.secondInput),
        'sourceSRS': self.sourceSRS,
        'outputSRS': self.outputSRS
      }))
  
  def output(self):
    return getLocalStateTarget(self.paths['state'], 'GetConfiguration.json')