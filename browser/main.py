
"""query_rcsb.py: 
    Query rscb

Last modified: Fri Aug 29, 2014  04:54PM

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


logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)

h1 = logging.StreamHandler(sys.stderr)
h1.setLevel(logging.DEBUG)
logger.addHandler(h1)

class Query():

    def __init__(self, args, **kwargs):
        """Create a query with text"""
        self.args = args
        self.queryText = ' '.join(self.args.query)
        logger.info("Querying for: {}".format(self.queryText))
        self.urlbase = 'http://www.rcsb.org/pdb/rest'
        self.url = self.urlbase + '/search'
        self.query = ET.Element("orgPdbQuery")
        self.queryType = "org.pdb.query.simple." + args.query_type
        self.queryType = kwargs.get("queryType", self.queryType)
        self.addQueryType(self.queryType)
        self.ids = []
        if "AdvancedKeywordQuery" in self.queryType:
            self.addKeywords(self.queryText)

    def addKeywords(self, keywords):
        logger.info("Keywords: {}".format(keywords))
        keywordsXML = ET.SubElement(self.query, "keywords")
        keywordsXML.text = keywords

    def addQueryType(self, type):
        """Add type to query if given """
        queryTypeXML = ET.SubElement(self.query, "queryType")
        self.queryType = type
        queryTypeXML.text = self.queryType
        self.addDescription()

    def addDescription(self):
        description = ET.SubElement(self.query, "description")
        description.text = "Query type %s for text: %s" % (
                self.queryType
                , self.queryText
                )

    def getResults(self):
        """Fetch results"""
        logger.info("Fetching results from: {}".format(self.url))
        req = urllib2.Request(self.url, data=ET.tostring(self.query))
        f = urllib2.urlopen(req)
        result = f.read()
        self.ids = filter(None, result.split("\n"))
        logger.info("Total {} results are fetched".format(len(self.ids)))
        
    def getStructureReport(self, **kwargs):
        """Get information about an id"""
        if not self.ids:
            self.getResults()
            if not self.ids:
                print("Nothing found for query: %s" % self)
            print self.ids
        size = kwargs.get('size', None)
        if not size:
            size = min(1000, len(self.ids))

        logger.debug("Getting details of {} entries...".format(size+1))
        query = ",".join(self.ids[:size])

        format = kwargs.get('format', 'xml')
        service = kwargs.get('service', 'wsfile')

        url = self.url + '/customReport.csv?pdbids={}'.format(query)
        url += '&customReportColumns=structureId,structureTitle'
        url += ',experimentalTechnique,depositionDate,releaseDate,ndbId'
        url += ',resolution,structureAuthor,classification'
        url += ',structureMolecularWeight,macromoleculeType'
        url += '&service={service}&format={format}'.format(service = service, format = format)
        logger.debug("Report URL:\n {} \n".format(url))
        req = urllib2.Request(url)
        f = urllib2.urlopen(req)
        self.report = f.read()
        with open(os.path.join(args.download_dir, 'custom_report.{}'.format(format))) as f:
            print("INFO: Storing custom report: {}".format(args.download_dir))
            f.write(self.report)

    def printReport(self):
        """Write report to console"""
        pass




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
        print("implement download pdb file")

if __name__ == "__main__":
    main()

