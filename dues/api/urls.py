from django.shortcuts import render
from django.urls import path

from dues.api.dues_entery_views import admin_get_all_dues_entry_view, delete_dues_entry, edit_dues_entry, get_all_dues_entry_view, pay_dues
from dues.api.dues_pay_period_views import add_dues_pay_period, archive_dues_pay_period, delete_dues_pay_period, edit_dues_pay_period, get_all_archived_dues_pay_period_view, get_all_dues_pay_period_view, unarchive_dues_pay_period
from dues.api.views import add_year_group_bank_account, delete_bank_account, get_all_bank_account_view


app_name = 'dues'


urlpatterns = [
    path('add-bank-account/', add_year_group_bank_account, name='add_bank_account'),
    path('get-all-bank-accounts/', get_all_bank_account_view, name="get_all_bank_account_view"),
    #path('archive-news/', archive_news, name="archive_news"),
    path('delete-bank-account/', delete_bank_account, name="delete_bank_account"),
    #path('unarchive-news/', unarchive_news, name="unarchive_news"),


    ### Pay Period
    path('add-dues-pay-period/', add_dues_pay_period, name="add_dues_pay_period"),
    path('edit-dues-pay-period/', edit_dues_pay_period, name="edit_dues_pay_period"),
    path('get-all-dues-pay-periods/', get_all_dues_pay_period_view, name="get_all_dues_pay_period_view"),
    path('archive-dues-pay-period/', archive_dues_pay_period, name="archive_dues_pay_period"),
    path('unarchive-dues-pay-period/', unarchive_dues_pay_period, name="unarchive_dues_pay_period"),
    path('delete-dues-pay-period/', delete_dues_pay_period, name="delete_dues_pay_period"),
    path('get-all-archived-dues-pay-periods/', get_all_archived_dues_pay_period_view,
         name="get_all_archived_dues_pay_period_view"),

    ### dues Payroll Entry
    path('pay-dues/', pay_dues, name="pay_dues"),
    path('edit-dues-entry/', edit_dues_entry, name="edit_dues_entry"),
    path('admin/get-all-dues-entries/', admin_get_all_dues_entry_view, name="admin_get_all_dues_entry_view"),
    path('get-all-dues-entries/', get_all_dues_entry_view, name="get_all_dues_entry_view"),

    #path('get-dues-entry-details/', get_dues_entry_details_view, name="get_dues_entry_details_view"),
    #path('archive-dues-entry/', archive_dues_entry, name="archive_dues_entry"),
    #path('unarchive-dues-entry/', unarchive_dues_entry, name="unarchive_dues_entry"),
    path('delete-dues-entry/', delete_dues_entry, name="delete_dues_entry"),
    #path('get-all-archived-dues-entries/', get_all_archived_dues_entry_view, name="get_all_archived_staff_pay_period_view"),

    
    #path('<str:account_id>/transactions/', list_transactions_view, name='bankaccount-transactions'),
    #path('<str:user_id>/client-transactions/', client_list_transactions_view, name='client-bankaccount-transactions'),
    #path('<str:account_id>/balance/', get_account_balance_view, name='bankaccount-balance'),
    #path('<str:account_id>/deposit/', deposit_view, name='bankaccount-deposit'),
    #path('<str:user_id>/client-deposit/', client_deposit_view, name='client-bankaccount-deposit'),
    #path('<str:user_id>/client-withdraw/', client_withdraw_view, name='client-bankaccount-withdraw'),
    #path('<str:account_id>/withdraw/', withdraw_view, name='bankaccount-withdraw'),
    #path('<str:account_id>/transfer/', transfer_view, name='bankaccount-transfer'),
]