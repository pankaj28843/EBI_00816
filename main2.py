import collections

# Define a namedtuple class to store Author
Author = collections.namedtuple('Author', ['LastName', 'ForeName', 'Initials'])


class Article(object):
    def __init__(self, title, authors):
        self.title = title
        self.authors = authors

    @staticmethod
    def initialize_from_lxml_etree(element):
        raise NotImplementedError


class CoAuthorshipDataStore(object):
    def __init__(self):
        # Create a dictionary of dictionary to store co-author relationship
        # Using set for list of article in a co-author relation to avoid duplication
        self.store = collections.defaultdict(lambda: collections.defaultdict(set))

    def addArticle(self, article):
        # Iterate twice to store coauthorship relation
        for author_1 in article.authors:
            for author_2 in article.authors:
                self.store[author_1][author_2].add(article.title)

    def getAllAuthors(self):
        return sorted(self.store.keys(), key=lambda x: x.LastName)

    def getCoAuthorshipCount(self, author_1, author_2):
        return len(self.store[author_1][author_2])
