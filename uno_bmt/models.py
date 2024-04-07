from django.contrib.auth import get_user_model
from django.db import models


class Members(models.Model):
    member_name = models.CharField(max_length=255)
    member_added_date = models.IntegerField()
    members_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.member_name

    class Meta:
        ordering = ('member_name',)
        verbose_name_plural = 'Members'
        db_table = 'members'


class WorldNews(models.Model):
    news_title = models.CharField(max_length=255)
    news_description = models.TextField()
    news_content = models.TextField()
    news_image = models.ImageField(upload_to='news/', blank=True)
    news_date = models.DateTimeField(auto_now_add=True)
    add_views_count = models.IntegerField(default=0)
    news_author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    news_areas = models.ForeignKey(Members, on_delete=models.CASCADE)

    def __str__(self):
        return self.news_title

    class Meta:
        db_table = 'worldnews'
        verbose_name_plural = 'WorldNews'
        ordering = ('news_date',)
