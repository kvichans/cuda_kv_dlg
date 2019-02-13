''' Lib for Plugin
Authors:
    Andrey Kvichansky    (kvichans on github.com)
Version:
    '0.8.01 2019-02-13'
Content
ToDo: (see end of file)
'''

import  sys, os, gettext, logging, inspect, collections, json, re, subprocess
from    time        import perf_counter

import  cudatext        as app
from    cudatext    import ed
import  cudax_lib       as apx
from    cd_kv_base  import *

VERSION     = re.split('Version:', __doc__)[1].split("'")[1]
VERSION_V,  \
VERSION_D   = VERSION.split(' ')


if __name__ == '__main__' :
    # To start the tests run in Console
    #   exec(open(path_to_the_file, encoding="UTF-8").read())

    app.app_log(app.LOG_CONSOLE_CLEAR, 'm')
    print('Start all tests')
    if -1==-1:
        print('Start tests: log')
        log('n={}',1.23)
        log('n,s¬=¶{}',(1.23, 'abc'))
        def my():
            log('a={}',1.23)
            def sub():
                log('###')
            class CMy:
                def meth(self):
                    log('###')
            sub()
            CMy().meth()
        my()
        print('Stop tests: log')

    if -2==-2:
        print('Start tests: plugin history')

        for smk in [smk for smk 
            in  sys.modules                             if 'cuda_kv_base.tests.test_hist' in smk]:
            del sys.modules[smk]        # Avoid old module 
        import                                              cuda_kv_base.tests.test_hist
        import unittest
        suite = unittest.TestLoader().loadTestsFromModule(  cuda_kv_base.tests.test_hist)
        unittest.TextTestRunner().run(suite)
        
        print('Stop tests: plugin history')
    print('Stop all tests')
'''
ToDo
[+][kv-kv][11feb19] Extract from cd_plug_lib.py
[+][kv-kv][11feb19] Set tests
'''
