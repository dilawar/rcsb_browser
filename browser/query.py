
"""query.py: 

Last modified: Sun Aug 31, 2014  02:03PM

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

h1 = logging.StreamHandler(sys.stderr)
h1.setLevel(logging.DEBUG)

logger = logging.getLogger('rscb')
logger.addHandler(h1)
logger.setLevel(logging.INFO)

class Query():

    def __init__(self, args, **kwargs):
        """Create a query with text"""
        self.args = args
        self.queryText = ' '.join(self.args.query)
        self.queryType = self.args.query_type

        logger.info("Querying for: {}".format(self.queryText))
        self.urlbase = 'http://www.rcsb.org/pdb/rest'
        self.url = self.urlbase + '/search'
        self.query = ET.Element("orgPdbQuery")
        self.queryTypePrefix = "org.pdb.query.simple."
        self.addQueryType(args.query_type)
        self.ids = []

    def addQueryType(self, type):
        """Add type to query if given """

        helpText = [ "Currently following types of queries are available:"
                , "1 Structure description"
                , "2 Strucuture tile"
                , "3 Macromolecule name"
                , "4 Text Search, searches for text in file, returns a lot of files"
                ] 

        if "Unspecified" in self.queryType:
            print("\n\t".join(helpText))
            qtype = raw_input("+ Your choice [default 1]:")
            if qtype is None: qtype = 1
            elif len(qtype.strip()) == 0: qtype = 1
            else: qtype = int(qtype.strip())
        else:
            self.queryType = self.queryTypePrefix + 'StructDescQuery'
            qtype = 0

        queryTypeXML = ET.SubElement(self.query, "queryType")

        if qtype == 1:
            self.queryType = self.queryTypePrefix + 'StructDescQuery'
            queryTypeXML.text = self.queryType
            childXml = ET.SubElement(self.query, "entity.pdbx_description.comparator")
            childXml.text = "contains"
            childXml = ET.SubElement(self.query, "entity.pdbx_description.value")
            childXml.text = self.queryText

        elif qtype == 2:
            self.queryType = self.queryTypePrefix + 'StructTitleQuery'
            queryTypeXML.text = self.queryType
            childXml = ET.SubElement(self.query, "struct.title.comparator")
            childXml.text = "contains"
            childXml = ET.SubElement(self.query, "struct.title.value")
            childXml.text = self.queryText

        elif qtype == 3:
            self.queryType = self.queryTypePrefix + 'MoleculeNameQuery'
            queryTypeXML.text = self.queryType
            childXml = ET.SubElement(self.query, "macromoleculeName")
            childXml.text = self.queryText

        else:
            queryTypeXML.text = self.queryType
            keywordsXML = ET.SubElement(self.query, "keywords")
            keywordsXML.text = self.queryText


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
        size = kwargs.get('size', None)
        if not size:
            size = min(100, len(self.ids))

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
        with open(
                os.path.join(self.args.download_dir, 'custom_report.{}'.format(format))
                , "w") as f:
            print("INFO: Storing custom report: {}".format(self.args.download_dir))
            f.write(self.report)

    def printReport(self):
        """Write report to console"""
        tree = ET.fromstring(self.report)
        for child in tree.findall('./record'):
            print("\n++++++++++")
            for c in child:
                print("{:>25} : {}".format(c.tag.split('.')[-1], c.text))


