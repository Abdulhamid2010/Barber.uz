from django.urls import path
from . import views
urlpatterns=[
path("",views.home,name="home"),path("barbers/",views.barbers,name="barbers"),
path("barber/<int:pk>/",views.barber_detail,name="barber_detail"),path("book/<int:pk>/",views.book,name="book"),
path("favorite/<int:pk>/",views.favorite,name="favorite"),path("review/<int:pk>/",views.review,name="review"),
path("register/",views.register_view,name="register"),path("login/",views.login_view,name="login"),
path("logout/",views.logout_view,name="logout"),path("dashboard/",views.dashboard,name="dashboard"),
path("booking/<int:pk>/<str:action>/",views.booking_action,name="booking_action"),
path("barber/setup/",views.barber_setup,name="barber_setup"),
path("barber/video/add/",views.add_video,name="add_video"),
path("payment/<int:booking_id>/",views.payment_demo,name="payment_demo")]
