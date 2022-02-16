import luigi
import json
import os

from luigi import LocalTarget

class GetConfiguration(luigi.Task):
  paths = luigi.DictParameter()
  firstInput = luigi.Parameter()
  secondInput = luigi.Parameter()
  
  def run(self):
    with self.output().open('w') as outFile:
      outFile.write(json.dumps({
        'executablePath': self.paths['executablePath'],
        'configXMLPath': self.paths['configXMLPath'],
        'firstInputPath': self.firstInput,
        'secondInputPath': self.secondInput,
        'outputBaseFolder': self.paths['outputFolder']
      }))
  
  def output(self):
    outFile = os.path.join(self.paths['state'], 'GetConfiguration.json')
    return LocalTarget(outFile)