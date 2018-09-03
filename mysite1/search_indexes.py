from haystack import indexes
from mysite1.models import Anime

# 修改此处，类名为模型类的名称+Index，比如模型类为GoodsInfo,则这里类名为GoodsInfoIndex
class AnimeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Anime

    def index_queryset(self, using=None):
        return self.get_model().objects.all()