from typing import DefaultDict
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager, Group, PermissionsMixin
from django.db.models.deletion import SET_NULL
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


# VALIDATOR


def validate_image(image):
    file_size = image.file.size
    limit_mb = 1
    if file_size > limit_mb * 1024 * 1024:  # 1kb = 1024b ; 1mb = 1024kb
        raise ValidationError("Max size of file is %s MB" % limit_mb)


class MyAccountManager(BaseUserManager):
    # if u have other mandatory field for registration, add it to param
    def create_user(self, email, username, password, address, phone):
        if not email:
            raise ValueError("Users must have an email!")
        if not username:
            raise ValueError("Users must have a username!")
        if not password:
            raise ValueError("Users must have a password!")
        if not address:
            raise ValueError("Users must have an address!")
        if not phone:
            raise ValueError("Users must have a phone number!")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
            address=address,
            phone=phone
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, phone, address):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            phone=phone,
            address=address
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email",
                              max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+9999999'. Up to 15 digits allowed")
    phone = models.CharField(max_length=255, validators=[phone_regex], blank=True)
    group = models.ForeignKey(Group, on_delete=SET_NULL, null=True)

    # Required fields for custom user model
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Set identifier of the user model, the selected field(s) must be unique
    USERNAME_FIELD = 'username'

    # Set other required field(s) for the user to filled in when registering a user
    REQUIRED_FIELDS = ['email', 'password', 'phone', 'address']

    # Tell account model where to find account manager
    objects = MyAccountManager()

    # Set the name of user object when printed on template(.html files)
    def __str__(self):
        return self.username

    # Required permission (learn it later). If inherit PermissionMixins, dont need these line of codes
    # def has_perm(self, perm, obj=None):
    #     return self.is_admin

    # def has_module_perms(self, app_label):
    #     return True


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.BigIntegerField()
    extra = models.CharField(max_length=200)

    # upload to folder media/products, before do this make sure to install Pillow and set up ur media in settings.py
    picture = models.ImageField(
        upload_to='products', validators=[validate_image])
    date_added = models.DateField(auto_now_add=True, null=True)
    placeholder = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    ORDERSTATS = (('Pending', 'Pending'), ('In Delivery', 'In Delivery'),)
    customer = models.ForeignKey(
        Account, related_name="order", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(
        Product, related_name="order", on_delete=SET_NULL, null=True)
    status = models.CharField(max_length=200, choices=ORDERSTATS)
    order_date = models.DateField(auto_now_add=True, null=True)
    quantity = models.IntegerField(null=True)
    price_sum = models.FloatField(null=True)

    def __str__(self) -> str:
        if len(str(self.id)) == 1:
            return '00'+str(self.id)+'_'+self.customer.username
        if len(str(self.id)) == 2:
            return '0'+str(self.id)+'_'+self.customer.username
        else:
            return str(self.id)+'_'+self.customer.username
