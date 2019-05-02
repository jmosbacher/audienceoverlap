from django.db import models


class Account(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=150, default='', blank=True)
    access_token = models.CharField(max_length=500, default='', blank=True)

    def get_absolute_url(self):
        return f'audience_manager/accounts/{self.id}'


class Audience(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, default='')
    size = models.PositiveIntegerField(default=0)


class Overlap(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    account = models.ForeignKey(Account, related_name='overlaps', on_delete=models.CASCADE)
    audience_1 = models.ForeignKey(Audience, related_name='overlaps_1', on_delete=models.CASCADE)
    audience_2 = models.ForeignKey(Audience, related_name='overlaps_2', on_delete=models.CASCADE)
    overlap = models.PositiveIntegerField(default=0)
    fetch_date = models.DateTimeField()


class Video(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    account = models.ForeignKey(Account, related_name='videos' , on_delete=models.CASCADE)
    link = models.CharField(max_length=500)
    
    fetch_date = models.DateTimeField()

    