import logging
import luigi
import json
import os

from process_slc_pair.Common import getLocalStateTarget, getOutputPatternFromInputs

log = logging.getLogger('luigi-interface')

class GetConfiguration(luigi.Task):
  paths = luigi.DictParameter()
  inputFolder = luigi.Parameter()
  
  def run(self):
    [firstInput, secondInput] = self.getInputFilePairs(self.inputFolder)
    log.info('Processing S1 file pair [{0}, {1}]'.format(firstInput, secondInput))

    with self.output().open('w') as outFile:
      outFile.write(json.dumps({
        'executablePath': self.paths['executable'],
        'configXMLPath': os.path.join(self.paths['toolchain'], self.paths['toolchainXML']),
        'inputFolder': self.inputFolder,
        'firstInputPath': firstInput,
        'secondInputPath': secondInput,
        'outputBaseFolder': self.paths['output'],
        'outputFolder': getOutputPatternFromInputs(firstInput, secondInput),
        'outputFilePattern': getOutputPatternFromInputs(firstInput, secondInput)
      }))
  
  def getInputFilePairs(self, inputFolder):
    inputFolderPath = os.path.join(self.paths['input'], inputFolder)
    firstDate = inputFolder[4:19]
    secondDate = inputFolder[20:]

    print(inputFolderPath)

    firstInput = [input for input in os.listdir(inputFolderPath) if firstDate in input]
    secondInput = [input for input in os.listdir(inputFolderPath) if secondDate in input]

    if not (len(firstInput) == 1):
      raise Exception('Found more than one candidate for the first input file "%s"').format(firstInput)
    elif not (len(secondInput) == 1):
      raise Exception('Found more than one candidate for the second input file "%s"').format(secondInput)
    return [os.path.join(inputFolderPath, firstInput[0]), os.path.join(inputFolderPath, secondInput[0])]

  def output(self):
    return getLocalStateTarget(self.paths['state'], 'GetConfiguration.json')