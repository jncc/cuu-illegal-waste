import luigi
import os
import logging
import json

from luigi.util import requires
from orchestration.GetProducts import GetProducts

log = logging.getLogger('luigi-interface')

@requires(GetProducts)
class GetProductPairs(luigi.Task):
    stateLocation = luigi.Parameter()

    def run(self):
        files = []
        with self.input().open('r') as inputFile:
            files = json.load(inputFile)

        products = []
        for file in files['files']:
            filename = os.path.basename(file)
            products.append(filename)

        products = sorted(products)

        productPairs = []
        for i in range(len(products)-1):
            firstProduct = products[i]
            secondProduct = products[i+1]

            firstDate = firstProduct[17:32]
            secondDate = secondProduct[17:32]

            name = f'S1_{firstDate}_{secondDate}'

            productPairs.append({
                'pairName': name,
                'products': [firstProduct, secondProduct]
            })

        with self.output().open('w') as outFile:
            outFile.write(json.dumps(productPairs, indent=4, sort_keys=True))

    def output(self):
        return luigi.LocalTarget(os.path.join(self.stateLocation, 'GetProductPairs.json'))