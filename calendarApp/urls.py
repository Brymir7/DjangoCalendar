from django.urls import path
from . import views
from .views import NoteCreate, NoteUpdate, NoteDelete
urlpatterns = [
    path('', views.index, name='index'),
    path('note/create/<int:day_id>/', NoteCreate.as_view(), name='note-create'),
    path('note-update/<int:pk>/', NoteUpdate.as_view(), name = 'note-update'),
    path('note/delete/<int:pk>/', NoteDelete.as_view(), name='note-delete'),

]