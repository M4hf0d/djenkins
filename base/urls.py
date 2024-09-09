from django.urls import path,include
from .views import *


urlpatterns = [

   # path('', index, name = 'index'),
   path('', homepage, name = 'homepage'),
   path('event/<int:pk>', eventpage, name = 'event_page'),
   path('registration-confirmaton/<int:pk>', registration_confirmation, name = 'registration_confirmaton'), 
   path('profile/<int:pk>', profile, name = 'profile'),
   path('account/', account, name = 'account'),
   path('project-submission/<int:pk>', project_submission, name = 'psubmission'),
   path('project-submission-edit/<int:pk>', updated_submission, name = 'pesubmission'),
   path('login/', login_page, name = 'login'),
   path('logout/', logout_f, name = 'logout'),

   path('register/', register_page, name = 'register'),




]