import luigi
import os
import logging
import json
import glob

from luigi.util import requires
from orchestration.SetupSubBaskets import SetupSubBaskets
from orchestration.GetProducts import GetProducts

log = logging.getLogger('luigi-interface')

@requires(SetupSubBaskets)
class GetAllSubBaskets(luigi.Task):
    inputLocation = luigi.Parameter()
    basketLocation = luigi.Parameter()
    stateLocation = luigi.Parameter()
    workingLocation = luigi.Parameter()

    def run(self):
        log.info(self.basketLocation)

        subBaskets = []
        for dir in glob.glob(os.path.join(self.basketLocation, 'S1*_*_*/')):
            task = GetProducts(
                inputLocation = dir,
                stateLocation = self.stateLocation
            )

            yield task

            with task.output().open('r') as taskOutput:
                products = json.load(taskOutput)['products']

                count = len(products)
                if count < 2:
                    raise Exception(f'Need at least two products in the basket, found {count}')

                subBaskets.append({
                    'basketPath': dir,
                    'products': products
                })

        output = {
            'subBaskets': subBaskets
        }
        with self.output().open("w") as outFile:
            outFile.write(json.dumps(output, indent=4, sort_keys=True))

    def output(self):
        return luigi.LocalTarget(os.path.join(self.stateLocation, 'GetAllSubBaskets.json'))
