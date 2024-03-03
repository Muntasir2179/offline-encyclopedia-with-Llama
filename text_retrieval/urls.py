from django.urls import path
from text_retrieval import views

urlpatterns = [
    path('', view=views.index, name='index'),
    path('login/', view=views.login_function, name='login'),
    path('signup/', view=views.signup_function, name='signup'),
    path('logout/', view=views.logout_function, name='logout'),
    path('upload/', view=views.upload, name='upload'),
    path('upload/chat', view=views.chat, name='chat')
]
