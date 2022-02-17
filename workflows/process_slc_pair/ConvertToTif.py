import json
import logging
import luigi
import os
import subprocess

from importlib_metadata import requires
from process_slc_pair.Common import getLocalStateTarget
from process_slc_pair.ProcessSLCPair import ProcessSLCPair

log = logging.getLogger('luigi-interface')

@requires(ProcessSLCPair)
class ConvertToTif(luigi.Task):
  sourceSRS = luigi.Parameter()
  outputSRS = luigi.Parameter()

  def convert(self, input, outputFolder, sourceSRS, outputSRS):
    outputFilename = os.path.basename(input).replace('.img', '.tif')
    outputFullPath = os.path.join(outputFolder, outputFilename)

    log.info('Creating output GeoTIFF at {0}'.format(outputFullPath))

    return subprocess.run('gdalwarp -s_srs {0} -t_srs {1} -dstnodata 0 -r near -of GTiff -tr 10.0 10.0 -co "COMPRESS=DEFLATE" {2} {3}'.format(sourceSRS, outputSRS, input, outputFullPath))

  def getInputFile(self, processOutputFolder):
    dataFolder = [dataFolder for dataFolder in os.listdir(processOutputFolder) if dataFolder.endswith('.data')]

    if (len(dataFolder) == 1):
      dataFolder = dataFolder[0]
    else:
      raise Exception('Found more than one data folder candidate in output folder "{0}", found {1}'.format(processOutputFolder, dataFolder))

    inputFile = os.path.join(dataFolder, '{0}.img'.format(os.basename(dataFolder)))

    if os.path.isfile(inputFile):
      return inputFile
    else:
      raise Exception('Output raster file does not exist: {0}'.format(inputFile))

  def run(self):
    processSLCPairOutput = {}
    with self.input().open('r') as processOutput:
        processSLCPairOutput = json.load(processOutput)

    retcode = self.convert(self.getInputFile(processSLCPairOutput['outputFolderPath']), processSLCPairOutput['outputFolder'], self.sourceSRS, self.outputSRS)

    if retcode != 0:
        raise "Return code from snap process not 0, code was: {0}".format(
            retcode)

    with self.output().open('w') as output:
      output.write(json.dumps({

      }))    
  
  def output(self):
    return getLocalStateTarget(self.paths['state'], 'ConvertToTif.json')
