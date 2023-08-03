from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _ 
from django.db import models
from django.utils import timezone
from django.conf import settings



class UserManager(BaseUserManager):
    """Define a model manager for User model with username field."""

    use_in_migrations = True

    def _create_user(self, username,  email, password, **extra_fields):
        """Create and save a User with the given username and password."""
        if not username:
            raise ValueError('You must provide an username')
       
        email = self.normalize_email(email)
        user = self.model(
                            username=username,
                             **extra_fields
                             )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, email,  password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self._create_user(username, email,  password, **extra_fields)


class User(AbstractUser):
    """Custom User model
    """
    
    USER_GROUP_CHOICES = (
    ('confirmed_author', 'confirmed author'),
    ('not_confirmed_author', 'not confirmed author'),
    ('moderator', 'moderator'),
    ('user', 'user'),
    )

    SUBSCRIPTIONS_TYPE_CHOICES = (
    ('freebello', 'freebello'),
    )

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=100, unique=True)
    avatar = models.ImageField(upload_to='images/users/avatar/%Y/%m/%d/', null=True)
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created = models.DateTimeField(default=timezone.now, db_index=True)
    verify_email = models.BooleanField(default=False)
    black_list = models.ManyToManyField('User', related_name='bloced_users')
    user_group = models.CharField(
        max_length=50,
        verbose_name='group_users',
        choices=USER_GROUP_CHOICES,
        default='user',
    )
    facebook = models.CharField(max_length=100, null=True, blank=True)
    twiter = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    pinterest = models.CharField(max_length=100, null=True, blank=True)
    dribbble = models.CharField(max_length=100, null=True, blank=True)
    behance = models.CharField(max_length=100, null=True, blank=True)
    linkedin = models.CharField(max_length=100, null=True, blank=True)
    github = models.CharField(max_length=100, null=True, blank=True)
    figma = models.CharField(max_length=100, null=True, blank=True)
    website_url = models.CharField(max_length=100, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True)
    is_affiliate = models.BooleanField(default=False)
    #payment_method = (номер карты, месяц и год в формате MM/YY, CVV, а также Country (выбирается из списка))
    #карт может быть несколько, нужно дать возможность выбраь любую из сохраненных
    subscriptions = models.CharField(max_length=100, choices=SUBSCRIPTIONS_TYPE_CHOICES, null=True, blank=True)
    #?subscriptions = выбор из 3-х типов подписок. Подписки платные. В зависимости от типа подписки пользователь получает скидку на покупку платных продуктов.

    #?authorized_devices = device/browser (вероятно единым полем, так как в нем хранится например 'Chrome on Win10 (Desktop)'), Location (текстовое поле), sign_in_date (дата), accepted (True или Folse)
    #?таких authorized_devices может быть несколько
    
    #user_notifications = список чекбоксов (со значениями True или Folse):
    # Top_new_products, Free_goods, Trending_products, favorite_shops_news, new_message, new_update
    #Склько может быть аффилиатов. Аффилиат - это сам пользователь а не магазин. 
    #Просто страницы аффилиата на фронте проще отображать там же где и страницы магазина. 
    
        #prod_arrange = массив {имя продукта либо ID и индекс}, необ. Default - по дате создания.
    
    #?earning_reports, new_purchase, new_comment, new_review, new_like
    objects = UserManager()
    USERNAME_FIELD = 'username'
    
    
class Moderator(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_moderator')
    # = список чекбоксов (со значениями True или Folse). Данную рассылку получают только стаф магазина:
    shop_notifications = models.BooleanField(default=False)
