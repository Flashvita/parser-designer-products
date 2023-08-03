from django.db import models
from django.utils import timezone
from django.conf import settings

from slugify import slugify

from .utils import product_file_path


class Category(models.Model):
    """Model Category for products"""

    name = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    level = models.IntegerField()
    slug = models.SlugField(max_length=255, unique=False)
    road = models.CharField(max_length=500)
    alias = models.CharField(max_length=250, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def str(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            if not self.parent:
                self.level = 0
                self.road = self.slug + '/'
            else:
                self.level = self.parent.level + 1
                self.road = self.parent.road + self.slug + '/'
        super().save(*args, **kwargs)
    

class Product(models.Model):

    PUBLIC_STATUS_CHOICES = (
    ('pending_approval', 'pending approval'),
    ('rejected', 'rejected'),
    ('published', 'published'),
    ('draft', 'quarantined'),
)
    PRIVATE_STATUS_CHOICES = (
    ('hide', 'hide'),
    ('accepted', 'accepted'),
    ('new', 'new'),
    ('in_sorting', 'in sorting'),
    ('quarantined','quarantined'),
    )

    name = models.CharField(max_length=200)
    product_date = models.DateField(auto_now_add=True)
    product_file = models.FileField(
        upload_to=product_file_path,
        null=True,
        blank=True
    )
    file_size = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )
    orig_link = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    file_type = models.CharField(max_length=10)
    portfolio_link = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    parse_desc = models.TextField(
        max_length=67000,
        blank=True,
        null=True
    )
    seo_title = models.CharField(
        max_length=125,
        blank=True,
        null=True
    )
    seo_description = models.TextField(
        max_length=1000,
        blank=True,
        null=True
    )
    descr = models.TextField(
        max_length=67000,
        blank=True,
        null=True
    )
    public_status = models.CharField(
        max_length=50,
        choices=PUBLIC_STATUS_CHOICES,default='pending_approval'
    )
    private_status = models.CharField(
        max_length=50,
        choices=PRIVATE_STATUS_CHOICES,
        default=PRIVATE_STATUS_CHOICES[0][0]
        )
    manual = models.OneToOneField(
        'Manual',
        on_delete=models.CASCADE,
        related_name='product_manual',
        blank=True,
        null=True
    )
    shop = models.ForeignKey(
        'Shop',
        on_delete=models.CASCADE,
        related_name='shop_products', 
        blank=True,
        null=True
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='product_likes',
        blank=True,
        null=True 
    )
    accepted = models.BooleanField(default=True)
    reject_comment = models.TextField(
        max_length=500,
        null=True,
        blank=True
    )
    license = models.ManyToManyField(
        'License',
        related_name='product_licenses',
        blank=True,
        null=True
    )
    created = models.DateTimeField(default=timezone.now, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    product_alias = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField(
        'Tag',
        related_name='products',
        blank=True,
        null=True 
        )
    category = models.ForeignKey(
        'Category',
        related_name='product_category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    properties = models.CharField(max_length=255, blank=True, null=True)
    migration = models.BooleanField(default=False)
    
    
    def save(self, *args, **kwargs):
        text = """Your product was rejected due to the fact that it does 
        not meet the quality requirements of our site. Try to improve 
        the presentation and quality of the product and 
        try again! <br><br> Chat with the friendly community of our authors,
        and they will tell you how you can improve your product. We wish you good luck!"""
        if self.public_status == 'pending_approval':
            self.reject_comment == text
            return super().save(*args, **kwargs)
    
    @property
    def product_url_alias(self):

        return f'{self.author_url_alias}/{self.product_alias}'

TAG_STATUS_CHOICE = (
    ('indexed', 'indexed'),
    ('not_indexed', 'not indexed'),
    ('not_considered', 'not considered'),
   
)

class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=50,
        choices=TAG_STATUS_CHOICE,
        default=TAG_STATUS_CHOICE[2][0]
        )


class Search(models.Model):
    SEARCH_STATUS_CHOICE = (
    ('indexed', 'indexed'),
    ('not_indexed', 'not indexed'),
    ('not_considered', 'not considered'),
    )
    title = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, choices=TAG_STATUS_CHOICE, default='not considered')


class License(models.Model):
    LICENSE_TYPE_CHOICES = (
    ('100_free', '100% free'),
    ('100_free_premium', '100% free premium'),
    ('personal_use','personal use'),
    ('commercial_use', 'commercial use'),
    ('extended_commercial', 'extended commercial'),
)
    type = models.CharField(max_length=50, choices=LICENSE_TYPE_CHOICES)
    price = models.PositiveIntegerField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='author_licenses'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_licenses'
    )

    class Meta:
        verbose_name = 'License'
        verbose_name_plural = 'Licenses'


class Image(models.Model):
   
    image = models.ImageField(upload_to= 'images/%Y/%m/%d/', null=True)
    date = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=100, blank=True, null=True)

    def str(self):
        return self.image.name

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class Presentation(models.Model):
    cover = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='cover_image')
    images = models.ManyToManyField(Image, related_name='presentation_images')
    #Добавить последовательность у файлов
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.OneToOneField('Product', on_delete=models.CASCADE, related_name='product_presentations')
    #Все изображения храняться в виду ссылок на яндекс облако

    class Meta:
        verbose_name = 'Presentation'
        verbose_name_plural = 'Presentations'


class Shop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    descr = models.TextField(max_length=1000, null=True, blank=True)
    alias = models.CharField(max_length=125)
    owners = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shop_owner')
    #staff = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shop_staff', null=True, blank=True)
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shop_managers', null=True, blank=True)
    assistants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shop_assistants', null=True, blank=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shop_custom_users', null=True, blank=True)
    custom_rules = models.OneToOneField('CustomPermisson', on_delete=models.CASCADE, related_name='shop_custom_users', null=True, blank=True)
    #Как овнер соотноситься с автором
    #лучше staff вместо manager. Потому что manager это название конкретной роли. У стафа будет несколько ролей.
    #для начала хватит одной роли стафа, и пусть это будет manager. Но привязку лучше делать скорее всего через staff, потому что кол-во ролей добавится
    #staff = список пользователей
    shop_logo = models.ImageField(upload_to='shop/logo/%Y/%m/%d/', null=True, blank=True)
    shop_banner = models.ImageField(upload_to='shop/banner/%Y/%m/%d/', null=True, blank=True)
    #dealer = models.BooleanField(default=False)
    #subscriptions = модель подписок. Будет содержать 1 магазин и список пользователей, либо в самом магазине зашить
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shop_followers' )
    #Cколько может быть дилеров в магазине
    #Дилером является сам магазин. Стало быть функциями дилера управляет весь стаф, у которого есть права. Включая овнеров.

    
    #announcements = другая модель. Каждый анонс это заголовок, текст, картинка и дата публикации
    #events = возможно, другая модель. К событиям относятся всевозможные обновления магазина (публикация новых продуктов, апдейт продуктов, распродажа и прочее)
    

class HintChain(models.Model):
    STATUS_HINT_CHOICES = (
        ('new', 'new'),
        ('skipped', 'skipped'),
        ('done', 'done'),
    )
    status = models.CharField(max_length=50, choices=STATUS_HINT_CHOICES, default='new')
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='hint_shops')


class CustomPermisson(models.Model):
    #Спросить подробнее о кастомных правах
    #Написать модель с кастомными правами
    analythics = models.BooleanField(default=False)#есть доступ к просмотру аналитики или нет
    products_edit = models.BooleanField(default=False)#есть доступ к редактированию продуктов
    products_delete = models.BooleanField(default=False)# есть доступ к удалению продуктов
    migration = models.BooleanField(default=False) #есть доступ к созданию миграций или нет
    marketing = models.BooleanField(default=False) #есть доступ к вкладкам Matketing Tools
    shop_main = models.BooleanField(default=False) #есть доступ к вкладкам Shop Description
    shop_info = models.BooleanField(default=False) #есть доступ к Shop Design, Arrangement, Announcements
    shop_team = models.BooleanField(default=False) #есть доступ к приглашению и удалению стафа (кроме овнеров)
    shop_messages = models.BooleanField(default=False) #есть доступ отвечать на сообщения/комментарии на сайте от имени магазина
 

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    created = models.DateField(auto_now_add=True)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)
    #привязка к магазину от чьего имени выпущен анонс
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)


class Sale(models.Model):
    # Какие продукты выбраны для распродажи (выбирать можно только платные)
    products = models.ManyToManyField('Product', related_name='products_sales')
    summ_sales = models.PositiveIntegerField()
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    # Сумма скидки на данные продукты
    # Дата начала распродажи
    # Дата окончания распродажи


class IntegerRangeField(models.IntegerField):
    """ Integer field with min and max value
    """
    def init(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.init(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Review(models.Model):
    comment = models.CharField(max_length=200, null=True, blank=True)
    rating = IntegerRangeField() #от одного до пяти
    created = models.DateTimeField(auto_now=True)
    #created = дата создания ревью
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='product_reviews'
    )       
    #привязка к продукту. Нужн сделать таким образом, чтобы в ЛК у пользователя напротив продуктов отображалось приглашение написать ревью для тех продуктов, для которых он ревью еще не написал
    #likes


class Comment(models.Model):
    comment = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
        #привязка к продукту.


#Продукты могут входить в Deals. Deal - это когда несколько разных магазинов скидываются продуктами и устраивают совместную распродажу
class Deal(models.Model):
    organizer = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='organizer_deals'
    )
    # dealer = привязка к пользователю-дилеру, кто создал данный deal
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='participants_deals'
    )
    # список участников (приглашенных дилером с их долями в Deal)# Как он будет их приглашать?
    products_enter = models.ManyToManyField(
        'Product',
        related_name='products_deals_enter'
    )
    # список продуктов-точек входа
    products_payable = models.ManyToManyField(
        'Product',
        related_name='products_deals_payable'
    )
    # список платных продуктов
    start_date = models.DateTimeField()
    finish_date = models.DateTimeField()
    # дата начала и дата окончания Deal
    percent_discount = models.IntegerField()
    # скидка от общей стоимости продуктов (вероятно в %)
    # итоговая стоимость продуктов    