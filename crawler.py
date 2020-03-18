#$crawler is a site crawler to help one familiarise with the target
#this is useful when one has a target with limited time to identify services adn directories
#crawler basically gets thje sites various links to help you identify attacking or injection parameters
#say you are in a remote target with no access to your machine.. git clone.. last time i checked most companies haven't blocked github
#this script is open source and liable for advancement by anyone.. just FORK_IT
#crawl the web index pages and save the details

import re
import requests
import argparse as argp
from urllib.parse import urlparse

print( "===================================================================")
print( "[*] CREATED  BY HYBRID-BABY powered by BINARYLABSKE.CO.KE [*!...]")
print( "===================================================================")
print( "    ")
print( "=============================")
print( "[*]  WEBSITE CRWALER [*!...]")
print( "=============================")

#get taget
parser = argp.ArgumentParser(description="Website Crawler")
parser.add_argument("target",help="set targets url")
args = parser.parse_args()

#store all crawling functions in a class
class Crawler(object):
    def __init__(self,starting_url):
        self.starting_url = starting_url
        self.visited = set()

    #get the html
    def getHtml(self,url):
        try:
            html = requests.get(url)
        except Exception as e:
            print(e)
            return""
        return html.content.decode('latin-1')

    #get the links
    def getLinks(self,url):
        html = self.getHtml(url)
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''',html)
        for i, link in enumerate(links):
            if not urlparse(link).netloc:
                link_with_base = base + link
                links[i] = link_with_base
        return set(filter(lambda x: 'mailto' not in x,links))


    #extract info
    def extractInfo(self,url):
        html = self.getHtml(url)
        meta = re.findall("<meta .*?name=[\"'](.*?)['\"].*?content=[\"'](.*?)['\"'].*?>",html)
        return dict(meta)

    def crawl(self,url):
        for link in self.getLinks(url):
            if link in self.visited:
                continue
            self.visited.add(link)
            info = self.extractInfo(link)
            print(f"""Link:{link}
                Description: {info.get('description')}
                Keywords: {info.get('keywords')}""")
            self.crawl(link)


    def start(self):
        self.crawl(self.starting_url)


def main():
    crawler = Crawler(args.target)
    crawler.start()

main()
