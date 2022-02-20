from urllib.parse import urlparse, urljoin
import networkx as nx
from random import randint
from time import sleep

import urllib3
from bs4 import BeautifulSoup


# def find_metrics(G):
#     pass


def crawler(root_url: str):
    # list of extensions to ignore from crawler
    extensions = ['jpg', 'jpeg', 'pdf', 'svg']
    file = 1
    http = urllib3.PoolManager()
    next_to_visit = []
    visited = set()
    traversal_order = []
    next_to_visit.append(root_url)
    visited.add(root_url)
    graph = nx.DiGraph()
    while len(next_to_visit) != 0:
        current_url = next_to_visit.pop(0)
        graph.add_node(current_url, label=current_url)
        traversal_order.append(current_url)
        try:
            sleep(randint(1, 5))
            webpage = http.request('GET', current_url)
        except Exception as e:
            print(e)
            continue
        soup = BeautifulSoup(webpage.data, "html.parser")
        # print(soup.head.title)
        for url in soup.find_all('a'):
            link = url.get('href')
            # condition to check if link is not an image or a pdf
            if link != None and not (any(link.endswith(ext) for ext in extensions)):
                # extract domain name from link
                domain_name = urlparse(link).netloc
                # condition to check if domain is right
                if "ontariotechu.ca" in domain_name or "uoit.ca" in domain_name:
                    if link in visited:
                        continue
                    next_to_visit.append(link)
                    visited.add(link)
                    graph.add_edge(current_url, link)
                elif link.startswith('/'):
                    link = urljoin(current_url, link)
                    if link in visited:
                        continue
                    next_to_visit.append(link)
                    visited.add(link)
                    graph.add_edge(current_url, link)
        if len(traversal_order) % 5000 == 0:
            path_to_file = f'university-network{file}.gexf'
            nx.write_gexf(graph, path_to_file)
            print(*traversal_order, sep='\n')
            file += 1
    # find the metrics of the graph derived from the crawler
    # find_metrics(graph)


if __name__ == '__main__':
    # crawl all ontario tech webpages
    crawler(root_url="https://ontariotechu.ca/")
