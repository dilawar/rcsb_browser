
"""downloader.py: 

Last modified: Sat Jan 18, 2014  05:01PM

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2013, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import logging 
import urllib
import os

logger = logging.getLogger('rscb')

class Downloader():

    def __init__(self, ids, download_dir, **kwargs):
        """Initialize downloader """
        self.ids = ids
        self.download_dir = download_dir
        self.args = kwargs
        self.url = 'http://www.rcsb.org/pdb/files/'

    def downloadFiles(self, ids = None, type = 'pdb'):
        if ids: self.ids = ids
        for id in self.ids:
            logger.info("Downloading: {}".format(id))
            postfix = '{}.{}.gz'.format(id.upper(), type)
            url = self.url + postfix
            # This part is from 
            # http://stackoverflow.com/questions/22676/how-do-i-download-a-file-over-http-using-python
            file_name = url.split('/')[-1]
            saveFilePath = os.path.join(self.download_dir, file_name)
            logger.info("Downloading {}".format(url))
            urllib.urlretrieve(url, saveFilePath)



