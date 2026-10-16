from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.PositiveIntegerField()
    description = models.TextField(max_length=700)
    poster = models.ImageField(upload_to="movies/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta :
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.release_year}"
