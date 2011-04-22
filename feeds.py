from django.contrib.syndication.views import Feed


class LatestEntriesFeed(Feed):
    title = "feed accumulator"
    link = "/news/"
    description = "Newsfeed Accumulator for GP|Bln"

    def items(self):
        return NewsItem.objects.order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

