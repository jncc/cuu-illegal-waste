import json
import logging
import luigi
import os
import subprocess

from luigi.util import requires
from process_slc_pair.Common import getLocalStateTarget
from process_slc_pair.ProcessSLCPair import ProcessSLCPair

log = logging.getLogger('luigi-interface')

@requires(ProcessSLCPair)
class ConvertToTif(luigi.Task):
  sourceSRS = luigi.Parameter()
  outputSRS = luigi.Parameter()

  def convert(self, input, outputFilePath, sourceSRS, outputSRS, runAsShell=True):
    log.info('Creating output GeoTIFF at {0}'.format(outputFilePath))

    cmd = 'gdalwarp -s_srs EPSG:{0} -t_srs EPSG:{1} -dstnodata 0 -r near -of GTiff -tr 10.0 10.0 -co "COMPRESS=DEFLATE" {2} {3}'.format(sourceSRS, outputSRS, input, outputFilePath)
    log.info('Running {0}'.format(cmd))

    return subprocess.run(cmd, shell=runAsShell)

  def getInputFile(self, workingFolderWithPattern):
    dataFolder = '{0}.data'.format(workingFolderWithPattern)

    if not (os.path.isdir(dataFolder)):
      raise Exception('Expected output folder {0} does not exist'.format(dataFolder))
    
    log.info('Using data folder {0}'.format(dataFolder))
    
    inputFiles = [file for file in os.listdir(dataFolder) if file.endswith('.img')]
    inputFile = ''

    if len(inputFiles) == 1:
      inputFile = inputFiles[0]
    else:
      if len(inputFiles) == 0:
        raise Exception('Could not find a valid .img file in {0}'.format(dataFolder))
      raise Exception('Found more than one candidate data file in {0}, found {1}'.format(dataFolder, inputFiles))

    log.info('Using input file {0}'.format(inputFile))

    return os.path.join(dataFolder, inputFile)

  def run(self):
    processSLCPairOutput = {}
    with self.input().open('r') as processOutput:
        processSLCPairOutput = json.load(processOutput)

    outputFilename = '{0}.tif'.format(processSLCPairOutput['outputFilePattern'])
    outputFilePath = os.path.join(processSLCPairOutput['workingFolder'], outputFilename)
    proc = self.convert(self.getInputFile(processSLCPairOutput['workingFolderWithPattern']), outputFilePath, self.sourceSRS, self.outputSRS)

    if proc.returncode != 0:
        raise Exception("Return code from gdalwarp process not 0, code was: {0}".format(
            proc.returncode))

    with self.output().open('w') as output:
      output.write(json.dumps({
        'inputFolder': processSLCPairOutput['inputFolder'],
        'outputFolder': processSLCPairOutput['outputFolder'],
        'workingFolder': processSLCPairOutput['workingFolder'],
        'outputFilePath': outputFilePath,
        'outputFilename': outputFilename,
        'outputFilePattern': processSLCPairOutput['outputFilePattern']
      }, indent=4))
  
  def output(self):
    return getLocalStateTarget(self.paths['state'], 'ConvertToTif.json')
