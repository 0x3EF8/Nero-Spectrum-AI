import os
import logging

def setup_environment():
    """Sets up the env vars and shuts up some of the noisy logs"""
    # gets rid of that annoying pygame welcome message
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    # keeps grpc from spamming the console
    os.environ['GRPC_VERBOSITY'] = 'ERROR'
    
    # kill loggers for all these libraries so the console stays clean
    for lg in ['httpx', 'httpcore', 'comtypes', 'urllib3', 'google', 'grpc']:
        logging.getLogger(lg).setLevel(logging.CRITICAL)
