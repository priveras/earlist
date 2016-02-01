from django.db import models
from django.db.models import permalink
from django.core.urlresolvers import reverse


class Post(models.Model):
	title = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(max_length=200, unique=True)
	body = models.TextField()
	link = models.CharField(max_length=200, unique=True)
	image_url = models.CharField(max_length=1000)
	created_at = models.DateField(db_index=True, auto_now_add=True)
	# category = models.ForeignKey('Category')

	def __str__(self):
		return self.title

class Event(models.Model):
	title = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(max_length=200, unique=True)
	body = models.TextField()
	link = models.CharField(max_length=200, unique=True)
	image_url = models.CharField(max_length=1000)
	cover_url = models.CharField(max_length=1000)
	event_date = models.DateField(db_index=True)
	created_at = models.DateField(db_index=True, auto_now_add=True)

	def __str__(self):
		return self.title

class Job(models.Model):
	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	company = models.CharField(max_length=200)
	link = models.CharField(max_length=200, unique=True)
	image_url = models.CharField(max_length=1000)
	created_at = models.DateField(db_index=True, auto_now_add=True)

	def __str__(self):
		return self.title

# class Category(models.Model):
# 	title = models.CharField(max_length=200, db_index=True)
# 	slug = models.SlugField(max_length=200, db_index=True)

# 	def __str__(self):
# 		return self.title

