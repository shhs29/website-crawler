import networkx as nx
import urllib3
from urllib.parse import urlparse, urljoin
from random import randint
from time import sleep
from bs4 import BeautifulSoup


def crawl_engine(root_url: str):
    # list of extensions to ignore from crawler
    extensions = ['.jpg', '.jpeg', '.png', '.pdf', '.svg']
    # create a connection pool to handle requests
    http = urllib3.PoolManager()
    # initialise next_to_visit list that behaves as a queue used to traverse graphs in BFS
    next_to_visit = []
    # initialise discovered variable as a set to store unique urls that have been discovered so far
    discovered = set()
    # initialise visited list that stores the urls that have been traversed. This is purely to understand which nodes
    # have already been traversed and the order of the traversal
    visited = []
    # add root url to next_to_visit
    next_to_visit.append(root_url)
    # add root url to discovered
    discovered.add(root_url)
    # initialise networkx directed graph to store nodes and edges
    graph = nx.DiGraph()
    # repeat the loop till the contents of the queue are empty
    while len(next_to_visit) != 0:

        current_url = next_to_visit.pop(0)
        graph.add_node(current_url, label=current_url)
        visited.append(current_url)
        # encompass code in try-catch blocks to avoid interruptions to crawler due to exceptions
        try:
            # sleep command for an interval of 1s or 2s to ensure inconsistent delay in hitting the urls and
            # avoid blocking of requests
            sleep(randint(1, 2))
            # api to make http request to given url
            webpage = http.request('GET', current_url)
            # use BeautifulSoup library to parse webpage data
            soup = BeautifulSoup(webpage.data, "html.parser")
            # extract all the urls inside <a> tags
            for url in soup.find_all('a'):
                link = url.get('href')
                # condition to check if link is not an image or a pdf
                if link != None and not (any(link.endswith(ext) for ext in extensions)):
                    # extract domain name from link
                    domain_name = urlparse(link).netloc
                    # condition to check if domain is right
                    if "ontariotechu.ca" in domain_name or "uoit.ca" in domain_name:
                        # add edge to graph
                        graph.add_edge(current_url, link)
                        # if the link has already been discovered, move to the next one
                        if link in discovered:
                            continue
                        # add link to next-to-visit and discovered
                        next_to_visit.append(link)
                        discovered.add(link)
                    # check if url is a relative url
                    elif link.startswith('/'):
                        # join current url with relative url to get complete url
                        link = urljoin(current_url, link)
                        # add edge to graph
                        graph.add_edge(current_url, link)
                        # if the link has already been discovered, move to the next one
                        if link in discovered:
                            continue
                        # add link to next-to-visit and discovered
                        next_to_visit.append(link)
                        discovered.add(link)
                    # write every 2000 discovered nodes to an output file to avoid loss of information in case the
                    # system crashes
                    if len(discovered) % 2000 == 0:
                        path_to_file = f'university-network-{len(discovered)}.gexf'
                        # write the graph to output file in gexf format
                        nx.write_gexf(graph, path_to_file)
            print(f'Number of nodes discovered {len(discovered)}')
            print(f'Number of nodes visited {len(visited)}')
        # catch any exception during BFS, print and then continue to next url. All exceptions are handled by ignoring
        # the problem link
        except Exception as e:
            print(e)
            continue
    # write all nodes till end of parsing to output file
    path_to_file = f'university-network-final.gexf'
    nx.write_gexf(graph, path_to_file)
    print(f'Number of nodes in information network {len(visited)}')


if __name__ == '__main__':
    # crawl all ontario tech webpages
    crawl_engine(root_url="https://ontariotechu.ca/")
