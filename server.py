# %% This is so code can be run as cell in vscode
"""
Some parts of template code were taken from here https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7
I believe this is fair use as it's why we have google for and people need to learn somehow.

Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
from github import Github
"""
it's initialized with no authorization token nor it's not using enterprise server of github 
change this if you want more requests / different server
"""
g = Github()

class Server(BaseHTTPRequestHandler):
    def _set_response(self,code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def handle_API_exception(self,e):
        self._set_response(404)
        """
        This should be a simple project and this code would probably quadruple in size if I was to parse every
        possible exception, at the same time if user provides bad data from which I can't recover anyway. The best course of
        action is to pass issue to them and make sure server still stays online. 
        """
        self.wfile.write("Probably typo in user name. More details bellow  <br>".encode('utf-8'))
        self.wfile.write("""<img src="https://http.cat/{}.jpg" alt="No image for you"> <br>""".format(str(e)[:3]).encode('utf-8'))
        self.wfile.write(str(e).encode('utf-8'))

    def do_GET(self):
        if(self.path.startswith("/repos/")): 
            try:    
                user = g.get_user(self.path[len("/repos/"):]) #I'm conflicted on how clean this is but I don't thing exposing path as variable in this code would make it cleaner
                self._set_response(200)
                """
                Generally you did not specified how output should be formated so I'm using simple strings of text 
                / this is default for somethign like algorithmic contests.
                """
                self.wfile.write("Repository name | number of stars <br>".encode('utf-8'))
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
        """
        This is probably unnecessary but I though why not. 
        """
        if(self.path.startswith("/favicon.ico")):
            self._set_response(200)
            with open('favicon.ico', 'rb') as file: 
                self.wfile.write(file.read()) # Read the file and send the contents 
            return
        self._set_response(400)
        self.wfile.write("Failed GET request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Server, port=8420):
    logging.basicConfig(level=logging.INFO) # This can be left or removed
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
