from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # This will save files in media/uploads/
    uploaded_at = models.DateTimeField(auto_now_add=True)
