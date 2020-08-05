from django.urls import path
from .views.mango_views import Mangos, MangoDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword
from .views.post_views import PostsIndex, PostsCreate, PostsShow, PostDetail

urlpatterns = [
	# Restful routing
    path('mangos/', Mangos.as_view(), name='mangos'),
    path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-pw/', ChangePassword.as_view(), name='change-pw'),
    path('feed/', PostsIndex.as_view(), name='posts-index'),
    path('posts/', PostsCreate.as_view(), name='posts-create'),
    path('feed/<int:pk>', PostsShow.as_view(), name='posts-show'),
    path('posts/<int:pk>', PostDetail.as_view(), name='posts-show')
]
