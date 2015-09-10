# -*- coding:utf-8 -*-
import urllib2
from xml.dom import minidom
from xml.parsers import expat
import logging

from nasaQuery import NASAQuery, NASAQueryException
import NASAparserconfig


class NASAQueryMoon(NASAQuery):

    """ NASAQueryMoon class sets all the parameters needed for the query.
    Ables to perform the query and to return the results

    Mandatory Attributes:
      ihid (str): ID
      iid (str): instrument ID
    """

    def __init__(self, ihid=None, iid=None, **parameters):
        """
        Defines mandatory parameters for the observation
        set the target to 'moon'
        :param ihid: ihid (ID) of the observation
        :param iid: iid (instrument ID) of the observation
        """

        super(NASAQuery, self).__init__()
        self.target = 'moon'

    def extractFiles(self, a_tag):
        """
        Extract observation metadata, ID name, and URL links
        Each mission has a different way to retrieve data
        :param  a selected xml tag
        :return: info_files (metadata and associated files based on the file ID)
        """

        files, geometry_files = [], []
        #loops over the product tag and select for each product the product files

        if self.ihid == 'CLEM' and self.iid == 'HIRES':
            product_file = a_tag.getElementsByTagName("Product_file")
            for a_file in product_file:
               #loop over the product_file for each product
                  type_tag = a_file.getElementsByTagName('Type')
                  #select the type tag Product
                  if self.read_nodelist(type_tag) == 'Product':
                        files.append(self.read_nodelist(a_file.getElementsByTagName('URL')))

        elif self.ihid == 'LRO' and self.iid == 'LROC':
            files.append(self.read_nodelist(a_tag.getElementsByTagName('LabelURL')))

        elif self.ihid == 'CH1-ORB' and self.iid == 'M3':
            product_file = a_tag.getElementsByTagName("Product_file")
            for a_file in product_file:
                type_tag = a_file.getElementsByTagName('Type')
                if self.read_nodelist(type_tag) == 'Product':
                    file_name = self.read_nodelist(a_file.getElementsByTagName('FileName'))

                    if file_name.endswith('LOC.IMG'):
                        geometry_files.append(self.read_nodelist(a_file.getElementsByTagName('URL')))

                    elif file_name.endswith('RDN.IMG'):
                        files.append(self.read_nodelist(a_file.getElementsByTagName('URL')))

        return files, geometry_files


    def fetchData(self):
        """
        Extract observation metadata + Footprint Geometry, ID name, and LabelURL links
        :return: info_files (metadata and associated files based on the file ID)
        """

        info_files = {}
        #select here what to read from the configuration define by mission and instrument
        config = NASAparserconfig.configurations_moon[self.ihid][self.iid]
        try:

            xmlNASA = urllib2.urlopen(self.composeURL(config['pt']))
            xmldoc = minidom.parseString(xmlNASA.read())

            #here select all the product tags
            products = xmldoc.getElementsByTagName('Product')
            for a_tag in products:
                files, geometry_files = self.extractFiles(a_tag)
                info_files[self.read_nodelist(a_tag.getElementsByTagName('pdsid'))] = \
                     {'metadata': self.readMetadata(a_tag), 'files': files}
                if geometry_files:
                    info_files[self.read_nodelist(a_tag.getElementsByTagName('pdsid'))].update({'geometry_files': geometry_files})
                 #no result: two options
                 #1- NASA page returns error
                 #2- query didn't produce output
                if not files:
                    #check if there was an error
                    error = xmldoc.getElementsByTagName('Error')
                    if error:
                        logging.critical("Error retrieving data for URL %s: \n" % self.composeURL(config['pt']) +
                                         self.read_nodelist(error))
                    else:
                        logging.critical("Query didn't produce any files. Please check parameters")
                    raise NASAQueryException

        except urllib2.URLError as e:
            logging.critical(e)
        except expat.ExpatError as e:
            logging.critical(e)

        return info_files


def add_required_arguments(parser):
    """
    set specific  parameters to the command line parser
    :param parser:
    :return:
    """

    requiredNamed = parser.add_argument_group('required  arguments')

    requiredNamed.add_argument('--ihid', dest='ihid', help="instrument host ID", choices=NASAparserconfig.ihid_moon,
                               required=True)
    requiredNamed.add_argument('--iid', dest='iid', help="instrument  ID", choices=NASAparserconfig.iid_moon,
                               required=True)

def main(parser):

    #creates the NASAQuery obj
    nq = NASAQueryMoon()
    # Parse the arguments and directly load in the NASAQuery namespace
    args = parser.parse_args(namespace=nq)

    #setup the logging
    log_format = "%(message)s"
    if args.log:
        logging.basicConfig(filename=args.log, filemode='w',
                            format=log_format, level=logging.INFO)
    else:
        logging.basicConfig(format=log_format, level=logging.INFO)

    info_files = nq.fetchData()
    nq.print_info(info_files, logging)



if __name__ == "__main__":

    parser = NASAparserconfig.argumentParser('Matisse Nasa query for the Moon target')
    add_required_arguments(parser)
    main(parser)
