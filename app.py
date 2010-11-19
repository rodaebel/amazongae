from config import AWS_KEY, SECRET_KEY
from amazonproduct import API, AWSError
from amazonproduct import ResultPaginator

from xml.dom.minidom import parse

import cgi


def minidom_response_parser(fp):
    """
    Custom response parser using xml.dom.minidom.parse 
    instead of lxml.objectify.
    """
    root = parse(fp)
    
    # parse errors
    for error in root.getElementsByTagName('Error'):
        code = error.getElementsByTagName('Code')[0].firstChild.nodeValue
        msg = error.getElementsByTagName('Message')[0].firstChild.nodeValue
        raise AWSError(code, msg)
    
    return root

if __name__ == '__main__':
    
    api = API(AWS_KEY, SECRET_KEY, 'us',
              processor=minidom_response_parser)
    root = api.item_lookup('0718155157')
    
    contents = root.childNodes[0].childNodes[-1].childNodes[-1].childNodes[-1].toprettyxml()
    print "<html>"
    print "<body><pre>%s</pre></body>" % cgi.escape(contents)
    print "</html>"
