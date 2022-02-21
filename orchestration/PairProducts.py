import luigi
import os
import logging
import json
import re

from luigi.util import requires
from orchestration.GetInputs import GetInputs

log = logging.getLogger('luigi-interface')

@requires(GetInputs)
class PairProducts(luigi.Task):
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

            pattern = 'S1.*_([0-9]{8}T[0-9]{6})_[0-9]{8}T[0-9]{6}_.*\.zip'

            firstDate = re.match(pattern, firstProduct).group(1)
            secondDate = re.match(pattern, secondProduct).group(1)

            name = f'{firstDate}_{secondDate}'

            productPairs.append({
                'pairName': name,
                'products': [firstProduct, secondProduct]
            })

        with self.output().open('w') as outFile:
            outFile.write(json.dumps(productPairs, indent=4, sort_keys=True))

    def output(self):
        return luigi.LocalTarget(os.path.join(self.stateLocation, 'PairProducts.json'))