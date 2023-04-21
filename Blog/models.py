from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse("blogs:category", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title
    
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Post(TimeStampMixin):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    overview = models.TextField()
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    views = models.IntegerField(default=0)


    def get_absolute_url(self):
        return reverse("blog:post", kwargs={"slug": self.slug})
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(max_length=1000, help_text='Ingrese un comentario')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        len_title = 15
        if len(self.content) > len_title:
            return self.content[:len_title] + '...'
        return self.content