from django.db import models
from society.models import Society
import os
from django.utils.text import slugify
from backend.storages import OverwriteStorage
# Create your models here.
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError
import secrets
from django.dispatch import receiver


def compress_profile_pic(thumbnail, width_specified, image_name):
    temp_image = Image.open(thumbnail)
    output_io_stream = BytesIO()
    width, height = temp_image.size
    aspect_ration = width / height
    # final_image = temp_image.resize((width_specified, int(width_specified/aspect_ration)))
    # final_image = temp_image.resize((int(130 * aspect_ration),130))
    final_image = temp_image.resize((int(aspect_ration * 300), 300))
    final_image = final_image.convert('RGB')
    final_image.save(output_io_stream, format='JPEG', optimize=True, quality=75)
    output_io_stream.seek(0)
    thumbnail = InMemoryUploadedFile(output_io_stream, None, image_name+".jpg", 'image/jpeg', output_io_stream.tell(), None)
    return thumbnail



def random_number_generator():
    my_secure_rng = secrets.SystemRandom()
    rand_int = my_secure_rng.randrange(0, 100000)
    return rand_int


class Person(models.Model):

    def get_image_path(instance, filename):
        if instance.society:
            return os.path.join('media', 'people', instance.society.slug, slugify(instance.full_name_english + "-"+str(instance.random_number_after_name), allow_unicode=True), filename)
        else:
            return os.path.join('media', 'people', 'ieee-ntua-sb-board', slugify(instance.full_name_english + "-"+str(instance.random_number_after_name), allow_unicode=True), filename)

    full_name_greek = models.CharField(max_length=200, help_text="Όνομα στα Ελληνικά.")
    full_name_english = models.CharField(max_length=200, help_text="Όνομα στα Αγγλικά")
    role = models.CharField(max_length=200, help_text="Ρόλος του ατόμου.")
    profile_pic = models.ImageField(upload_to=get_image_path, storage=OverwriteStorage, max_length=350, help_text="Η εικόνα που θα ανεβάσετε να μην έχει το ίδιο όνομα με αυτή που είναι ανεβασμένη (αν υπάρχει ανεβασμένη εικόνα).")
    society = models.ForeignKey(Society, null=True, blank=True, on_delete=models.CASCADE)
    random_number_after_name = models.IntegerField(default=random_number_generator, editable=False)
    #social media
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)


    def __str__(self):
        return self.full_name_english
        
    def save(self, *args, **kwargs):
        self.full_name_english = self.full_name_english.strip().capitalize().title()
        self.full_name_english = self.full_name_english.strip().capitalize().title()
        self.role = self.role.strip().capitalize().title()
        
        if self.email:
            self.email = self.email.strip().lower()

        name_of_thumbnail = str(slugify(self.full_name_english, allow_unicode=True))+"-"+str(self.random_number_generator)
        if os.path.basename(self.profile_pic.name) != name_of_thumbnail+".jpg":
            self.profile_pic = compress_profile_pic(self.profile_pic, 130, name_of_thumbnail)
        super(Person, self).save(*args, **kwargs)


    # Unique together constraint validation error
    # def clean(self):
    #     # Check if another object exists with the same values for field1 and field2
    #     self.full_name = self.full_name.strip().capitalize().title()

    #     existing_obj = Person.objects.filter(full_name=self.full_name, society=self.society).exclude(pk=self.pk).first()
    #     if existing_obj is not None:
    #         # Raise a validation error if there is a match
    #         raise ValidationError("A record with these values already exists.")
    #     super().clean()


    class Meta:
        verbose_name_plural = 'People'

import shutil
@receiver(models.signals.post_delete, sender=Person)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image file from filesystem
    when corresponding `MyModel` object is deleted.
    """
    if instance.profile_pic:
        if os.path.isfile(instance.profile_pic.path):
            os.remove(instance.profile_pic.path)
        if os.path.exists(os.path.dirname(instance.profile_pic.path)):
            shutil.rmtree(os.path.dirname(instance.profile_pic.path), ignore_errors=True)
            # os.rmdir(os.path.dirname(instance.profile_pic.path))