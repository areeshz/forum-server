from django.urls import path
from .views.mango_views import Mangos, MangoDetail
from .views.user_views import SignUp, SignIn, SignOut, ChangePassword
from .views.post_views import PostsManageView, PostDetailManageView
from .views.comment_views import Comments, CommentDetail

urlpatterns = [
	# Restful routing
    path('mangos/', Mangos.as_view(), name='mangos'),
    path('mangos/<int:pk>/', MangoDetail.as_view(), name='mango_detail'),
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('change-password/', ChangePassword.as_view(), name='change-pw'),
    # 'Posts' views
    path('posts/', PostsManageView.as_view(), name='posts'),
    path('posts/<int:pk>', PostDetailManageView.as_view(), name='posts-detail'),
    # 'Comment' views
    path('comments/', Comments.as_view(), name='comments'),
    path('comments/<int:pk>', CommentDetail.as_view(), name='comment-detail')
]
