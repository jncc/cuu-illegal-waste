import json
import logging
import luigi
import os
import shutil

from luigi.util import requires
from process_slc_pair.Common import getLocalStateTarget
from process_slc_pair.ConvertToTif import ConvertToTif

log = logging.getLogger('luigi-interface')

@requires(ConvertToTif)
class CleanupCompletedProductInputs(luigi.Task):
  paths = luigi.DictParameter()

  def run(self):
    convertToTifOutput = {}
    with self.input().open('r') as processOutput:
        convertToTifOutput = json.load(processOutput)

    inputBasketDirectory = os.path.join(self.paths['input'], convertToTifOutput['inputFolder'])
    log.info('Removing input basket directory "{0}"'.format(inputBasketDirectory))
    shutil.rmtree(inputBasketDirectory)

    with self.output().open('w') as output:
      output.write(json.dumps(convertToTifOutput))
  
  def output(self):
    return getLocalStateTarget(self.paths['state'], 'CleanupCompletedProductInputs.json')  