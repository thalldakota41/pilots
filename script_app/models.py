from django.db import models
from django.db.models.fields.files import FileField

class Creator(models.Model):
    name = models.CharField(null=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    genre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.genre


class Show(models.Model):
    title = models.CharField(max_length=200)
    count = models.IntegerField()
    script = models.FileField(blank=True, null=True, upload_to="screenplays")
    creators = models.ManyToManyField(Creator, related_name='shows')
    tag = models.ManyToManyField(Tag, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# to create a variable to filter and print all shows with a certain gerne tag for the recommend feature:
# but the drama name will have to be dynamically generated. 
# recommend = Show.objects.filter(tag__genre='Drama')
# print (recommend)

class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length = 100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message




    

    
    
