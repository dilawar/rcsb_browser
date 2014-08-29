
"""query_rcsb.py: 
    Query rscb

Last modified: Fri Aug 29, 2014  11:57PM

"""
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2013, Dilawar Singh and NCBS Bangalore"
__credits__          = ["NCBS Bangalore"]
__license__          = "GNU GPL"
__version__          = "1.0.0"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"
__status__           = "Development"

import urllib2
import logging
import sys
import os
import xml.etree.ElementTree as ET
from query import Query

logger = logging.getLogger('rscb')

def fetchIF(id, download_dir):
    logger.info("Fetching id: {}".format(id))

def main():
    import argparse
    # Argument parser.
    description = 'A script to download PDB files from RCSB Protein Data Bank'
    parser = argparse.ArgumentParser(description=description)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--query', '-q', metavar='query'
            , nargs = '+'
            , help = 'Query text'
            )

    parser.add_argument('--query_type', '-qt', metavar='queryType'
            , default = 'AdvancedKeywordQuery'
            , help = "Type of this query, prefixed by org.pdb.query.simple"
            )

    parser.add_argument('--download_dir', '-dd', metavar = "downloadDir"
            , default = os.getcwd()
            , help = "Directory. All PDB files are downloaded into this dir"
            )

    group.add_argument('--fetch', '-f', metavar = 'fetchID'
            , nargs = '+'
            , help = 'Download this ID'
            )

    class Args: pass 
    args = Args()
    parser.parse_args(namespace=args)

    # get the arguments.
    if args.query:
        q = Query(args)
        q.getStructureReport()
        q.printReport()
    elif args.fetch:
        fetchID(args.fetch, args.download_dir)

if __name__ == "__main__":
    main()

