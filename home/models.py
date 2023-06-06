# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

#"AuthGroup: Represents a user authentication group
#AuthGroupPermissions: Represents the permissions assigned to an authentication group.
#AuthPermission: Represents an individual permission.
#AuthUser: Represents a user with authentication-related fields.
#AuthUserGroups: Represents the relationship between a user and an authentication group.
#AuthUserUserPermissions: Represents the relationship between a user and individual permissions.
#DjangoAdminLog: Represents the admin log for actions performed in the Django admin interface.
#DjangoContentType: Represents a content type used by Django's content framework.
#DjangoMigrations: Represents the recorded database migrations.
#DjangoSession: Represents a session in Django.
#HomeMypost: Represents a post created by a user, including various property details.
#ListImage: Represents images associated with a post.
#UserProfile: Represents additional user profile information, including social media links and profile picture.
#Comment: Represents a comment posted by a user on a post.
#Review: Represents a user review for a property.
#Favorite: Represents the favorite relationship between a user and a post"

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class HomeMypost(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    descrip = models.TextField()

    dientich = models.TextField(blank=True, null=True)
    chieudai = models.TextField(blank=True, null=True)
    chieurong = models.TextField(blank=True, null=True)
    mattien = models.TextField(blank=True, null=True)  #mat tien hay trong hem
    duongtruocnha = models.TextField(blank=True, null=True)  #chieu rong duong truoc nha

    addressdetail = models.TextField(blank=True, null=True)
    address = models.TextField()
    city = models.TextField(blank=True, null=True)
    district = models.TextField(blank=True, null=True)

    name = models.TextField()
    email = models.TextField()
    images = models.ImageField(max_length=100, blank=True, null=True, upload_to='images/')

    bathroom = models.TextField(blank=True, null=True)
    bedroom = models.TextField(blank=True, null=True)
    solau = models.TextField(blank=True, null=True)  #số tầng

    price = models.TextField(blank=True, null=True)
    guess_price = models.TextField(blank=True, null=True)
    dochinhxac =  models.TextField(blank=True, null=True)

    listimages = models.ManyToManyField('ListImage', blank=True)

    class Meta:
        managed = True
        db_table = 'home_mypost'

class ListImage(models.Model):
    listimage = models.ImageField(upload_to='list_images/')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fblink = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(max_length=100, blank=True, null=True, upload_to='profile_pics/')
    is_host = models.IntegerField(default=0)
    
    
class Comment(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(HomeMypost, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True, null=True)  # Field for posting time

    class Meta:
        managed = True
        db_table = 'home_cmt'

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField(blank=True, null=True)
    star = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'home_review'

        
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(HomeMypost, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

