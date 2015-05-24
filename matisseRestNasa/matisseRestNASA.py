# -*- coding:utf-8 -*-
import string
import urllib2
from datetime import datetime
from xml.dom import minidom
from xml.parsers import expat
import argparse


import logging

FORMAT = "%(message)s"
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


__REST_NASA__ = 'http://oderest.rsl.wustl.edu/live2/?query=p&output=XML&r=f'

"""
To use

"""


class NASAQueryException(Exception):
    pass


class NASAQuery(object):

    """ NASAQuery class sets all the parameters needed for the query.
    Ables to perform the query and to return the results

    Mandatory Attributes:
      target (str): target to query
      ihid (str): ID
      iid (str): instrument ID
    """
    def __init__(self, target=None, ihid=None, iid=None, **parameters):

        self.target = target
        self.ihid = ihid
        self.iid = iid
        #not mandatory parameter, this takes parameters dynamical
        for name, value in parameters.iteritems():
            setattr(self, name, value)



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

        return " ".join(t.nodeValue for t in nodelist[0].childNodes if t.nodeType == t.TEXT_NODE)

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

        files = []
        try:
            xmlNASA = urllib2.urlopen(a_url)
            xmldoc = minidom.parseString(xmlNASA.read())
            product_files = xmldoc.getElementsByTagName('Product_file')
            for a_tag in product_files:

                type_tag = a_tag.getElementsByTagName('Type')

                if self.read_nodelist(type_tag) == 'Product':
                    url_tag = a_tag.getElementsByTagName('URL')
                    files.append(self.read_nodelist(url_tag))
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
                    log.critical("Error retrieving data for URL %s: \n" % a_url +
                                 self.read_nodelist(error))
                else:
                    log.critical("Query didn't produce any files. Please check parameters")
                raise NASAQueryException

        except urllib2.URLError as e:
            log.critical(e)
        except expat.ExpatError as e:
            log.critical(e)

        return files

    def associateFiles(self):
        """
        Call the fetch data for all the composed URLs
        fetch all information and associate the files to a unique ID
        Return:
           Dictionary key -> ID
                      values -> associate files
        """
        all_files, result = [], {}

        for a_url in self.composeURL():
            try:
                all_files.extend(self.fetchData(a_url))
            except NASAQueryException as e:
                log.critical(e)
                continue

        for a_file in all_files:
            file_name = a_file[string.rfind(a_file, "/") + 2:]
            id_filename = file_name[1: string.find(file_name, "_")]
            result.setdefault(id_filename, []).append(a_file)

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
    #associate the files
    files = nq.associateFiles()

    for key, value in files.iteritems():
        log.info("fileID: %s;\n files: \n%s" % (key, '\n'.join(value)))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="")
  # Define the command line options
    parser.add_argument('--target', dest='target',
                        help="PDS target name", required=True)
    parser.add_argument('--ihid', dest='ihid', help="instrument host ID", required=True)
    parser.add_argument('--iid', dest='iid', help="instrument  ID", required=True)

    #coordinates (c1, c2, c3)
    parser.add_argument('--c1min', dest='westernlon', type=float,
                        help="Min of first coordinate (in degrees by default)")
    parser.add_argument('--c1max', dest='easternlon', type=float,
                        help="Max of first coordinate (in degrees by default)")
    parser.add_argument('--c2min', type=float, dest='minlat',
                        help="Min of second coordinate (in degrees by default) ")
    parser.add_argument('--c2max', type=float, dest='maxlat',
                        help="Max of second coordinate (in degrees by default) ")
    """

    parser.add_argument('--c3min', type=float, dest='maxlat',
                        help="Min of third coordinate (in degrees by default) ")
    parser.add_argument('--c3max', type=float, dest='c3max',
                        help="Max of third coordinate (in degrees by default) ")
    """
    #times
    parser.add_argument('--Time_min', dest='minobtime', type=valid_date,
                        help="Acquisition start time - format YYYY-MM-DDTHH:MM:SS.m")
    parser.add_argument('--Time_max', dest='maxobtime', type=valid_date,
                        help="Acquisition stop time - format YYYY-MM-DDTHH:MM:SS.m")
    #angles

    parser.add_argument('--Incidence_min', dest='mininangle', type=float,
                        help="Min incidence angle (solar zenithal angle)")

    parser.add_argument('--Incidence_max', dest='maxinangle', type=float,
                        help="Max incidence angle (solar zenithal angle)")

    parser.add_argument('--Emerge_min', dest='minemangle', type=float,
                        help="Min emerge angle")

    parser.add_argument('--Emerge_max', dest='maxemangle', type=float,
                        help="Max emerge angle")

    parser.add_argument('--Phase_min', dest='minphangle', type=float,
                        help="Min phase angle")

    parser.add_argument('--Phase_max', dest='maxpjangle', type=float,
                        help="Max phase angle")

    main(parser)



