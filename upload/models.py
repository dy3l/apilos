import uuid

from rest_framework import serializers

from django.db import models

# Create your models here.
class UploadedFile(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=255, null=True)
    filepath = models.CharField(max_length=255, null=True, unique=True)
    size = models.CharField(max_length=255, null=True)
    content_type = models.CharField(max_length=255, null=True)
    thumbnail = models.CharField(max_length=100000, blank=True, null=True)

    def __str__(self):
        return self.filename


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = "__all__"