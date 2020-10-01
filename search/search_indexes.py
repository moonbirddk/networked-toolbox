from haystack import indexes
from tools.models import Tool, Story, ToolCategory
from profiles.models import Profile


class ToolIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Tool

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(published=True)


class ToolCategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ToolCategory

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(published=True)


class StoryIndex(indexes.SearchIndex, indexes.Indexable):
    """
        Search in:
         * user first + last name
         * story title
         * story content
         * story country (full country name)
    """
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Story

    def index_queryset(self, using=None):
        return self.get_model().objects.filter()


class ProfileIndex(indexes.SearchIndex, indexes.Indexable):
    """
        Search in:
         * user first+ last name
         * profile bio
         * profile country (full country name)
    """
    text = indexes.CharField(document=True, use_template=True)
    bio = indexes.CharField(model_attr="bio")
   # uuid = indexes.CharField(model_attr='uuid')
    
    def get_model(self):
        return Profile

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            user__is_active=True,
            user__is_superuser=False,
        )
