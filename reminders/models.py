from django.db import models
import datetime
import markdown

class ReminderList(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title", "modified"]


    def markdown(self):
        return markdown.markdown(self.content)
