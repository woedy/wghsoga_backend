from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


DEPARTMENT = (
    ('SECRETARY', 'SECRETARY'),
    ('HUMAN RESOURCES', 'HUMAN RESOURCES'),
    ('ADMIN', 'ADMIN'),
('LOGISTICS', 'LOGISTICS'),
('BILLING', 'BILLING'),
('OPERATIONS', 'OPERATIONS'),
('COMMERCIAL', 'COMMERCIAL'),
('CLIENT', 'CLIENT'),
('GUARD', 'GUARD'),
('LEGAL', 'LEGAL'),

)

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='user_notifications', on_delete=models.CASCADE)

    subject = models.CharField(max_length=1000, null=True, blank=True)

    content = models.TextField(null=True, blank=True)

    read = models.BooleanField(default=False)


    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



