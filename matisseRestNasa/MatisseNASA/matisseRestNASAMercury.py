# -*- coding:utf-8 -*-
import urllib2
from datetime import datetime
from xml.dom import minidom
from xml.parsers import expat
import argparse
import logging


from nasaQuery import NASAQuery, NASAQueryException
import NASAparserconfig


class NASAQueryMercury(NASAQuery):

    """ NASAQuery class sets all the parameters needed for the query.
    Ables to perform the query and to return the results.
    NASAQueryMercury class specific for the mercury target

    Available ihid, and iid set in the NASAparserconfig

    Mandatory Attributes:
      ihid (str): ID
      iid (str): instrument ID
    """

    def __init__(self, ihid=None, iid=None, **parameters):
        """
        Defines mandatory parameters for the observation
        :param ihid: ihid (ID) of the observation
        :param iid: iid (instrument ID) of the observation
        """

        super(NASAQuery, self).__init__()
        self.target = 'mercury'


    def fetchDataWithPt(self, pt):

        """
        Open the connection to the NASA Rest interface and  to find all the
        files to download.
        A file is indentified by the following sequence:
        <type_of_file><ID>_<freq>_<file_version>.<type of the file>
        e.g is CN0266147010M_IF_4.IMG

        Return:

          a dictionary with metadata information and files url.
          in case of analysis of the geometry xml, only the information regarding
          the file_path is saved

        """

        info_files = {}
        files = []
        try:
            xmlNASA = urllib2.urlopen(self.composeURL(pt))
            xmldoc = minidom.parseString(xmlNASA.read())
            products = xmldoc.getElementsByTagName('Product')

            for a_tag in products:

                observation_id = self.read_nodelist(a_tag.getElementsByTagName('Observation_id'))

                metadata = self.readMetadata(a_tag)
                type_tag = a_tag.getElementsByTagName('Type')

                if self.read_nodelist(type_tag) == 'Product':
                    url_tag = a_tag.getElementsByTagName('URL')
                    files.append(self.read_nodelist(url_tag))

                    if pt == 'ddrnac':
                        info_files.setdefault(observation_id, {}).update({'geometry_files': files})
                    else:

                        info_files.setdefault(observation_id, {}).update({'metadata': metadata,
                                                                         'files': files})

                    #one product file per <Product_file> tag
                    #continue the loop
                    continue
            #no result: two options
            #1- NASA page returns error
            #2- query didn't produce output
            if not files:
                #check if there was an error
                error = xmldoc.getElementsByTagName('Error')
                if error:
                    logging.critical("Error retrieving data for URL %s: \n" % self.composeURL(pt) +
                                     self.read_nodelist(error))
                else:
                    logging.critical("Query didn't produce any files. Please check parameters")
                raise NASAQueryException

        except urllib2.URLError as e:
            logging.critical(e)
        except expat.ExpatError as e:
            logging.critical(e)

        return info_files

    def fetchData(self):
        """
        Call the fetch data for all the composed URLs
        fetch all information and associate the files to a unique ID
        Return:
           Dictionary key -> observation ID
                      values -> associate files
        """
        result = {}
        #type of pt to query to obtain the product files (cdrnac)
        # and geometry files (ddrnac)
        pt = ['cdrnac', 'ddrnac']
        for a_pt in pt:
            try:
                if not result:
                    result = self.fetchDataWithPt(a_pt)
                else:
                    tmp_result = self.fetchDataWithPt(a_pt)
                    for key in tmp_result:
                        result.setdefault(key, {}).update(tmp_result[key])

            except NASAQueryException as e:
                logging.critical(e)
                continue


        return result

def add_required_arguments(parser):
    """
    set specific  parameters to the command line parser
    :param parser:
    :return:
    """

    requiredNamed = parser.add_argument_group('required  arguments')
    requiredNamed.add_argument('--ihid', dest='ihid', help="instrument host ID", choices=NASAparserconfig.ihid_mercury,
                               required=True)
    requiredNamed.add_argument('--iid', dest='iid', help="instrument  ID", choices=NASAparserconfig.iid_mercury,
                               required=True)


def main(parser):

     #creates the NASAQueryMercury obj
    nq = NASAQueryMercury()
    # Parse the arguments and directly load in the NASAQueryMercury namespace
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

    parser = NASAparserconfig.argumentParser('Matisse Nasa query for the Mercury target')
    add_required_arguments(parser)
    main(parser)



