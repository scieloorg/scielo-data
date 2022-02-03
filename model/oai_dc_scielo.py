import logging
import xml.parsers.expat
import xmltodict

from lxml import etree
from lxml.etree import SerialisationError
from sickle._compat import PY3
from sickle.models import Record, Header


class SciELOHeader(Header):
    def __init__(self, header_element):
        super(Header, self).__init__(header_element, strip_ns=True)
        self.deleted = self.xml.attrib.get('status') == 'deleted'

        _identifier_element = self.xml.find('dc:identifier', self.xml.nsmap)
        _date_element = self.xml.find('date', self.xml.nsmap)
        _is_part_of = self.xml.findall('dc:isPartOf', self.xml.nsmap)
        
        self.identifier = getattr(_identifier_element, 'text', None)
        self.date = getattr(_date_element, 'text', None)
        self.is_part_of = [isPartOf.text for isPartOf in _is_part_of]

    def __repr__(self):
        if self.deleted:
            return '<Header %s [deleted]>' % self.identifier
        else:
            return '<Header %s>' % self.identifier

    def __iter__(self):
        return iter([
            ('identifier', self.identifier),
            ('date', self.date),
            ('is_part_of', self.is_part_of)
        ])


class SciELORecord(Record):
    def __init__(self, record_element, strip_ns=True):
        super(Record, self).__init__(record_element, strip_ns=strip_ns)
        self.header = SciELOHeader(self.xml.find('.//' + self._oai_namespace + 'header'))
        self.deleted = self.header.deleted
        if not self.deleted:
            self.metadata = self.get_metadata()

    def __repr__(self):
        if self.header.deleted:
            return '<Record %s [deleted]>' % self.header.identifier
        else:
            return '<Record %s>' % self.header.identifier

    def __iter__(self):
        return iter(self.metadata.items()) if PY3 else self.metadata.iteritems()

    def get_metadata(self):
        xml_metadata = self.xml.find('.//' + self._oai_namespace + 'metadata')
        try:
            return xmltodict.parse(xml_input=etree.tostring(xml_metadata), process_namespaces=False)
        except xml.parsers.expat.ExpatError as e:
            logging.error(e)
            return {}
        except SerialisationError as e:
            logging.error(e)
            return {}
