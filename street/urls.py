from django.urls import path
from django.contrib.auth import views as auth_views
from . views import (LoginPage,home_view, logout_view,client_dashboard,approval,
gift_card,upload_card,AboutUs,hustler_dashboard,Withdraw,approve_front,approve_back,register,
viewActive,quiz_expired,withdraw_time_extension)

app_name = 'street'
urlpatterns =[
    path('login/',LoginPage,name='login'),
	path('logout/', logout_view, name='logout'), 
    path('user/dashboard/', client_dashboard, name='client'), 
    path('oga/dashboard', hustler_dashboard, name='hustler'),
    path('amount/withdraw/', Withdraw, name='withdraw'),
    path('card_choice/', gift_card, name='gift_card'), 
    path('upload_card/', upload_card, name='upload_card'), 
    path(r'', home_view, name='home'),
    path('about_page/', AboutUs, name='about'),
    path('approve/front/<int:card_id>/', approve_front, name='approve_front'),
    path('approve/back/<int:card_id>/', approve_back, name='approve_back'),
    path('user_details/<int:id>/', viewActive, name='user_active'),
    path('new_user/', register, name='register'),
    path('approval/', approval, name='approval'),
    path('time_elasped/continue_quiz_user?', quiz_expired, name='quiz_expired'),
    path('extend_time_or_withdraw_cash/', withdraw_time_extension, name='extend_withdraw'), 
      
    
]