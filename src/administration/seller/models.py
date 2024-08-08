from core.settings import AUTH_USER_MODEL as User
from django.db import models



# Create your models here.
class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor_profile")
    store_name = models.CharField(max_length=255)
    store_description = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="seller_profile", blank=True, null=True)
    # Add more fields as needed

    def __str__(self):
        return self.store_name
