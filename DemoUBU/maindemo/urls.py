from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # user
    path("", views.home),
    path("logout/", views.logout_view),
    path('index/', views.index, name='index'),
    path('edit-profile/', views.edit_user_profile, name='edit-profile'),
    path('contact/', views.contact, name='contact'),
    path('rules/', views.rules, name='rules'),
    path('detail/<int:id>/', views.detail, name='detail'),
    path('confirm/<int:id>/', views.confirm, name='confirm'),
    path('history/', views.history, name='history'),
    path('cancel/<int:record_id>/', views.cancel_borrow, name='cancel_borrow'),
    path('check-cancels/', views.check_and_cancel_borrows, name='check_cancels'),
    
    #admin
    path('check-admin/', views.check_and_cancel_admin, name='check_admin'),
    path('create/',  views.create, name='create'),
    path('delete/<int:id>/',  views.delete, name='delete'),
    path('edit/<int:id>/',  views.edit, name='edit'),
    path('index-admin/', views.index_admin, name='index_admin'),
    path('approve-admin/', views.approve_admin, name='approve_admin'),
    path('noreturn-admin/', views.noreturn_admin, name='noreturn_admin'),
    path('reject/<int:record_id>/', views.reject, name='reject'),
    path('approve-borrow/<int:record_id>/', views.approve_borrow, name='approve_borrow'),
    path('return-item/', views.return_item, name='return_item'),
    path('return-confirm/<int:record_id>/', views.confirm_return, name='confirm_return'),
    path('not-returned/<int:record_id>/', views.not_returned, name='not_returned'),
    path('noreturn-admin/', views.noreturn_admin, name='noreturn_admin'),
    path('confirm_noreturn/<int:record_id>/', views.confirm_noreturn, name='confirm_noreturn'),
    path('dashboard/', views.dashboard, name='dashboard'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

