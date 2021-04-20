# %%
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from github import Github
g = Github()

class S(BaseHTTPRequestHandler):
    def _set_response(self,code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def handle_API_exception(self,e):
        self._set_response(404)
        """
        This should be a simple procject and this code base would probably double in size if I was to parse every /
        possible exception, at the same time if user provides bad data from which I can't recover anyway best course of  /
        action is to pass issue to them and make sure server still stays online. 
        """
        self.wfile.write("Probably typo in user name. More details bellow  <br>".encode('utf-8'))
        self.wfile.write("""<img src="https://http.cat/{}.jpg" alt="No image for you"> <br>""".format(str(e)[:3]).encode('utf-8'))
        self.wfile.write(str(e).encode('utf-8'))

    def do_GET(self):
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        if(self.path.startswith("/repos/")): 
            try:    
                user = g.get_user(self.path[len("/repos/"):])
                self._set_response(200)
                self.wfile.write("Repository name | number of stars <br>").encode('utf-8')
                for repo in user.get_repos():
                    print(repo.name+" "+str(repo.stargazers_count) )
                    self.wfile.write((repo.name+" "+str(repo.stargazers_count)+"<br>").encode('utf-8'))    
            except Exception as e:
                self.handle_API_exception(e)
            return
        if(self.path.startswith("/stars/")):
            try:
                user = g.get_user(self.path[len("/stars/"):])
                sum_of_stars = 0
                for repo in user.get_repos():
                    sum_of_stars += repo.stargazers_count
                self._set_response(200)
                self.wfile.write("Total number of stars {}.".format(sum_of_stars).encode('utf-8')) 
            except Exception as e:
                self.handle_API_exception(e)
            return
        if(self.path.startswith("/favicon.ico")):
            self._set_response(200)
            with open('favicon.ico', 'rb') as file: 
                self.wfile.write(file.read()) # Read the file and send the contents 
            return
        self._set_response(400)
        self.wfile.write("Failed GET request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8420):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting server on port {}\n'.format(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stoping server\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()



# %%
