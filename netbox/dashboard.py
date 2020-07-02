"""
This file was generated with the customdashboard management command, it
contains the two classes for the main dashboard and app index dashboard.
You can customize these classes as you want.

To activate your index dashboard add the following to your settings.py::
    ADMIN_TOOLS_INDEX_DASHBOARD = 'networked-toolbox.dashboard.CustomIndexDashboard'

And to activate the app index dashboard::
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'networked-toolbox.dashboard.CustomAppIndexDashboard'
"""

from django.utils.translation import ugettext_lazy as _
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for networked-toolbox.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        
        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'), 5,  draggable=False, deletable=False, layout='stacked',))

        # will list all apps except the django.contrib ones
       
        self.children.append(modules.ModelList(
            title='Events And Workshops',
            models=('events_workshops.*',), 
            draggable=False,
            deletable=False,
            
        ))
        self.children.append(modules.ModelList(
            _('Overview Pages'),
            models=[
                'tools.models.ToolOverviewPage',
                'tools.models.CategoryOverviewPage',
                'tools.models.CategoryGroupOverviewPage',
                'tools.models.StoryOverviewPage',
            ], 
            draggable=False,
            deletable=False,
        ))
        self.children.append(modules.ModelList(
            _('Pages and Textblocks'),
            models=[
                'pages.models.Page',
                'menus.models.MenuItem', 
                'pages.models.FlashTextNew', 
                'pages.models.FooterTextblock', 
                'pages.models.SearchBarInfotext',
            ], 
            draggable=False,
            deletable=False,
        ))
        self.children.append(modules.ModelList(
            _('Library'),
            models=[
                'filer.models.foldermodels.Folder', 
                'library.models.Video',
                'library.models.DocumentCategory',
                'library.models.LibraryDocument', 
                'library.models.VideoResource', 
                'library.models.OnlineCourse',

            ], 
            draggable=True,
            deletable=False,
        ))
        self.children.append(modules.ModelList(
            _('Interactions'),
            models=[
                'user_notifications.*',
                'comments.*', 
                'feedback.*',
         
            ], 
            draggable=False,
            deletable=False,
        ))
        self.children.append(modules.ModelList(
            _('People'),
            models=[
                'allauth.account.models.EmailAddress', 
                'profiles.models.Profile', 
                'tools.models.ToolFollower', 
                'tools.models.ToolUser', 
                'tools.models.CategoryGroupFollower', 


            ],
            draggable=False,
            deletable=False,
        ))
        self.children.append(modules.ModelList(
            _('Main Content'),
            models=[
                'tools.*',
                'resources.models.ToolResource', 
                'django_summernote.*', 
            ], 
            exclude=[
                
                    'tools.models.ToolOverviewPage',
                    'tools.models.CategoryOverviewPage',
                    'tools.models.CategoryGroupOverviewPage',
                    'tools.models.StoryOverviewPage',
                    'tools.models.ToolFollower',
                    'tools.models.ToolUser',
                    'tools.models.CategoryGroupFollower',
                
            ],
            draggable=False,
            deletable=False,
        ))

        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('Authentication and Authorization'),
            models=('django.contrib.*',),
            exclude=('django.contrib.sites.*',), 
            draggable=False,
            deletable=False,
            
        ))



class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for networked-toolbox.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
