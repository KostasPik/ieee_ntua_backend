from django.db import models
from PIL import Image
from io import BytesIO
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.files.uploadedfile import InMemoryUploadedFile
from backend.storages import OverwriteStorage
import os
from django.utils.text import slugify
from society.models import Society
# from backend.utils import validate_no_at_symbol
from django.core.exceptions import ValidationError
from backend.utils import remove_html_tags, capitalize_first_character
import html
from backend.utils import sanitize_html, emoji_pattern, remove_emoji_img_tags
from django.dispatch import receiver
# Create your models here.


def compress_event_thumbnail(thumbnail, width_specified, image_name):
    temp_image = Image.open(thumbnail)
    output_io_stream = BytesIO()
    width, height = temp_image.size
    aspect_ration = width / height
    final_image = temp_image.resize((width_specified, int(width_specified/aspect_ration)))
    final_image = final_image.convert('RGB')
    final_image.save(output_io_stream, format='JPEG', optimize=True)
    # final_image.save(output_io_stream, format='webp')
    output_io_stream.seek(0)
    if width_specified > 1000:
        thumbnail = InMemoryUploadedFile(output_io_stream, None,image_name+".jpg", 'image/jpeg', output_io_stream.tell(), None)
    elif width_specified < 1000:
        thumbnail = InMemoryUploadedFile(output_io_stream, None, image_name+"-mobile.jpg", 'image/jpeg', output_io_stream.tell(), None)
    return thumbnail




class Event(models.Model):

    def get_image_path(instance, filename):
        return os.path.join('media', 'event', slugify(instance.greek_title, allow_unicode=True), filename)

    english_version = models.BooleanField(default=False, help_text="Εαν έχει αγγλική έκδοση το Εvent ενεργοποίησε το.")
    greek_title = models.CharField(max_length=150, unique=True, help_text="Ελληνικός τίτλος του Event", primary_key=True)
    english_title = models.CharField(max_length=150, unique=True, help_text="Αγγλικός τίτλος του Event (εαν έχει αγγλική έκδοση)", blank=True, null=True)
    greek_slug = models.SlugField(max_length=150, unique=True, allow_unicode=True)
    english_slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=get_image_path, storage=OverwriteStorage, max_length=350, help_text="Η εικόνα που θα ανεβάσετε ΔΕΝ πρέπει να έχει το ίδιο όνομα με αυτή που είναι ανεβασμένη (αν υπάρχει ανεβασμένη εικόνα).")
    mobile_thumbnail = models.ImageField(upload_to=get_image_path,blank=True, null=True, max_length=350)
    societies = models.ManyToManyField(Society)
    greek_body = RichTextUploadingField(max_length=30000)
    english_body = RichTextUploadingField(max_length=30000, blank=True, null=True, help_text="Η έκδοση του κειμένου στην Αγγλική γλώσσα. (εαν υπάρχει αγγλική έκδοση του κειμένου)")
    greek_event_place = models.CharField(max_length=150, help_text="Το μέρος που θα γίνει το Event (στα Ελληνικά).")
    english_event_place = models.CharField(max_length=150, blank=True, null=True, help_text="Το μέρος που θα γίνει το Event στα Αγγλικά. Εάν δεν υπάρχει αγγλική έκδοση αφήστε κενό.")
    event_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.greek_title

    def save(self, *args, **kwargs):

        self.greek_title = capitalize_first_character(self.greek_title.strip())


        if self.english_title:
            self.english_title = capitalize_first_character(self.english_title.strip())

        self.greek_body = remove_emoji_img_tags(emoji_pattern.sub(r'', sanitize_html(self.greek_body).strip()))
        if self.english_body:
            self.english_body = remove_emoji_img_tags(emoji_pattern.sub(r'', sanitize_html(self.english_body).strip()))

        self.greek_event_place = capitalize_first_character(self.greek_event_place.strip())
        if self.english_event_place:
            self.english_event_place = capitalize_first_character(self.english_event_place.strip())



        self.english_slug = slugify(self.english_title)
        self.greek_slug = slugify(self.greek_title, allow_unicode=True)



        name_of_thumbnail = str(self.greek_slug)+'-image'
        if os.path.basename(self.thumbnail.name) != name_of_thumbnail+".jpg":
            self.thumbnail = compress_event_thumbnail(self.thumbnail, 1200, name_of_thumbnail)
            self.mobile_thumbnail = compress_event_thumbnail(self.thumbnail, 560, name_of_thumbnail)
        super(Event, self).save(*args, **kwargs)


    def clean(self):
        if self.english_version:
            if not self.english_title or (self.english_title and not self.english_title.strip()):
                raise ValidationError("English title is required since english_version field is activated!")
            if not self.english_body or (self.english_body and not remove_html_tags(html.unescape(self.english_body)).strip()):
                raise ValidationError("English Body is required since english_version field is activated!")
            if not self.english_event_place or (self.english_event_place and not self.english_event_place):
                raise ValidationError("English Event Place is required since english_version field is activated!")

        super().clean()

    class Meta:
        verbose_name_plural = 'Events'
        indexes = [
            models.Index(fields=['english_version','event_time']),
            models.Index(fields=['greek_slug',]),
            models.Index(fields=['english_version','english_slug']),
        ]

import shutil
@receiver(models.signals.post_delete, sender=Event)
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
    if instance.mobile_thumbnail:
        if os.path.isfile(instance.mobile_thumbnail.path):
            os.remove(instance.mobile_thumbnail.path)
        if os.path.exists(os.path.dirname(instance.mobile_thumbnail.path)):
            shutil.rmtree(os.path.dirname(instance.mobile_thumbnail.path), ignore_errors=True)
            # os.rmdir(os.path.dirname(instance.mobile_thumbnail.path))
