from django.db import models
from ckeditor.fields import RichTextField
import os
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify
from backend.storages import OverwriteStorage
from backend.utils import capitalize_first_character, sanitize_html, emoji_pattern, remove_emoji_img_tags
from django.core.exceptions import ValidationError
from django.dispatch import receiver
# Create your models here.


def compress_society_logo(thumbnail, width_specified, image_name):
    temp_image = Image.open(thumbnail)
    output_io_stream = BytesIO()
    width, height = temp_image.size
    aspect_ration = width / height
    final_image = temp_image.resize((width_specified, int(width_specified/aspect_ration)))
    final_image = final_image.convert('P', palette=Image.ADAPTIVE, colors=256)
    final_image.save(output_io_stream, format='PNG', optimize=True, quality=40, compress_level=9)
    # final_image.save(output_io_stream, format='webp')
    # thumbnail = InMemoryUploadedFile(output_io_stream, None, f"{image_name}.webp", 'image/webp', output_io_stream.tell(), None)
    thumbnail = InMemoryUploadedFile(output_io_stream, None, f"{image_name}.png", 'image/png', output_io_stream.tell(), None)

    return thumbnail
    

def compress_event_thumbnail(thumbnail, width_specified, image_name):
    temp_image = Image.open(thumbnail)
    output_io_stream = BytesIO()
    width, height = temp_image.size
    aspect_ration = width / height
    final_image = temp_image.resize((width_specified, int(width_specified/aspect_ration)))
    final_image = final_image.convert('RGB')
    final_image.save(output_io_stream, format='JPEG', optimize=True,quality=60)
    # final_image.save(output_io_stream, format='webp')
    output_io_stream.seek(0)
    thumbnail = InMemoryUploadedFile(output_io_stream, None,image_name+".jpg", 'image/jpeg', output_io_stream.tell(), None)
    return thumbnail
    

def compress_background_hero(thumbnail,width_specified,image_name):
    temp_image = Image.open(thumbnail)
    output_io_stream = BytesIO()
    width, height = temp_image.size
    aspect_ration = width / height
    final_image = temp_image.resize((width_specified, int(width_specified/aspect_ration)))
    final_image = final_image.convert('RGB')
    final_image.save(output_io_stream, format='JPEG')
    # final_image.save(output_io_stream, format='webp')
    output_io_stream.seek(0)
    thumbnail = InMemoryUploadedFile(output_io_stream, None,image_name+"-background.jpg", 'image/jpeg', output_io_stream.tell(), None)
    return thumbnail


class Society(models.Model):
    
    SUBGROUP_LABEL_CHOICES = (
        ('Subgroups', 'Subgroups'),
        ('Projects', 'Projects'),
    )


    def get_image_path(instance, filename):
        return os.path.join('media', 'society', str(instance.slug), filename)

    def get_background_hero_image(instance, filename):
        return os.path.join('media', 'chapter_background_images', str(instance.slug), filename)

    title = models.CharField(max_length=200, unique=True, primary_key=True, help_text='Δεν αλλάζει ο τίτλος που θα βάλετε. Εάν θέλετε να τον αλλάξετε φτιάξτε καινούργιο society και διαγράψτε αυτό.')
    short_title = models.CharField(max_length=100, help_text="Ο σύντομος τίτλος (π.χ. CS, RAS ...)")
    slug = models.SlugField(max_length=200, unique=True)
    logo = models.ImageField(upload_to=get_image_path, storage=OverwriteStorage, help_text="Η εικόνα που θα ανεβάσετε να μην έχει το ίδιο όνομα με αυτή που είναι ανεβασμένη (αν υπάρχει ανεβασμένη εικόνα).")
    hero_image = models.ImageField(upload_to=get_background_hero_image, storage=OverwriteStorage, help_text="Η background εικόνα που εμφανίζεται μόλις ανοιχτεί το συγκεκριμένο chapter page.")
    greek_body = RichTextField(max_length=10000)
    english_body = RichTextField(max_length=10000)
    recruitment_form = models.URLField(null=True, blank=True, help_text="Φόρμα πρόσληψης.")

    # social media
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    tiktok = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    subgroup_label = models.CharField(max_length=30, choices=SUBGROUP_LABEL_CHOICES, default=SUBGROUP_LABEL_CHOICES[0], help_text="Το συγκεκριμένο chapter έχει Subgroups ή Projects;")
    page_color = models.CharField(default='00629A', max_length=8, help_text="Theme color του chapter.")


    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        self.title = self.title.strip().title()

        self.slug = slugify(self.title)
        self.short_title = self.short_title.strip().upper()

        self.greek_body = remove_emoji_img_tags(emoji_pattern(r'', sanitize_html(self.greek_body).strip()))
        if self.english_body:
            self.english_body = remove_emoji_img_tags(emoji_pattern(r'', sanitize_html(self.english_body).strip()))

        self.page_color = self.page_color.strip()

        name_of_thumbnail = str(self.slug)
        if os.path.basename(self.logo.name) != name_of_thumbnail + ".png":
            self.logo = compress_society_logo(self.logo, 560, name_of_thumbnail)
        if os.path.basename(self.hero_image.name) != name_of_thumbnail + '-background.jpg':
            self.hero_image = compress_background_hero(self.hero_image, 2400, name_of_thumbnail)
        super(Society, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Societies'
        indexes = [
            models.Index(fields=['slug',]),
        ]




class SubGroup(models.Model):

    MAX_BODY_CHARS = 379
    def get_image_path(instance, filename):
        return os.path.join('media', 'subgroup', instance.society.slug, slugify(instance.title, allow_unicode=True), filename)    

    title           = models.CharField(max_length=150)
    thumbnail       = models.ImageField(upload_to=get_image_path, max_length=350, storage=OverwriteStorage, help_text="Η εικόνα που θα ανεβάσετε ΔΕΝ πρέπει να έχει το ίδιο όνομα με αυτή που είναι ανεβασμένη (αν υπάρχει ανεβασμένη εικόνα).")
    greek_body      = models.TextField(max_length=MAX_BODY_CHARS, help_text=f"{MAX_BODY_CHARS} characters maximum.")
    english_body    = models.TextField(max_length=MAX_BODY_CHARS, help_text=f"{MAX_BODY_CHARS} characters maximum.")
    society         = models.ForeignKey(Society, on_delete = models.CASCADE)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        self.title = self.title.strip().title()
        self.greek_body = capitalize_first_character(self.greek_body.strip())
        self.english_body = capitalize_first_character(self.english_body.strip())

        name_of_thumbnail = str(slugify(self.title))
        if os.path.basename(self.thumbnail.name) != name_of_thumbnail + ".jpg":
            self.thumbnail = compress_event_thumbnail(self.thumbnail, 560, name_of_thumbnail)
        super(SubGroup, self).save(*args, **kwargs)

    # Unique together constraint validation error
    def clean(self):
        # Check if another object exists with the same values for field1 and field2
        self.title = self.title.strip().title()
        existing_obj = SubGroup.objects.filter(title=self.title, society=self.society).exclude(pk=self.pk).first()
        if existing_obj is not None:
            # Raise a validation error if there is a match
            raise ValidationError("A record with these values already exists.")
        super().clean()

    class Meta:
        verbose_name_plural = 'SubGroups'
        unique_together = ['title', 'society']

import shutil
@receiver(models.signals.post_delete, sender=Society)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image file from filesystem
    when corresponding `MyModel` object is deleted.
    """
    if instance.hero_image:
        if os.path.isfile(instance.hero_image.path):
            os.remove(instance.hero_image.path)
        if os.path.exists(os.path.dirname(instance.hero_image.path)):
            # os.rmdir(os.path.dirname(instance.hero_image.path))
            shutil.rmtree(os.path.dirname(instance.hero_image.path), ignore_errors=True)

    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)
        if os.path.exists(os.path.dirname(instance.logo.path)):
            shutil.rmtree(os.path.dirname(instance.logo.path), ignore_errors=True)
            # os.rmdir(os.path.dirname(instance.logo.path))

@receiver(models.signals.post_delete, sender=SubGroup)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes image file from filesystem
    when corresponding `MyModel` object is deleted.
    """
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)
        if os.path.exists(os.path.dirname(instance.thumbnail.path)):
            shutil.rmtree(os.path.dirname(instance.thumbnail.path), ignore_errors=True)
            # os.rmdir(os.path.dirname(instance.thumbnail.path))