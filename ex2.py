# Osher Elhadad 318969748 Gili Gutfeld 209284512

import math
import random
import sys


def myData():
    mini_web = [
        {
            'URL': 'mammals.com',
            'tokens': ['jaguar', 'mammal', 'dog', 'cat', 'penguin', 'lion', 'bear', 'dolphin'],
            'linksTo': ['animals.com']
        },
        {
            'URL': 'animals.com',
            'tokens': ['jaguar', 'cute', 'big', 'cat', 'jaguar', 'my', 'favorite', 'dolphin'],
            'linksTo': []
        },
        {
            'URL': 'cats.com',
            'tokens': ['my', 'cat', 'big'],
            'linksTo': ['mammals.com', 'animals.com']
        },
        {
            'URL': 'dogs.com',
            'tokens': ['dog', 'puppy', 'cute', 'big', 'loyal'],
            'linksTo': ['mammals.com']
        },
        {
            'URL': 'pets.com',
            'tokens': ['cat', 'dog', 'pets', 'cute', 'animals'],
            'linksTo': ['cats.com', 'dogs.com', 'mammals.com']
        },
        {
            'URL': 'zoos.com',
            'tokens': ['lion', 'tiger', 'elephant', 'zoo', 'animals'],
            'linksTo': ['mammals.com', 'animals.com']
        },
        {
            'URL': 'wildlife.com',
            'tokens': ['lion', 'tiger', 'bear', 'wildlife', 'safari'],
            'linksTo': ['mammals.com', 'zoos.com', 'animals.com']
        },
        {
            'URL': 'birding.com',
            'tokens': ['bird', 'eagle', 'sparrow', 'falcon', 'birding'],
            'linksTo': ['animals.com']
        },
        {
            'URL': 'reptiles.com',
            'tokens': ['snake', 'lizard', 'turtle', 'reptiles'],
            'linksTo': ['animals.com']
        },
        {
            'URL': 'aqua.com',
            'tokens': ['shark', 'dolphin', 'whale', 'aquatic', 'life'],
            'linksTo': ['mammals.com', 'animals.com']
        }
    ]
    return mini_web


def mySearchString():
    search_string = ['cat', 'mammal', 'animals', 'cute', 'big']
    return search_string


def invertedIndex(data, search_string):
    # create an empty dictionary for the inverted index
    inverted_index = {}

    # iterate each token in the search string, add it and initialize its value to an empty list
    for token in search_string:
        if token not in inverted_index:
            inverted_index[token] = []

    # iterate each website in the mini web
    for web in data:
        # get the url and the tokens for the website
        url = web['URL']
        tokens = web['tokens']

        # iterate each token in the search string
        for token in search_string:
            # calculate the tf of the token, the idf of the token and the tf-idf score of the token in the website
            tf = tokens.count(token) / len(tokens)
            websites_with_token = [web for web in data if token in web['tokens']]
            idf = math.log(len(data) / len(websites_with_token))
            tf_idf = tf * idf

            # if the tf-idf score is positive, add the url and tf-idf score to the inverted index
            if tf_idf > 0:
                inverted_index[token].append([url, tf_idf])

    # sort the lists in the inverted index by descending tf-idf score
    for key in inverted_index:
        inverted_index[key] = sorted(inverted_index[key], key=lambda a: a[1], reverse=True)

    return inverted_index


'''
    The PageRank algorithm takes into account the number and quality of links pointing to a website, as well as
    the PageRank of the websites that those links point to, in order to determine the importance of the website.
    In our example, the website with the highest PageRank is animals.com, which match my intuition on
    what is the "most important" website, because almost all the websites has links to it. Then, we have mammals.com
    which may be the second "most important" website because almost all the animals are mammals and actually
    have links to it, and also mammals.com has link to animals.com and it make sense because we got that animals.com
    is more important. The other websites have significantly lower PageRank as we expected.
'''


def pageRankSimulation(data, numIter, beta):

    # create a dictionary for the PageRank of each website
    page_rank = {}
    for web in data:
        url = web['URL']
        page_rank[url] = 1 / len(data)

    # בhoose a random link from our data
    current_url = random.choice(list(page_rank.keys()))

    # iterate for the number of steps we got
    for i in range(numIter):

        # choose a random website and follow links randomly with probability beta and get the links of it
        links = [web for web in data if web['URL'] == current_url][0]['linksTo']

        # in probability of beta choose a random link to follow from the current website, if it exists
        if random.uniform(0, 1) < beta and links:
            current_url = random.choice(links)
        else:
            current_url = random.choice(list(page_rank.keys()))

        # update the PageRank of the current website
        page_rank[current_url] += 1

    # sort the PageRank results by descending score
    page_rank_list = [[page, rank / numIter] for page, rank in page_rank.items()]
    page_rank_list.sort(key=lambda a: a[1], reverse=True)
    return page_rank_list


def score(tfIdf, pageRankValue):
    
    # Root sum square
    return math.sqrt(math.pow(tfIdf, 2) + math.pow(pageRankValue, 2))


def getFilledInvertedIndex(invertedIndex, pages):

    # Fill missing pages in indexes, every index has rank of all pages
    for index, pagesScores in invertedIndex.items():
        for page in pages:
            pagesInIndex = [pageWithRank[0] for pageWithRank in pagesScores]
            if page not in pagesInIndex:
                invertedIndex[index].append([page, 0])
    return invertedIndex


def getMapForRandomAccess(invertedIndex, pageRank):
    pageToScoresMap = dict()
    column = 0

    # Creates a map for random access. From page to it's all ranks in all columns
    for urlWithRank in pageRank:
        pageToScoresMap[urlWithRank[0]] = [0 for _ in range(len(invertedIndex) + 1)]
        pageToScoresMap[urlWithRank[0]][column] = urlWithRank[1]
    column += 1
    for pagesScores in invertedIndex.values():
        for urlWithRank in pagesScores:
            if urlWithRank[0] in pageToScoresMap.keys():
                pageToScoresMap[urlWithRank[0]][column] = urlWithRank[1]
        column += 1
    return pageToScoresMap


def getTop1(threshold, scores):
    maxPage = None
    maxScore = 0

    # Get the page with max score, if above the threshold then retun it and it's score, else return None and -1.
    # Because of TA algorithm- we stop and return top 1 only after there is at least 1 page with score>=threshold.
    for page, pageScore in scores.items():
        if pageScore > maxScore:
            maxPage = page
            maxScore = pageScore
    if maxScore >= threshold:
        return maxPage, maxScore
    return None, -1


def top1(invertedIndex, pageRank):
    pages = [urlWithRank[0] for urlWithRank in pageRank]

    # Fill missing pages in indexes, every index has rank of all pages
    invertedIndex = getFilledInvertedIndex(invertedIndex, pages)

    # Creates a map for random access. From page to it's all ranks in all columns
    pageToScoresMapForRandomAccess = getMapForRandomAccess(invertedIndex, pageRank)

    threshold = sys.maxsize
    indexesForSortedAccess = [0 for _ in range(len(invertedIndex) + 1)]

    # For calculate and update the threshold
    minRanks = [sys.maxsize for _ in range(len(invertedIndex) + 1)]

    # map of page and it's score (-1 if doesn't have)
    scores = dict()
    for page in pages:
        scores[page] = -1

    column = 0
    canCalcThreshold = False
    while True:
        
        # PageRank is column 0
        if column == 0:
            page = pageRank[indexesForSortedAccess[column]][0]
            pageRankScore = pageRank[indexesForSortedAccess[column]][1]
            minRanks[column] = pageRankScore
            print('Sorted access to ' + page + ' at the PageRank index')
            if scores[page] == -1:
                tfIdf = 0
                for index in range(len(indexesForSortedAccess)):
                    if index != column:
                        tfIdf += pageToScoresMapForRandomAccess[page][index]
                        print('Random access to ' + page + ' at the invertedIndex ' + list(invertedIndex.keys())[index - 1])
                scores[page] = score(tfIdf, pageRankScore)

        # invertedIndex is columns 1 and more
        else:
            page = invertedIndex[list(invertedIndex.keys())[column - 1]][indexesForSortedAccess[column]][0]
            invertedIndexScore = invertedIndex[list(invertedIndex.keys())[column - 1]][indexesForSortedAccess[column]][1]
            minRanks[column] = invertedIndexScore
            print('Sorted access to ' + page + ' at the invertedIndex ' + list(invertedIndex.keys())[column - 1])
            if scores[page] == -1:
                tfIdf = invertedIndexScore
                pageRankScore = 0
                for index in range(len(indexesForSortedAccess)):
                    if index != column:
                        if index == 0:
                            pageRankScore = pageToScoresMapForRandomAccess[page][index]
                            print('Random access to ' + page + ' at the PageRank index')
                        else:
                            tfIdf += pageToScoresMapForRandomAccess[page][index]
                            print('Random access to ' + page + ' at the invertedIndex ' + list(invertedIndex.keys())[index - 1])
                scores[page] = score(tfIdf, pageRankScore)

        # Check if we went over the all columns at least ones
        if not canCalcThreshold:
            canCalcThreshold = True
            for rank in minRanks:
                if rank == sys.maxsize:
                    canCalcThreshold = False
                    break

        # Calculate threshold
        if canCalcThreshold:
            pageRankScore = minRanks[0]
            tfIdf = 0
            for i in range(len(minRanks)):
                if i != 0:
                    tfIdf += minRanks[i]
            threshold = score(tfIdf, pageRankScore)

        indexesForSortedAccess[column] += 1

        # Round Robin over the columns
        column = (column + 1) % len(indexesForSortedAccess)

        topPage, topScore = getTop1(threshold, scores)
        if topPage is not None:
            return topPage, topScore


if __name__ == '__main__':
    invertedIndexOutput = invertedIndex(myData(), mySearchString())
    pageRankSimulationOutput = pageRankSimulation(myData(), 100000, 0.8)
    print(invertedIndexOutput)
    print(pageRankSimulationOutput)
    top1Page, top1Score = top1(invertedIndexOutput, pageRankSimulationOutput)
    print("Top 1 page- " + top1Page + ' with score- ' + str(top1Score))
