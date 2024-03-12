import os
import unittest

import config


class MyTestCase(unittest.TestCase):
    def test_something(self):
        a = os.listdir(config.PROJECT_ROOT)
        print(a)
        cfg = config.CONFIG
        print(cfg)


if __name__ == '__main__':
    unittest.main()
