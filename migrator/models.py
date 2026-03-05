from django.db import models

# Create your models here.

class MigrationTask(models.Model):
    source_email = models.EmailField()
    destination_email = models.EmailField()
    folder_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default="Running") # Running, Completed, Failed
    log_output = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_email} -> {self.folder_name}"