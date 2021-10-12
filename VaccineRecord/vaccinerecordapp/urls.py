from django.urls import path
from . import views
from django.contrib.auth import views as v

urlpatterns = [
    path('',views.home, name="home"),
    #path('logout', views.logout, name="logout"),
    path('logout/',v.LogoutView.as_view(next_page='/'),name="logout"),
    path('reset/password-reset/', views.passwordReset, name="password-reset"),
    path('reset/password-reset/done/', v.PasswordResetDoneView.as_view(template_name='vaccinerecordapp/password-reset-done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', v.PasswordResetConfirmView.as_view(template_name="vaccinerecordapp/password-reset-confirm.html"), name='password_reset_confirm'),
    path('reset/done/', v.PasswordResetCompleteView.as_view(template_name='vaccinerecordapp/password-reset-complete.html'), name='password_reset_complete'),      
    path('search-create-patient/', views.search_create_patient, name="search-create-patient"),
    path('create-patient/', views.create_patient, name="create-patient"),
    path('tool/', views.tool, name="tool"),
    path('tool/staff', views.staff, name="staff"),
    path('tool/staff/create-staff', views.create_staff, name="create-staff"),
    path('dashboard/', views.dashboard, name="dashboard"),
]