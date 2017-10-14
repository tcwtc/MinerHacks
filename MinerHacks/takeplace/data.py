# Use news API to extract news, then stores news data
# using Mongodb
from __future__ import print_function
from eventregistry import *
import collections
import pymongo
import datetime



class NewsQuery(object):

    def __init__(self):
        # 22d2e6f355774376a927b3735ec0b039
        self.er = EventRegistry(apiKey='9aa996a4-029c-4cc6-88dc-bd7cd42a8bf7')
        startdate = datetime.datetime.now() - datetime.timedelta(days=15)
        self.dateStart = datetime.date(startdate.year, startdate.month, startdate.day)
        # self.dateStart = datetime.date(2017, 10, 1)
        self.client = pymongo.MongoClient('localhost', 27017)
        self.newsdata = self.client['newsdata']

    def event_query(self, location):
        q = QueryEventsIter(
            # conceptUri = er.getConceptUri("George Clooney"),
            # dateStart=datetime.date(2017, 9, 20), dateEnd=datetime.date(2017, 10, 13),
            dateStart=self.dateStart,
            # sourceUri=self.er.getNewsSourceUri("New York Times"),
            sourceUri=QueryItems.OR([self.er.getNewsSourceUri("New York Times"), self.er.getNewsSourceUri("bbc")])
            # locationUri= self.er.getLocationUri(location),
            # locationUri = QueryItems.OR([er.getLocationUri("United States"), er.getLocationUri("Los Angeles")]),
        )

        q.setRequestedResult(RequestEventsInfo(count=3,
                                               returnInfo=ReturnInfo(
                                               eventInfo=EventInfoFlags(title=True, concepts=True, categories=True,
                                                                            location=True, stories=True, date=True,
                                                                            socialScore=True))))

        client = pymongo.MongoClient('localhost', 27017)
        newsdata = client['newsdata']
        event_tab = newsdata['event_tab']

        res = []

        for event in q.execQuery(self.er, sortBy="date", maxItems=10):
            print(event)
            # new_event = { your_key: event[your_key] for your_key in newkeys }
            # new_event['location'] = query_location
            if event['location'] is not None:
            # if (event['location']['country']['label']['eng'] is not None) and (event['location']['label']['eng'] is not None):

                new_event = collections.defaultdict(str)
                new_event['country'] = event['location']['country']['label']['eng']
                new_event['city'] = event['location']['label']['eng']
                new_event['title'] = event['title']['eng']
                new_event['summary'] = event['summary']['eng']
                new_event['eventDate'] = event['eventDate']
                new_event['id'] = event['id']
                new_event['uri'] = event['uri']
                event_tab.insert_one(new_event)
                res.append(new_event)

        return res

    # def event_feed(self):
    #     recentQ = GetRecentEvents(mandatoryLang='eng', mandatoryLocation=True)
    #     starttime = time.time()
    #
    #
    #     event_tab = self.newsdata['event_tab']
    #
    #     while True:
    #         ret = recentQ.getUpdates()
    #         if "eventInfo" in ret and isinstance(ret["eventInfo"], dict):
    #             print("==========\n%d events updated since last call" % len(ret["eventInfo"]))
    #
    #             # get the list of event URIs, sorted from the most recently changed backwards
    #             activity = ret["activity"]
    #             # for each updated event print the URI and the title
    #             # NOTE: the same event can appear multiple times in the activity array - this means that more than one article
    #             # about it was recently written about it
    #             for eventUri in activity:
    #                 event = ret["eventInfo"][eventUri]
    #                 print("Event %s ('%s') was changed" % (
    #                 eventUri, event["title"][list(event["title"].keys())[0]].encode("ascii", "ignore")))
    #                 # event["concepts"] contains the list of relevant concepts for the event
    #                 # event["categories"] contains the list of categories for the event
    #                 # new_event = collections.defaultdict(str)
    #                 new_event = {}
    #                 print("***", event)
    #                 new_event['country'] = event['location']['country']['label']['eng']
    #                 new_event['city'] = event['location']['label']['eng']
    #                 new_event['title'] = event['title']['eng']
    #                 new_event['summary'] = event['event']['eng']
    #                 new_event['eventDate'] = event['eventDate']
    #                 new_event['id'] = event['id']
    #                 new_event['uri'] = event['uri']
    #                 event_tab.insert_one(new_event)
    #                 #
    #                 # TODO: here you can do the processing that decides if the event is relevant for you or not. if relevant, send the info to an external service
    #
    #         # wait exactly a minute until next batch of new content is ready
    #         print("sleeping for 60 seconds...")
    #         time.sleep(60.0 - ((time.time() - starttime) % 60.0))
    #
    #
    # def article_query(self, target_event):
    #
    #     article_tab = self.newsdata['article_tab']
    #
    #     q = QueryArticles(
    #         locationUri = QueryItems.OR([self.er.getLocationUri(target_event['country']), self.er.getLocationUri(target_event['city'])]),
    #         lang = 'eng',
    #         dateStart=self.dateStart,
    #         isDuplicateFilter='skipDuplicates',
    #         hasDuplicateFilter='skipHasDuplicates',
    #         eventFilter='skipArticlesWithoutEvent',
    #         # dateStart=datetime.date(2016, 3, 22), dateEnd=datetime.date(2016, 3, 23),
    #         # conceptUri=self.er.getConceptUri("Brussels"),
    #         # sourceUri=self.er.getNewsSourceUri("New York Times")
    #         )
    #     # return details about the articles, including the concepts, categories, location and image
    #     q.setRequestedResult(RequestArticlesInfo(count=5,
    #                                              returnInfo=ReturnInfo(
    #                                              articleInfo=ArticleInfoFlags(concepts=True,
    #                                                                           categories=True,
    #                                                                           location=True,
    #                                                                           eventUri=True,
    #                                                                           url=True,
    #                                                                           basicInfo=True,
    #                                                                            ))))
    #     # execute the query
    #     arts = self.er.execQuery(q)
    #     new_art = collections.defaultdict(str)
    #     for art in arts['articles']['results']:
    #
    #     # new_event['country'] = art['location']['country']['label']['eng']
    #     # new_event['city'] = art['location']['label']['eng']
    #     # new_event['title'] = art['title']['eng']
    #     # new_event['summary'] = event['event']['eng']
    #     # new_event['eventDate'] = event['eventDate']
    #     # new_event['id'] = event['id']
    #     # new_event['uri'] = event['uri']
    #         article_tab.insert_one(new_art)
    #
    #     return arts
    # for item in sheet_tab.find():
    # print(item)
    # def article_query_2(self, location):
    #     q = QueryArticlesIter(
    #         # conceptUri = er.getConceptUri("George Clooney"),
    #         dateStart=self.dateStart,
    #         sourceUri=self.er.getNewsSourceUri("New York Times"),
    #         locationUri= self.er.getLocationUri(location),
    #         # locationUri = QueryItems.OR([er.getLocationUri("United States"), er.getLocationUri("Los Angeles")]),
    #     )
    #
    #     q.setRequestedResult(RequestArticlesInfo(count=3,
    #                                            returnInfo=ReturnInfo(
    #                                            articleInfo=ArticleInfoFlags(title=True, concepts=True,
    #                                                                         categories=True,
    #                                                                         location=True,
    #                                                                         socialScore=True))))
    #
    #     # client = pymongo.MongoClient('localhost', 27017)
    #     # newsdata = client['newsdata']
    #     article_tab = self.newsdata['article_tab']
    #
    #     # newkeys = ['location', 'uri', 'date', 'title', 'body']
    #
    #     for art in q.execQuery(self.er, sortBy="date", maxItems=3):
    #         print(art)
    #         # new_event = { your_key: event[your_key] for your_key in newkeys }
    #         # new_event['location'] = query_location
    #
    #         new_event = collections.defaultdict(str)
    #         # new_event['country'] = event['location']['country']['label']['eng']
    #         # new_event['city'] = event['location']['label']['eng']
    #         # new_event['title'] = event['title']['eng']
    #         # new_event['summary'] = event['event']['eng']
    #         # new_event['eventDate'] = event['eventDate']
    #         # new_event['id'] = event['id']
    #         # new_event['uri'] = event['uri']
    #         article_tab.insert_one(new_event)


if __name__ == "__main__":
    # target_event = {'country':'United States', 'city': 'New York', 'uri': 'deu-783116'}
    # art = NewsQuery().article_query(target_event)
    event = NewsQuery().event_query(None)
    print(event)





