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

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
    def handle_starttag(self, tag, attrs):
        if (tag == 'br'):
            self.fed.append("\n")
    def handle_entityref(self, name):
        if (name == 'nbsp'):
            self.fed.append(' ')
        elif (name == 'lt'):
            self.fed.append('<')
        elif (name == 'gt'):
            self.fed.append('>')
        elif (name == 'amp'):
            self.fed.append('&')
        elif (name == 'excl'):
            self.fed.append('!')
        elif (name == 'quot'):
            self.fed.append('"')
        elif (name == 'num'):
            self.fed.append('#')
        elif (name == 'percnt'):
            self.fed.append('%')
        elif (name == 'apos'):
            self.fed.append('\'')
        elif (name == 'lpar'):
            self.fed.append('(')
        elif (name == 'rpar'):
            self.fed.append(')')
        elif (name == 'comma'):
            self.fed.append(',')
        elif (name == 'period'):
            self.fed.append('.')
        elif (name == 'lsqb'):
            self.fed.append('[')
        elif (name == 'lbrack'):
            self.fed.append('[')
        elif (name == 'rsqb'):
            self.fed.append(']')
        elif (name == 'rbrack'):
            self.fed.append(']')

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
