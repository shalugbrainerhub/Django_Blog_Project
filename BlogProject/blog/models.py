from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# for Category model
class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)

    def __str__(self):
        return self.name
    



# for Author model
class Author(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField()
    profile_picture=models.ImageField(upload_to="profile_pic/")

    def __str__(self):
        return self.user.username






# for Post model
class Post(models.Model):
    title=models.CharField(max_length=50)
    content=models.TextField()
    pub_date=models.DateTimeField(auto_now_add=True)
    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    categories=models.ManyToManyField(Category,related_name="posts")

    def __str__(self):
        return self.title
