from django.db import models




class Pilot(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    count = models.IntegerField()
    writer = models.CharField(max_length=200)
    year = models.IntegerField()
    script = models.FileField(blank=True, null=True, upload_to="scripts")
    poster = models.ImageField(blank=True, null=True, default='default.jpg', upload_to="posters")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length = 100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    

    
    
