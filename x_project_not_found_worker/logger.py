import linecache
import sys
import traceback
import logging
import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger('x_project_not_found_worker')
f = logging.Formatter('[L:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', datefmt='%d-%m-%Y %H:%M:%S')
logger.setLevel(logging.DEBUG)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(f)
logger.addHandler(consoleHandler)


def exception_message(*args, **kwargs):
    params = json.dumps({'args': args, 'kwargs': kwargs})
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    trace = ''.join(traceback.format_tb(tb))
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return 'EXCEPTION IN ({}, LINE {} "{}"): {} {} PARAMS: {}'.format(filename, lineno, line.strip(), exc_obj, trace, params)
