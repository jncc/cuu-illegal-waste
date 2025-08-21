import json
import logging
import luigi
import os
import shutil

from pathlib import Path
from luigi.util import requires
from process_slc_pair.Common import getLocalStateTarget
from process_slc_pair.TransferOutputs import TransferOutputs

log = logging.getLogger('luigi-interface')

@requires(TransferOutputs)
class CleanupCompletedProducts(luigi.Task):
    paths = luigi.DictParameter()

    def run(self):
        transferOutputs = {}
        with self.input().open('r') as transferOutput:
            transferOutputs = json.load(transferOutput)

        workingFolder = transferOutputs["workingFolder"]
        log.info(f'Cleanup working files in {workingFolder}')
        for path in Path(workingFolder).glob('**/*'):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)

        basketSubDirectory = os.path.join(self.paths['input'], transferOutputs['inputFolder'])
        log.info(f'Removing input basket directory {basketSubDirectory}')
        if Path(basketSubDirectory).exists():
            shutil.rmtree(basketSubDirectory)

        with self.output().open('w') as output:
            output.write(json.dumps(transferOutputs, indent=4))
    
    def output(self):
        return getLocalStateTarget(self.paths['state'], 'CleanupCompletedProducts.json')  