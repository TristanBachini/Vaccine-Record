from django.urls import path
from . import views
from django.contrib.auth import views as v

urlpatterns = [
    path('',views.home, name="home"),
    #path('logout', views.logout, name="logout"),
    path('logout/',v.LogoutView.as_view(next_page='/'),name="logout"),
    path('reset/password-reset/', views.passwordReset, name="password-reset"),
    path('reset/password-reset/done/', v.PasswordResetDoneView.as_view(template_name='vaccinerecordapp/reset-password/password-reset-done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', v.PasswordResetConfirmView.as_view(template_name="vaccinerecordapp/reset-password/password-reset-confirm.html"), name='password_reset_confirm'),
    path('reset/done/', v.PasswordResetCompleteView.as_view(template_name='vaccinerecordapp/reset-password/password-reset-complete.html'), name='password_reset_complete'),      
    path('create-patient/', views.create_patient, name="create-patient"),
    path('tool/', views.tool, name="tool"),
    path('tool/staff', views.staff, name="staff"),
    path('tool/staff/create-staff', views.create_staff, name="create-staff"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('create-patient-record/', views.create_patient_record, name="create-patient-record"),
    path('create-record/<username>', views.create_record, name="create-record"),
    path('patient-profile/<pk>', views.patient_profile, name="patient-profile"),
    path('tool/staff-profile/<pk>', views.staff_profile, name="staff-profile"),
    path('register-patient',views.register_patient, name="register-patient"),
    path('search-patient/', views.search_patient, name="search-patient"),
    path('patient-landing<pk>', views.patient_landing, name="patient-landing"),
    path('update-patient-profile/<pk>',views.update_patient_profile, name="update-patient-profile"),
    path('vaccine-record/', views.vaccine_record, name="vaccine-record"),
    path('display-vaccine/<pk>', views.display_vaccine_record, name="display-vaccine"),
    path('create-vaccine-record/<pk>', views.create_vaccine_record, name="create-vaccine-record"),
    path('appointment/<pk>', views.appointment, name="appointment"),
    path('certificate-md/<pk>', views.certificate_md, name="certificate-md"),
    path('certificate-pt/<pk>', views.certificate_pt, name="certificate-pt"),
    path('confirm-appointments/', views.confirm_appointments, name="confirm-appointments"),
    path('confirm-appointment/<pk>', views.confirm_appointment, name="confirm-appointment"),
    path('reject-appointment/<pk>', views.reject_appointment, name="reject-appointment"),
    path('reschedule-appointment/<pk>', views.reschedule_appointment, name="reschedule-appointment"),
    path('certificate-pdf-md/<int:pk>', views.GeneratePDF_MD.as_view(), name="generatepdf-md"),
    path('certificate-pdf-pt/<int:pk>', views.GeneratePDF_PT.as_view(), name="generatepdf-pt"),
    path('update-vaccine/<pk>', views.update_vaccine, name="update-vaccine"),
    path('update-profile/<pk>', views.update_profile, name="update-profile"),
    path('update-own-profile/<pk>', views.update_own_profile, name="update-own-profile"),
    path('own-profile/', views.own_profile, name="own-profile"),
    path('tool/report/', views.report, name="report"),
    path('tool/staff/update-staff', views.update_staff, name="update-staff"),
    path('tool/staff/update-staff-profile/<pk>', views.update_staff_profile, name="update-staff-profile"),
    path('tool/reminder/', views.reminder, name="reminder"),
    path('tool/reminder-vaccines/<pk>',views.reminder_vaccines, name="reminder-vaccines"),
    path('tool/reminder/send-email-reminder/<pk>',views.send_email_reminder, name="send-email-reminder")
    ]