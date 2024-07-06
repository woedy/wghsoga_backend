from django.urls import path

from accounts.api.views import register_user, verify_user_email, resend_email_verification, UserLogin, \
    PasswordResetView, confirm_otp_password_view, resend_password_otp, new_password_reset_view, remove_user_view, \
    edit_account, list_all_users_view, list_all_archived_users_view, get_user_details_view, archive_user_view, \
    unarchive_user_view, delete_user_view, validate_email, update_user_info_view

app_name = 'accounts'

urlpatterns = [
    #path('register-user/', register_user, name="register_user"),


    path('validate-email/', validate_email, name="validate_email"),
    path('register-user/', register_user, name="register_user"),
    path('edit-account/', edit_account, name="edit_account"),

    path('verify-user-email/', verify_user_email, name="verify_user_email"),
    path('resend-email-verification/', resend_email_verification, name="resend_email_verification"),
    path('login-user/', UserLogin.as_view(), name="login_user"),

    path('forgot-user-password/', PasswordResetView.as_view(), name="forgot_password"),
    path('confirm-password-otp/', confirm_otp_password_view, name="confirm_otp_password"),
    path('resend-password-otp/', resend_password_otp, name="resend_password_otp"),
    path('new-password-reset/', new_password_reset_view, name="new_password_reset_view"),

    #path('remove_user/', remove_user_view, name="remove_user_view"),


    path('get-all-users/', list_all_users_view, name="list_all_users_view"),
    path('get-all-archived-users/', list_all_archived_users_view, name="list_all_archived_users_view"),
    path('get-user-details/', get_user_details_view, name="get_user_details_view"),
    path('archive-user/', archive_user_view, name="archive_user_view"),
    path('unarchive-user/', unarchive_user_view, name="unarchive_user_view"),
    path('delete-user/', delete_user_view, name="delete_user_view"),

    path('update-user-info/', update_user_info_view, name="update_user_info_view"),

]
