from os import path

from edurov import WebMethod

web_method = WebMethod(
    index_file=path.join(path.dirname(__file__), 'index.html')
)
web_method.serve()
