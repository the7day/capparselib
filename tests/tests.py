#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" These are the tests for the the capparselib module. """

__author__ = 'kelvinn'
__email__ = 'kelvin@kelvinism.com'

import os
import sys
import unittest
import chardet
from io import open

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(TEST_ROOT, os.pardir)

os.chdir(TEST_ROOT)
sys.path.insert(0, os.path.dirname(TEST_ROOT))

from src.parsers import CAPParser

# filename, cap type, num alerts, sent time, sender

CAP_DATA_FILES = [
    ["resources/weather.cap", "CAP1_1", 1, "2014-05-10T22:00:00-06:00", "w-nws.webmaster@noaa.gov"],
    ["resources/amber.atom", "ATOM", 1, "2010-06-03T19:15:00-05:00", "KARO@CLETS.DOJ.DC.GOV"],
    ["resources/australia.cap", "CAP1_2", 1, "2011-10-05T23:04:00+10:00", "webmaster@rfs.nsw.gov.au"],
    ["resources/earthquake.cap", "CAP1_1", 1, "2010-08-31T00:09:25-05:00",
     "http://earthquake.usgs.gov/research/monitoring/anss/neic/"],
    ["resources/earthquake-iso8859-1.cap", "CAP1_2", 1, "2012-10-14T22:53:04+00:00",
     "http://earthquake.usgs.gov/research/monitoring/anss/neic/"],
    # ["resources/sweden.xml", "CAP1_2", 11105, "2018-10-12T11:05:18+02:00", "https://www.krisinformation.se/"],
    # ["resources/mexico.atom", "ATOM", 469, "2014-10-31T21:15:00-06:00", "smn.cna.gob.mx"],
    ["resources/mexico.xml", "CAP1_2", 1, "2018-10-20T07:15:00-05:00", "smn.cna.gob.mx"],
    ["resources/taiwan.cap", "CAP1_2", 1, "2014-05-14T20:10:00+08:00", "ddmt01@wra.gov.tw"],
    ["resources/ph.cap", "CAP1_2", 1, "2014-11-03T14:57:33+08:00", "PAGASA-DOST"],
    ["resources/no_info_tag.cap", "CAP1_2", 1, "2016-02-25T12:47:09-08:00", "AtHoc"],
    ["resources/wcatwc-warning.cap", "CAP1_2", 1, "2011-09-02T11:36:50-00:00", "http://newwcatwc.arh.noaa.gov/tsuPortal/"]
]


class TestCAPParser_1_1(unittest.TestCase):
    def setUp(self):
        with open('resources/weather.cap', 'br') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
            self.cap_object = CAPParser(data.decode(encoding))

    def test_determine_cap_type(self):
        self.cap_object.determine_cap_type()
        self.assertEqual("CAP1_1", self.cap_object.cap_xml_type)

    def test_get_objectified_xml(self):
        self.cap_object.determine_cap_type()
        objectified_xml = self.cap_object.get_objectified_xml()
        children = objectified_xml.info.getchildren()
        self.assertIsNotNone(children)

    def test_parse_alert(self):
        self.cap_object.determine_cap_type()
        objectified_xml = self.cap_object.get_objectified_xml()
        alert_dict = self.cap_object.parse_alert(objectified_xml)
        self.assertEqual("2014-05-10T22:00:00-06:00", alert_dict['cap_sent'])

    def test_load(self):
        self.cap_object.load()
        result = self.cap_object.alert_list
        self.assertEqual("w-nws.webmaster@noaa.gov", result[0]["cap_sender"])


class TestCAPParser_1_2(unittest.TestCase):
    def setUp(self):
        with open('resources/taiwan.cap', 'br') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
            self.cap_object = CAPParser(data.decode(encoding))

    def test_determine_cap_type(self):
        self.cap_object.determine_cap_type()
        self.assertEqual("CAP1_2", self.cap_object.cap_xml_type)

    def test_get_objectified_xml(self):
        self.cap_object.determine_cap_type()
        objectified_xml = self.cap_object.get_objectified_xml()
        children = objectified_xml.info.getchildren()
        self.assertIsNotNone(children)

    def test_parse_alert(self):
        self.cap_object.determine_cap_type()
        objectified_xml = self.cap_object.get_objectified_xml()
        alert_dict = self.cap_object.parse_alert(objectified_xml)
        self.assertEqual("2014-05-14T20:10:00+08:00", alert_dict['cap_sent'])

    def test_load(self):
        self.cap_object.load()
        result = self.cap_object.alert_list
        self.assertEqual("ddmt01@wra.gov.tw", result[0]["cap_sender"])


class TestCAPParser_ATOM(unittest.TestCase):
    def setUp(self):
        with open('resources/amber.atom', 'br') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
            self.cap_object = CAPParser(data.decode(encoding))

    def test_determine_cap_type(self):
        self.cap_object.determine_cap_type()
        self.assertEqual("ATOM", self.cap_object.cap_xml_type)

    def test_get_objectified_xml(self):
        self.cap_object.determine_cap_type()
        objectified_xml = self.cap_object.get_objectified_xml()
        children = objectified_xml.entry.getchildren()
        self.assertIsNotNone(children)

    def test_load(self):
        self.cap_object.load()
        result = self.cap_object.alert_list
        self.assertEqual("KARO@CLETS.DOJ.DC.GOV", result[0]["cap_sender"])


class TestCAPParser_EDXLDE(unittest.TestCase):
    def setUp(self):
        with open('resources/bushfire_valid.edxlde', 'br') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
            self.cap_object = CAPParser(data.decode(encoding))

    def test_load(self):
        self.cap_object.load()
        result = self.cap_object.alert_list
        self.assertEqual(9, len(result[0]))

    def test_as_dict(self):
        alerts = self.cap_object.as_dict()
        self.assertEqual(59, len(alerts))


class TestInvalid(unittest.TestCase):
    def setUp(self):
        self.data = None
        with open('resources/invalid.cap', 'br') as f:
            self.data = f.read()
            self.encoding = chardet.detect(self.data)['encoding']

    def test_invalid(self):
        self.assertRaises(Exception, CAPParser, self.data.decode(self.encoding))


class TestSequence(unittest.TestCase):
    cap_object = None
    pass


def test_generator(filename, cap_xml_type, cap_alert_count, cap_sent, cap_sender):

    def test(self):
        with open(filename, 'br') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
            self.cap_object = CAPParser(data.decode(encoding))
            self.cap_object.determine_cap_type()
            self.assertEqual(cap_xml_type, self.cap_object.cap_xml_type)

    def test_cap_load(self):
        with open(filename, 'br') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
            self.cap_object = CAPParser(data.decode(encoding))
            result = self.cap_object.alert_list
            self.assertEqual(cap_sender, result[0]["cap_sender"])
            self.assertEqual(cap_sent, result[0]['cap_sent'])
            self.assertEqual(cap_alert_count, len(result))

    def test_parse_alert(self):
        with open(filename, 'br') as f:
            data = f.read()
            encoding = chardet.detect(data)['encoding']
            if encoding is not 'ascii':
                self.cap_object = CAPParser(data.decode(encoding))
            else:
                self.cap_object = CAPParser(data.decode('utf-8'))
            alert_list = self.cap_object.get_alert_list()
            alert = alert_list[0]
            alert_dict = self.cap_object.parse_alert(alert)
            self.assertEqual(cap_sent, alert_dict['cap_sent'])

    return test, test_cap_load, test_parse_alert


if __name__ == '__main__':

    # This creates dynamic test cases to test many files
    for t in CAP_DATA_FILES:
        test_name = 'test_%s' % t[0].split("/")[1].replace(".", "_")
        test, test_cap_load, test_parse_alert = test_generator(t[0], t[1], t[2], t[3], t[4], )
        setattr(TestSequence, test_name, test)
        setattr(TestSequence, test_name + "_cap_load", test_cap_load)
        setattr(TestSequence, test_name + "_parse_alert", test_parse_alert)
    unittest.main()
