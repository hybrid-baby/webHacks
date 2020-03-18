#content managers
#all you do is point it to the content managers directory
#crawler for content managers
import Queue as Q
import threading as t
import os
import urllib2 as url2
import argparse as agp

print "==================================================================="
print "[*] CREATED  BY HYBRID-BABY powered by BINARYLABSKE.CO.KE [*!...]"
print "==================================================================="
print "   "
print "===================================="
print "[*]  Content Manager Crawler [*!...]"
print "===================================="


#define the target url and threads to be used as the arguement to be passed
parser = agp.ArgumentParser(description="Crawler for content managers")
parser.add_argument("target",help="set the tagets url")
parser.add_argument("dir",help="give the directory to the CMS")
parser.add_argument("threads",help="Set the number of threads to use",type=int)
args = parser.parse_args()

filters = [".jpg",".jpeg",".gif",".png",".css"]
os.chdir(args.dir)

#store paths in a Queque
web_paths = Q.Queue()
for r,d,f in os.walk("."):
    for files in f:
        remote_path = "%s/%s" % (r,files)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (args.target,path)
        request = url2.Request(url)
        try:
            response = url2.urlopen(request)
            content = response.read()
            print"!!** [%d] => %s" % (response.code,path)
            response.close()

        except url2.HTTPError as e:
            pass

#spawn threads
for i in range(args.threads):
    print"Spawning thread: %d" % i
    thread =  t.Thread(target=test_remote)
    thread.start()
