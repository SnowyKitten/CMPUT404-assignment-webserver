#  coding: utf-8 
import SocketServer


# Copyright 2016 Abram Hindle, Eddie Antonio Santos, Randy Wong, Marcin Pietrasik
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        readRequest = self.data.split("\r")
        HTTPRequest = readRequest[0]
        requestedResource = self.HTTPParser(HTTPRequest)

        # if we end our query with /, we want the index.html in that folder
        if (requestedResource[-1] == "/"):
            requestedResource = requestedResource + "index.html"

        try:
            # handle client being rude, send them a 404
            if "/.." in requestedResource:
               raise

            resource = open("www" + requestedResource, "r")
            # send success header
            self.request.sendall("HTTP/1.1 200 OK\r\n")
            # finds the MIME extension for the resource
            fileType = requestedResource.split(".")[-1]
            # sends header line with extension type
            self.request.sendall("Content-Type: text/" + fileType + ";\r\n\r\n")
            # send resource
            self.request.sendall(resource.read())

        except:
            # can't open a resource, not found, or directed here when client tries to use /..
            self.request.sendall("HTTP/1.1 404 Not Found\r\n\r\n 404 Not Found")


    def HTTPParser(self, HTTPString):
        pageRequest = HTTPString.split(" ")
        if pageRequest[0] != "GET":
            return -1
        return pageRequest[1]

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
