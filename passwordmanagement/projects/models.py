from django.db import models
from django.conf import settings
from .aescbc import encrypt, decrypt

# Create your models here.


class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AccountType(Timestamped):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    class Meta:
        default_related_name = 'accounttypes'
        verbose_name = 'account type'
        verbose_name_plural = 'account types'

    def __str__(self):
        return self.name


class Project(Timestamped):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    class Meta:
        default_related_name = 'projects'
        verbose_name = 'project'
        verbose_name_plural = 'projects'

    def __str__(self):
        return self.name


class Password(Timestamped):
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    comments = models.TextField(blank=True)
    url = models.URLField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        default_related_name = 'passwords'
        verbose_name = 'password'
        verbose_name_plural = 'passwords'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        encrypted = encrypt(
            bytes(settings.SECRET_KEY, 'utf-8'), bytes(self.password, 'utf-8'))
        self.password = encrypted
        # decrypted = decrypt(bytes(settings.SECRET_KEY, 'utf-8'), encrypted)
        super().save(*args, **kwargs)

    def get_password(self):
        decrypted = decrypt(bytes(settings.SECRET_KEY, 'utf-8'), self.password)
        return decrypted.decode("utf-8")
