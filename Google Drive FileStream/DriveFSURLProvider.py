#!/usr/bin/python

"""
From https://gist.github.com/opragel/681fbf91f2d2aba548bac83049bd891b#file-google_drivefs_update_checker-py
by Owen Pragel
"""

import xml.etree.ElementTree as ET
import uuid
import urllib2
import urllib

from autopkglib import Processor, ProcessorError

__all__ = "DriveFSURLProvider"

class DriveFSURLProvider(Processor):
    description = "Provides latest Drive FileStream URL"
    input_variables = {}
    output_variables = {
        "url": {
            "description": "The full url for the file you want to download."
        },
        "version": {
            "description": "The version of the support download"
        }
    }


    def main(self):
        params = {'cup2hreq': 'foo', 'cup2key': 'bar'}

        platform = 'mac'
        os_version = '10.12'

        xml = """
        <request protocol="3.0" requestid="{%s}">
                <os platform="%s" version="%s" />
                <app appid="com.google.drivefs" lang="en-us">
                        <updatecheck />
                </app>
        </request>
        """ % (str(uuid.uuid1()), platform, os_version)

        url_params = urllib.urlencode(params)
        url = urllib2.Request('https://tools.google.com/service/update2', data=url_params)
        url.add_header('Content-Type', 'application/xml')
        output_url = urllib2.urlopen(url, xml)

        root = ET.fromstring(output_url.read())

        dmg_url_list = []
        version_list = []

        for tag in root.iter('url'):
            dmg_url_list.append(tag.attrib['codebase'])
            break

        for tag in root.iter('manifest'):
            version_list.append(tag.attrib['version'])

        for tag in root.iter('package'):
            dmg_url_list.append(tag.attrib['name'])

        dmg_url = ''.join(dmg_url_list)
        version = ''.join(version_list)
        self.env["url"] = dmg_url
        self.env["version"] = version

if __name__ == "__main__":
    PROCESSOR = DriveFSURLProvider()
    PROCESSOR.execute_shell()
