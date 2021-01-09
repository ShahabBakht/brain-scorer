import sys
sys.path.append('../')

from loaders import pvc4
import numpy as np
import tempfile
import time
import unittest
import torch
from pprint import pprint

class TestPvc4Loader(unittest.TestCase):
    def test_openimfile(self):
        framecount, iconsize, iconside, filetype = pvc4._openimfile(
            '../data_derived/crcns-pvc4/Nat/r0208D/test.review.mountlake.30_pix.2sizes.imsm')
        self.assertEqual(framecount, 756)
        self.assertEqual(iconsize, 14400)
        self.assertEqual(iconside, 120)
        self.assertEqual(filetype, 2)

    def test_loadimfile(self):
        data = pvc4._loadimfile(
            '../data_derived/crcns-pvc4/Nat/r0208D/test.review.mountlake.30_pix.2sizes.imsm')
        self.assertEqual(data.shape[2], 120)
        self.assertEqual(data.shape[0], 756)

    def test_loadimfile_iconsize0(self):
        data = pvc4._loadimfile(
            '../data_derived/crcns-pvc4/NatRev/r0156A/test.natrev.size.mountlake.imsm')
        self.assertEqual(data.shape[2], 96)
        self.assertEqual(data.shape[0], 7228)

    def test_train(self):
        loader = pvc4.PVC4('../data_derived/crcns-pvc4', 
                           nt=32, 
                           nx=64,
                           ny=64,
                           split='train',
                           )
        
        self.assertEqual(len({x['cellnum']: 1 for x in loader.sequence}), 
                         loader.total_electrodes)
        
        self.assertEqual(len({x['cellid']: 1 for x in loader.sequence}), 
                         loader.total_electrodes)

        X, m, W, y = loader[0]
        self.assertEqual(X.shape[3], 64)
        self.assertEqual(X.shape[1], loader.nt + loader.ntau - 1)
        self.assertEqual(m.shape, W.shape)
        self.assertEqual(y.ndim, 2)
        self.assertEqual(y.shape[1], 32)

    def test_traintune(self):
        loader = pvc4.PVC4('../data_derived/crcns-pvc4', 
                           nt=32, 
                           nx=64,
                           ny=64,
                           split='traintune',
                           )

        loader[0]

    def test_tune(self):
        _ = pvc4.PVC4('../data_derived/crcns-pvc4', nt=32, split='tune')

    def test_report(self):
        _ = pvc4.PVC4('../data_derived/crcns-pvc4', nt=32, split='report')

    def test_v2(self):
        for i in range(123):
            print(i)
            loader = pvc4.PVC4('../data_derived/crcns-v2', 
                            nt=32, 
                            nx=64,
                            ny=64,
                            split='train',
                            single_cell=i
                            )
            X, _, _, Y = loader[0]
            self.assertEqual(np.isnan(X).sum(), 0)
            self.assertEqual(np.isnan(Y).sum(), 0)


if __name__ == '__main__':
    unittest.main()