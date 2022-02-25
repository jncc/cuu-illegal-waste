import luigi
import os
import logging
import json
import shutil

from luigi.util import requires
from orchestration.GetProducts import GetProducts
from orchestration.GetProductPairs import GetProductPairs

log = logging.getLogger('luigi-interface')

@requires(GetProductPairs, GetProducts)
class SetupSubBaskets(luigi.Task):
    basketLocation = luigi.Parameter()
    stateLocation = luigi.Parameter()

    def run(self):
        productPairs = []
        with self.input()[0].open('r') as productPairsInfo:
            productPairs = json.load(productPairsInfo)

        products = []
        with self.input()[1].open('r') as productsInfo:
            products = json.load(productsInfo)

        movedPairs = []
        for pair in productPairs:
            subBasketDir = os.path.join(self.basketLocation, pair['pairName'])
            log.info(f'Setting up sub basket {subBasketDir}')

            movedPair = {
                'pairName': pair['pairName'],
                'products': [],
                'subBasketDir': subBasketDir
            }

            os.makedirs(subBasketDir)
            for product in pair['products']:
                srcPath = os.path.join(self.basketLocation, product)
                destPath = os.path.join(subBasketDir, product)
                shutil.copy(srcPath, destPath, follow_symlinks=False)

                movedPair['products'].append(destPath)

            movedPairs.append(movedPair)

        # cleanup products outside of sub baskets
        for file in products['files']:
            os.remove(file)

        with self.output().open('w') as outFile:
            outFile.write(json.dumps(movedPairs, indent=4, sort_keys=True))

    def output(self):
        return luigi.LocalTarget(os.path.join(self.stateLocation, 'SetupSubBaskets.json'))