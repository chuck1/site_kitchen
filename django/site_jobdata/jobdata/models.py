from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
    )

import django.core.files.base

# Create your models here.

import json

import jobdata.funcs
import jobdata.myjson

class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
            date_of_birth=date_of_birth
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Person(models.Model):
    user = models.OneToOneField(MyUser)
    file = models.FileField(null=True, blank=True)
   
    def __unicode__(

    def file_read(self):
        f = self.file
        if f:
            s = f.read()
        else:
            s = "{}"
        return s

    def file_read_json(self):
        s = self.file_read()
        j = json.loads(s)
        return j

    def file_save(self, s):
        fn = jobdata.funcs.clean(self.user.email) + '.json'
        cf = django.core.files.base.ContentFile(s)
        self.file.save(fn, cf)

    def file_save_json(self, j):
        s = json.dumps(j)
        self.file_save(s)

    def validate_json(self):
        j = self.file_read_json()
        for v in jobdata.myjson.json_iter_list_of_dict(j):
            if jobdata.myjson.json_list_of_dict_field_any(v, 'version'):
                print "adding fields"
                jobdata.myjson.json_dict_list_add_field_if_not_exists(v, 'version', [])
                jobdata.myjson.json_dict_list_add_field_if_not_exists(v, '_selector', [])
        self.file_save_json(j)

class Company(models.Model):
    name = models.CharField(max_length=256)

class Position(models.Model):
    name    = models.CharField(max_length=256)
    company = models.ForeignKey(Company)

class DocTemplate(models.Model):
    path    = models.CharField(max_length=256)

class Document(models.Model):
    person    = models.ForeignKey(Person)
    position  = models.ForeignKey(Position)
    template  = models.ForeignKey(DocTemplate)
    options   = models.CharField(max_length=256)
    file_html = models.FileField(null=True, blank=True)
    file_pdf  = models.FileField(null=True, blank=True)





