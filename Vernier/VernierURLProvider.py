#!/usr/bin/python

"""
Vernier Software YML to URL Provider
"""

from __future__ import absolute_import
import urllib2
import urlparse

from autopkglib import Processor, ProcessorError

__all__ = "VernierURLProvider"


class VernierURLProvider(Processor):
    description = "Converts Vernier yaml release to a URL"
    input_variables = {
        "apptype": {
            "required": True,
            "description": "Determins which app to download the yml to convert to a release url. Use ga for Graphical Analysis and sa for Spectral Analysis"
            }
        }
    output_variables = {
        "url": {
            "description": "The full url for the file you want to download."
        },
        "version": {
            "description": "The version of the support download"
        }
    }

    def main(self):
        apptype = self.env["apptype"]
        self.output("App choosen is: {}".format(self.env["apptype"]))
        header = {'User-Agent': 'Mozilla/5.0'}
        url = "http://software-releases.graphicalanalysis.com/{0}/mac/release/release-mac.yml".format(apptype)
        req = urllib2.Request(url, headers=header)
        file = urllib2.urlopen(req)
        data = file.read().split()
        dmgpath = data[data.index("path:")+1].rsplit(".", 1)[0] + ".dmg"
        fileurl = urlparse.urljoin(url, dmgpath)
        self.output("DMG URL is {}".format(fileurl))
        self.env["url"] = fileurl
        self.output("Version is {}".format(data[data.index("version:")+1]))
        self.env["version"] = data[data.index("version:")+1]


if __name__ == "__main__":
    PROCESSOR = VernierURLProvider()
    PROCESSOR.execute_shell()
