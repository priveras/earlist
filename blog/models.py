from django.db import models
from django.contrib.auth.models import User
from django.db.models import permalink
from django.core.urlresolvers import reverse
from meta.models import ModelMeta
import datetime

class Post(ModelMeta, models.Model):
	user = models.ForeignKey(User)
	title = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(max_length=200, unique=True)
	slogan = models.CharField(max_length=200)
	body = models.TextField()
	link = models.URLField(max_length=200, unique=True)
	image_file = models.FileField(upload_to='images/%Y%m%d', blank=True)
	city = models.CharField(max_length=200)
	approved = models.IntegerField()
	votes = models.IntegerField(default=0)
	date = models.DateField(auto_now_add=True)
	created_at = models.DateTimeField(db_index=True, auto_now_add=True)
	updated_at = models.DateTimeField(auto_now_add=True)
	# image_url = models.URLField(max_length=1000)
	# category = models.ForeignKey('Category')

	def __str__(self):
		return self.title.encode('utf-8')

	def get_absolute_url(self):
		return reverse('detail', kwargs={'slug':self.slug})

class Voter(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(db_index=True, auto_now_add=True)


# class Event(models.Model):
# 	user = models.ForeignKey(User)
# 	title = models.CharField(max_length=200, unique=True)
# 	slug = models.SlugField(max_length=200, unique=True)
# 	body = models.CharField(max_length=200)
# 	link = models.CharField(max_length=200, unique=True)
# 	image_file = models.FileField(upload_to='images/%Y%m%d', blank=True)
# 	cover_file = models.FileField(upload_to='images/%Y%m%d', blank=True)
# 	date_time = models.DateTimeField(db_index=True, null=True)
# 	created_at = models.DateTimeField(db_index=True, auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return self.title

# class Job(models.Model):
# 	user = models.ForeignKey(User)
# 	title = models.CharField(max_length=200)
# 	slug = models.SlugField(max_length=200, unique=True)
# 	company = models.CharField(max_length=200)
# 	link = models.URLField(max_length=200, unique=True)
# 	image_url = models.URLField(max_length=1000)
# 	created_at = models.DateTimeField(db_index=True, auto_now_add=True)

# 	def __str__(self):
# 		return self.title

# class Category(models.Model):
# 	title = models.CharField(max_length=200, db_index=True)
# 	slug = models.SlugField(max_length=200, db_index=True)

# 	def __str__(self):
# 		return self.title

