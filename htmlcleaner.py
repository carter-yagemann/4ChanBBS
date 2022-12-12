#
#    4Chan BBS
#    HTML Cleanner - htmlcleaner.py
#
#    Copyright Carter Yagemann 2014
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    See <http://www.gnu.org/licenses/> for a full copy of the license.
#

from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

        self.entities = {
            'nbsp': ' ',
            'lt': '<',
            'gt': '>',
            'amp': '&',
            'excl': '!',
            'quot': '"',
            'num': '#',
            'percnt': '%',
            'apos': '\'',
            'lpar': '(',
            'rpar': ')',
            'comma': ',',
            'period': '.',
            'lsqb': '[',
            'lbrack': '[',
            'rsqb': ']',
            'rback': ']'
        }

    def handle_data(self, data):
        self.fed.append(data)

    def get_data(self):
        return ''.join(self.fed)

    def handle_starttag(self, tag, attrs):
        if tag == 'br':
            self.fed.append("\n")

    def handle_charref(self, name):
        self.fed.append(self.entities.get(name, ''))

    def handle_entityref(self, name):
        self.fed.append(self.entities.get(name, ''))


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
