import json
import luigi
import logging
import os
import shutil

from luigi.util import requires
from process_slc_pair.Common import getLocalStateTarget
from process_slc_pair.ConvertToTif import ConvertToTif

log = logging.getLogger('luigi-interface')

@requires(ConvertToTif)
class TransferOutputs(luigi.Task):

    def run(self):
        convertToTif = {}
        with self.input().open('r') as convertToTifOutput:
            convertToTif = json.load(convertToTifOutput)

        outputFolderPath = convertToTif['outputFolder']
        outputFilePath = convertToTif['outputFilePath']
        outputFilename = convertToTif['outputFilename']
        
        finalOutputFilePath = os.path.join(outputFolderPath, outputFilename)
        shutil.copyfile(outputFilePath, finalOutputFilePath)

        with self.output().open('w') as output:
            output.write(json.dumps({
                'inputFolder': convertToTif['inputFolder'],
                'outputFolder': convertToTif['outputFolder'],
                'workingFolder': convertToTif['workingFolder'],
                'outputFilePath': outputFilePath,
                'outputFilename': outputFilename,
                'outputFilePattern': convertToTif['outputFilePattern']
            }, indent=4))

    def output(self):
      return getLocalStateTarget(self.paths['state'], 'TransferOutputs.json')