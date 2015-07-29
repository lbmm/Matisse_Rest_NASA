# -*- coding:utf-8 -*-
import urllib2
from datetime import datetime
from xml.dom import minidom
from xml.parsers import expat
import argparse
import logging

from nasaQuery import NASAQuery, NASAQueryException

__REST_NASA__ = 'http://oderest.rsl.wustl.edu/live2/?query=p&output=XML&r=Mf'



class NASAQueryMercury(NASAQuery):

    """ NASAQueryMercury class sets all the parameters needed for the query.
    Ables to perform the query and to return the results

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


    def composeURL(self):
        """
         Need to compose two URLs:
         1- product type pt=cdrnac -> calibrated products
         2- product type pt=ddrnac -> derived  products
         Return: the two urls
        """

        parameters = '&'.join(['%s=%s' % (item, value) for item, value in self.__dict__.iteritems()
                               if value])

        return __REST_NASA__ + '&pt=cdrnac&' + parameters, __REST_NASA__ + '&pt=ddrnac&' +parameters

    @staticmethod
    def read_nodelist(nodelist):
        """
        Utility method to read the content of a nodeList
        :param nodelist:
        :return: string of the xml element
        """
        if nodelist:
            return " ".join(t.nodeValue for t in nodelist[0].childNodes if t.nodeType == t.TEXT_NODE)
        else:
            return None

    def readMetadata(self, xml_tag):
        """
        Read the metadata of the observation
        :param: xml that contains al the metadata information
        :return: dictionary with all metadata read
        """
        from matisseRestNasa.MatisseNASA import matisse_configuration as cfg

        return {(key, self.read_nodelist(xml_tag.getElementsByTagName(value)))
                for key, value in cfg.metadata.iteritems()}

    def fetchData(self, a_url):

        """
        Open the connection to the NASA Rest interface and  to find all the
        files to download.
        A file is indentified by the following sequence:
        <type_of_file><ID>_<freq>_<file_version>.<type of the file>
        e.g is CN0266147010M_IF_4.IMG

        Return:
            a list of URL where to download products files

        """

        info_files = {}
        files = []
        try:
            xmlNASA = urllib2.urlopen(a_url)
            xmldoc = minidom.parseString(xmlNASA.read())
            products = xmldoc.getElementsByTagName('Product')

            for a_tag in products:

                observation_id = self.read_nodelist(a_tag.getElementsByTagName('Observation_id'))

                metadata = self.readMetadata(a_tag)
                type_tag = a_tag.getElementsByTagName('Type')

                if self.read_nodelist(type_tag) == 'Product':
                    url_tag = a_tag.getElementsByTagName('URL')
                    files.append(self.read_nodelist(url_tag))
                    info_files[observation_id] = {'metadata': metadata,
                                                  'files': files}
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
                    logging.critical("Error retrieving data for URL %s: \n" % a_url +
                                     self.read_nodelist(error))
                else:
                    logging.critical("Query didn't produce any files. Please check parameters")
                raise NASAQueryException

        except urllib2.URLError as e:
            logging.critical(e)
        except expat.ExpatError as e:
            logging.critical(e)

        return info_files

    def associateFiles(self):
        """
        Call the fetch data for all the composed URLs
        fetch all information and associate the files to a unique ID
        Return:
           Dictionary key -> observation ID
                      values -> associate files
        """
        all_files, result = [], {}

        for a_url in self.composeURL():
            try:
                tmp_result = self.fetchData(a_url)

                for key in tmp_result:
                    if key in result:
                        result[key]['files'].extend(tmp_result[key]['files'])
                    else:
                        result[key] = tmp_result[key]

            except NASAQueryException as e:
                logging.critical(e)
                continue

        return result


def valid_date(s):
    """"
    Validation of the command line options.
    Check if a date is of the right format
    e.g. = 2013-01-08T15:39:05.169

    Arg: string
    Return: string
    Raise ArgumentTypeError
    """

    try:
        datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f")
        #date string is well formatted
        return s
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def main(parser):

    #creates the NASAQuery obj
    nq = NASAQuery()
    # Parse the arguments and directly load in the NASAQuery namespace
    args = parser.parse_args(namespace=nq)

    #setup the logging
    log_format = "%(message)s"
    if args.log:
        logging.basicConfig(filename=args.log, filemode='w',
                            format=log_format, level=logging.INFO)
    else:
        logging.basicConfig(format=log_format, level=logging.INFO)

    #associate the files
    info_files = nq.associateFiles()

    for key in info_files:
        #skipping only geometry: needs both
        if len(info_files[key]['files']) > 1:
            logging.info('Observation ID: %s' % key)
            logging.info('\n'.join(['%s: %s' % (metadata_key, metadata_value) for metadata_key, metadata_value
                                     in info_files[key]['metadata']]))
            logging.info("fileID: %s;\n files: \n%s" % (key, '\n'.join(info_files[key]['files'])))


if __name__ == "__main__":

    main(parser)



