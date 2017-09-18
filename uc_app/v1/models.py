from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30)

    last_name = models.CharField(max_length=30)

    username = models.CharField(max_length = 100, unique=True)   # django automatically create iD as primary key

    password = models.CharField(max_length=100)

    item_owned = models.ManyToManyField(Item)

    # user_rating_stars = models.IntegerField()
    # ############
    # # FAVORITES
    # ############
    # favorite = models.ManyToManyField(Item)
    # ############
    # # BALANCE
    # # stores seller earning (can transfer to bank later) & promotion credit
    # ############
    # balance = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])


class Item(models.Model):
    item_name = models.CharField(max_length=100)

    item_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    ###########
    # SELLER
    ###########
    seller = models.ForeignKey(User, on_delete=models.CASCADE)  # 1 item have 1 seller
    #  when creating item, can indicate seller=username in Item field
    #  in views:
    #  item = Item(..... seller = __) to indicate which user is selling this item

    ###########
    # BUYER
    ###########
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # 1 item has 1 seller
    # buyer could be null when the item is being listed
    # to indicate buyer, in views:
    # item = Item.objects.get(id = __)
    # item.buyer = request.User

    # brand = models.CharField(max_Length=100)
    #
    # item_rating_stars = models.IntegerField()
    #
    # description = models.TextField()image_url = models.CharField(max_length=100)

    # ITEM_SIZES = (('S', 'Small'),('M', 'Medium'),('L', 'Large'),('OS', 'One Size'),('Other', 'Other'))
    # item_size = models.CharField(max_length = 15, choices=ITEM_SIZES)

    # ITEM_TYPES = (
    # 	('Top', 'Top'),
    # 	('Bottom', 'Bottom'),
    # 	('Other', 'Other')
    # )
    # item_type = models.CharField(max_Length= 15, choices = ITEM_TYPES)


# class Review(models.Model):
#     author = models.ForeignKey(User)
#     title = models.CharField(max_length=200)
#     body = models.TextField()
#
#     ##########
#     # POST TIME STAMP
#     ##########
#     posted_on = models.DateTimeField(
#             default=timezone.now)
#
#     def post(self):
#         self.posted_on = timezone.now()
#         self.save()
#
#
#     def __str__(self):
#         return self.title


# class Offer(models.Model):
# 	bidder = models.ForeignKey(User)
#
# 	offer_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
#
# 	offer_accepted = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])


# class AddressModelMixin(models.Model):
#     name = models.CharField("Full name", max_length=1024)
#     address1 = models.CharField("Address line 1", max_length=1024)
#     address2 = models.CharField("Address line 2", max_length=1024, blank=True, null=True)
#     zipcode = models.CharField("ZIP", max_length=12)
#     city = models.CharField("City", max_length=1024)
#
#     class Meta:
#         abstract = True

