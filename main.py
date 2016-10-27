import collections
import os
import sys

from lxml import objectify

# Find out the directory containing this file
HERE = os.path.dirname(__file__)

# Read the xml file and create object tree using lxml.objectify
with open(os.path.join(HERE, 'data.xml'), 'r') as f:
    root = objectify.fromstring(f.read())

# Define a namedtuple class to store Author
Author = collections.namedtuple('Author', ['LastName', 'ForeName', 'Initials'])

# Create a dictionary of dictionary to store co-author relationship
# Using set for list of article in a co-author relation to avoid duplication
coauthorship_data = collections.defaultdict(lambda : collections.defaultdict(set))

# Iterate over all the articles in the XML
for article_dict in root[0].getchildren():
    # Get the tite of the article
    article_title = article_dict['ArticleTitle']

    # Create a list of Author objects for this article
    authors_list = []
    for author_dict in article_dict['AuthorList'].getchildren():
        # Create instance of Author class
        author = Author(
            author_dict['LastName'],
            author_dict['ForeName'],
            author_dict['Initials'],
        )
        # Append to the list of authors
        authors_list.append(author)

    # Iterate twice to store coauthorship relation
    for author_1 in authors_list:
        for author_2 in authors_list:
            coauthorship_data[author_1][author_2].add(article_title)

# Get sorted list of all the authors across all articles
all_authors_list = sorted(coauthorship_data.keys(), key=lambda x: x.LastName)

# Print the matrix to stdout
sys.stdout.write('\t\t')
for author in all_authors_list:
    sys.stdout.write('%s %s\t' % (author.LastName, author.ForeName))
sys.stdout.write('\n')
for author_1 in all_authors_list:
    sys.stdout.write('%s %s\t' % (author_1.LastName, author_1.ForeName))
    for author_2 in all_authors_list:
        sys.stdout.write('%d\t\t' % len(coauthorship_data[author_1][author_2]))
    sys.stdout.write('\n')
