# -*- coding:utf-8 -*-

__REST_NASA__ = 'http://oderest.rsl.wustl.edu/live2/?query=p&output=XML&r=Mfp'


class NASAQueryException(Exception):
    pass


class NASAQuery(object):

    """ NASAQuery abstract class. sets all the parameters needed for the query.
    Ables to perform the query and to return the results

    Mandatory Attributes:
      target(str) : target
      ihid (str): ID
      iid (str): instrument ID
    """

    def __init__(self, target=None, ihid=None, iid=None, **parameters):
        """
        Defines mandatory parameters for the observation
        :param target: planet target
        :param ihid: ihid (ID) of the observation
        :param iid: iid (instrument ID) of the observation
        """

        self.target = target
        self.ihid = ihid
        self.iid = iid
        #not mandatory parameter, this takes parameters dynamical
        for name, value in parameters.iteritems():
            setattr(self, name, value)


    def composeURL(self, pt):
        """
         single URL:
         compose the url with pt hardcoded
         Return: url string 
        """

        parameters = '&'.join(['%s=%s' % (item, value) for item, value in self.__dict__.iteritems()
                               if value])

        return __REST_NASA__ + '&pt=%s&' % pt + parameters


    def readMetadata(self, xml_tag):
        """
        Read the metadata of the observation
        :param: xml that contains al the metadata information
        :param: ihid of the observation
        :return: dictionary with all metadata read
        """

        import matisse_configuration as cfg

        return {(key, self.read_nodelist(xml_tag.getElementsByTagName(value)))
                for key, value in cfg.getMetadata(self.ihid).iteritems()}

    @property
    def fetchData(self):
        raise NotImplementedError("Subclasses should implement this!")

    @property
    def extractFiles(self, a_tag):
        raise NotImplementedError("Subclasses should implement this!")

    @staticmethod
    def read_nodelist(nodelist):
        """
        Utility method to read the content of a nodeList
        :param nodelist
        :return: string of the xml element
        """

        if nodelist:
            return " ".join(t.nodeValue for t in nodelist[0].childNodes if t.nodeType == t.TEXT_NODE)
        else:
            return None


