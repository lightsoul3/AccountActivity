import sys

from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from io import BytesIO
from PIL import Image as PilImage



# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=32)
#    creator = models.ForeignKey(User, on_delete=models.PROTECT, default=User.objects.get(username='admin'))


    def __str__(self):
        return self.name


class Good(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField()
    description  = models.TextField()
    image = models.ImageField(upload_to='goods/images/' )
    preview = models.ImageField(upload_to='goods/previews/')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    creator = models.ForeignKey(User, on_delete=models.PROTECT, default=User.objects.get(username='admin'))

    # Save method to handle image resizing and preview creation
    def save(self, **kwargs):
        # Set the desired size for the preview image
        output_size = (100, 100)

        # Create an in-memory buffer to store the resized image
        output_thumb = BytesIO()

        # Open the original image using the Python Imaging Library (PIL)
        img = PilImage.open(self.image)

        # Extract the name of the image file without the extension
        img_name = self.image.name.split(".")[0]

        # Check if the original image size exceeds the desired preview size
        if img.height > 100 or img.width > 100:

            # Resize the image to the specified output size
            img = img.resize(output_size)

            # Save the resized image to the in-memory buffer in PNG format
            img.save(output_thumb, format="PNG", quality=90)

        # Extract the file extension of the original image and update the 'type' field
        self.type = self.image.path.split(".")[-1]

        # Create an InMemoryUploadedFile for the preview image
        self.preview = InMemoryUploadedFile(
            output_thumb,
            "ImageField",
            f"{img_name}_preview.png",
            "image/png",
            sys.getsizeof(output_thumb),
            None,
        )

        super(Good, self).save()
