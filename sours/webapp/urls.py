from django.urls import path
from django.views.generic import RedirectView
from webapp.views.project_views import ProjectUpdateView, ProjectDeleteView, ProjectCreateView,\
    ProjectView, IndexView
from webapp.views.review_views import ReviewCreateView, ReviewDeleteView, ReviewUpdateView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('projects/', RedirectView.as_view(pattern_name='webapp:index')),
    path('projects/add/', ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/', ProjectView.as_view(), name='project_view'),
    path('projects/<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update_view'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete_view'),
    path('project/<int:pk>/review/add/', ReviewCreateView.as_view(), name='review_add'),
    path('comment/<int:pk>/update/', ReviewUpdateView.as_view(), name='review_update_view'),
    path('comment/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete_view')
    # path('test/', TestView.as_view(), name='test')
]
