# cbf is meant to brute force directories and file locations for
#content managers
#all you do is point it to the content managers directory
#crawler for content managers
import urllib
import urllib2
import threading
import Queue as Q
import argparse as agp

print "==================================================================="
print "[*] CREATED  BY HYBRID-BABY powered by BINARYLABSKE.CO.KE [*!...]"
print "==================================================================="
print "    "
print "===================================="
print "[*]  DIRECTORY LISTER [*!...]"
print "===================================="

#get targets and url plus worlists as os arguments
parser = agp.ArgumentParser(description="Directory Brute forcer")
parser.add_argument("target",help="targets url")
parser.add_argument("wordlist",help="Directory to wordlist file")
parser.add_argument("threads",help="Number of threads to use",type=int)
argp = parser.parse_args()


resume = None
user_agent = "User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"

def build_wordlist(wordlist_file):
    fd = open(wordlist_file,"rb")
    raw_words = fd.readlines()
    fd.close()
    #with open(wordlist_file,"rb") as fd:
        #raw_words = fd.readlines() #list(fd)

    found_resume = False
    words =Q.Queue()
    for word in raw_words:
        word = word.rstrip()
        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print "Resulting wordlist from:%s"%resume
        else:
            words.put(word)

    return words

def dir_bruter(word_queue,extension=None):
    while not word_queue.empty():
        attempt = word_queue.get()
        attemp_list = []
        #check for file extension if 0, brute dir
        if "." not in attempt:
            attemp_list.append("/%s/" % attempt)
        else:
            attemp_list.append("/%s" % attempt)

        #brute force extencion
        if extensions:
            for extension in extensions:
                attemp_list.append("/%s%s" % (attempt,extension))

        for brute in attemp_list:
            url = "%s%s" % (argp.target,urllib.quote(brute))
            try:
                headers = {}
                headers["User-Agent"] = user_agent
                p = urllib2.Request(url,headers=headers)
                response = urllib2.urlopen(p)
                if len(response.read()):
                    print "[%d] => %s" % (response.code,url)

            except urllib2.URLError,e:
                if hasattr(e, 'code') and e.code != 404:
                    print "!!!! %d => %s" % (e.code,url)

                pass

word_queue = build_wordlist(argp.wordlist)
extensions = [".php",".bak",".orig",".inc",".html",".js"]
for i in range(argp.threads):
    t = threading.Thread(target=dir_bruter,args=(word_queue,extensions,))
    t.start()

#usage
#python cbf.py https://target.com/  wordlist/directory/path  no_of_threads
