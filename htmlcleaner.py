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

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
