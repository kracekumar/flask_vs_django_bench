from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

from hello.views import index

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_app.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
                       url('^index/$', index),
    # url(r'^admin/', include(admin.site.urls)),
)
