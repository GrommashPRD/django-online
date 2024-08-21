from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        related_name='sub_categories', blank=True, null=True
    )
    is_sub = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('women:category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    image = models.ImageField(upload_to='products')
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('women:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
