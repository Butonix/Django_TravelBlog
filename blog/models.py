# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils import timezone


from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField



class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Create your models here.
class Post(models.Model):
	author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	text = RichTextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	published = models.BooleanField(default=False)
	likes = models.PositiveIntegerField(default=0)
	favourite = models.BooleanField(default=False)
	tags = models.ManyToManyField(Tag, blank=True)
	slug = models.SlugField(max_length=100, blank=False)

	def publish(self):
		self.published_date = timezone.now()
		self.published = True
		self.save()

	#def get_absolute_url(self):
	#	return reverse(
	#			'post_details', 
	#		kwargs={'post_pk':self.id}
	#			)

	def get_absolute_url(self):
		return reverse(
			'post_details',
			kwargs={'slug': self.slug, 'post_pk': self.id }
			)

	def __str__(self):
		return self.title


class Comment(models.Model):
	post = models.ForeignKey(Post, related_name='comments')
	detail = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	approve_comment = models.BooleanField(default=False)

	def approve(self):
		self.approve_comment = True
		self.save()

	def __str__(self):
		return self.detail


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	location = models.CharField(max_length=30, blank=True)

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
	instance.profile.save()
