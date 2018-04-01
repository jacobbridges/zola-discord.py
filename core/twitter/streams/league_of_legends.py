from peony import EventStream, PeonyClient, event_handler, events
from peony.oauth_dance import oauth_dance


# all the event handlers are included in peony.events
class Client(PeonyClient):
    pass


# every class inheriting from `PeonyClient` or `BasePeonyClient` has
# an event_stream function that can be used on an `EventStream`
@Client.event_stream
class UserStream(EventStream):

    def stream_request(self):
        """
        The stream_request method returns the request
        that will be used by the stream
        """
        # return self.userstream.user.get()
        return self._client.stream_request(
            method='POST',
            url='https://stream.twitter.com/1.1/statuses/filter.json?track=twitter',
        )

    # the on_connect event is triggered on connection to an user stream
    # https://dev.twitter.com/streaming/overview/messages-types#friends-lists-friends
    @events.on_connect.handler
    def connection(self, data):
        print("Connected to stream!")

    # the on_tweet event is triggered when a tweet seems to be sent on
    # the stream, by default retweets are included
    @events.on_tweet.handler
    def tweet(self, data):
        print(data.text)

    # the on_retweet event is triggered when a retweet is in the user's
    # stream.
    # the on_tweet event won't be triggered by retweets if there
    # is an handler for the on_retweet event.
    # @events.on_retweet.handler
    # def retweet(self, data):
    #     pass

    # the on_follow event is triggered when the user gets a new follower
    # or the user follows someone
    # https://dev.twitter.com/streaming/overview/messages-types#events-event
    @events.on_follow.handler
    def follow(self, data):
        print("You have a new follower @%s" % data.source.screen_name)

    # the default event is the last event to be triggered
    # if no other event was triggered by the data then this one will be
    @events.default.handler
    def default(self, data):
        print(data)


if __name__ == '__main__':
    tokens = oauth_dance('DmSCessQ6xY75WL0VBaSSrQ5E', 'ronZsrZzd23bMXkg52gUQb2zEr0LLLDeUgSYLT6JjqZ3XnJVVY')
    client = Client(**tokens)
    client.run()
