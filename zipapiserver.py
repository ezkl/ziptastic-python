import time
import BaseHTTPServer
import urlparse
import json
import redis

HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 80 # Maybe set this to 9000.

class ZipAPIServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        # Get the zip from the data
        qs = {}
        path = s.path
        the_zip = None
        if '?' in path:
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)
            the_zip = qs['zip']
        elif path:
            the_zip = [path.strip('/')]

        if the_zip:
            r = redis.Redis(host='localhost', port=6379, db=0)
            
            row = r.hvals("zip:{zip}".format(zip=str(the_zip[0])))
            if row is not None:
                s.send_response(200)
                # The Magic!
                s.send_header("Access-Control-Allow-Origin", "*")
                s.send_header("Content-type", "application/json")
                s.end_headers()
                    
                data = dict(zip(('country', 'state', 'city'), row))
                s.wfile.write(json.dumps(data))
            else:
                # The Magic!
                s.send_response(404)
                s.send_header("Access-Control-Allow-Origin", "*")
                s.send_header("Content-type", "text/plain")
                s.end_headers()
                s.wfile.write("404 - Not Found")


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), ZipAPIServerHandler)
    #print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
