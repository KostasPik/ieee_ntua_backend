from django.db import models
from PIL import Image
from io import BytesIO
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.files.uploadedfile import InMemoryUploadedFile
from backend.storages import OverwriteStorage
import os
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from backend.utils import remove_html_tags, capitalize_first_character, sanitize_html, emoji_pattern, remove_emoji_img_tags
import html
from django.dispatch import receiver
import shutil
# Create your models here.


def compress_news_thumbnail(thumbnail, width_specified, image_name):
    image = Image.open(thumbnail).convert("RGBA")
    temp_image = Image.new("RGBA", image.size, "WHITE")
    temp_image.paste(image,(0,0) ,mask=image)
    output_io_stream = BytesIO()
    width, height = temp_image.size
    aspect_ration = width / height
    final_image = temp_image.resize((width_specified, int(width_specified/aspect_ration)))
    final_image = final_image.convert('RGB')
    final_image.save(output_io_stream, format='JPEG', optimize=True, quality=60)
    # final_image.save(output_io_stream, format='webp')
    output_io_stream.seek(0)
    if width_specified > 1000:
        thumbnail = InMemoryUploadedFile(output_io_stream, None,image_name+".jpg", 'image/jpeg', output_io_stream.tell(), None)
    elif width_specified < 1000:
        thumbnail = InMemoryUploadedFile(output_io_stream, None, image_name+"-mobile.jpg", 'image/jpeg', output_io_stream.tell(), None)
    return thumbnail




class News(models.Model):
    
    def get_image_path(instance, filename):
        return os.path.join('media', 'news', slugify(instance.greek_title, allow_unicode=True), filename)

    english_version = models.BooleanField(default=False, help_text="Εαν υπάρχει έκδοση στα αγγλικά, ενεργοποιήστε το.")
    greek_title = models.CharField(max_length=200, unique=True, help_text="Τίτλος του article στα Ελληνικά.")
    english_title = models.CharField(max_length=200, blank=True, null=True, help_text="Τίτλος του article στα Αγγλικά.")
    greek_slug = models.SlugField(max_length=200, allow_unicode=True)
    english_slug = models.SlugField(max_length=200, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=get_image_path, max_length=450, storage=OverwriteStorage, help_text="Η εικόνα που θα ανεβάσετε ΔΕΝ πρέπει να έχει το ίδιο όνομα με αυτή που είναι ανεβασμένη (αν υπάρχει ανεβασμένη εικόνα).")
    greek_body = RichTextUploadingField(max_length=55000)
    english_body = RichTextUploadingField(max_length=55000, blank=True, null=True, help_text="Η έκδοση του κειμένου στην Αγγλική γλώσσα (έαν υπάρχει αγγλική έκδοση του κειμένου).")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.greek_title

    def save(self, *args, **kwargs):

        self.greek_title = capitalize_first_character(self.greek_title.strip())
       
        if self.english_title:
            self.english_title = capitalize_first_character(self.english_title.strip())
        
        self.greek_body = remove_emoji_img_tags(emoji_pattern(r'', sanitize_html(self.greek_body).strip()))

        if self.english_body:
            self.english_body = remove_emoji_img_tags(emoji_pattern(r'', sanitize_html(self.english_body).strip()))

        self.english_slug = slugify(self.english_title) 
        self.greek_slug = slugify(self.greek_title, allow_unicode=True)

        name_of_thumbnail = str(self.greek_slug)

        if os.path.basename(self.thumbnail.name) != name_of_thumbnail+".jpg":
            self.thumbnail = compress_news_thumbnail(self.thumbnail, 1500, name_of_thumbnail)
        super(News, self).save(*args, **kwargs)


    def clean(self):
        if self.english_version:
            if not self.english_title or (self.english_title and not self.english_title.strip()):
                raise ValidationError("English title is required since english_version field is activated!")
            if not self.english_body or (self.english_body and not remove_html_tags(html.unescape(self.english_body)).strip()):
                raise ValidationError("English Body is required since english_version field is activated!")
        super().clean()

    class Meta:
        verbose_name_plural = 'News'
        indexes = [
            models.Index(fields=['english_version', 'created_at']),
            models.Index(fields=['greek_slug']),
            models.Index(fields=['english_version', 'english_slug']),
        ]


@receiver(models.signals.post_delete, sender=News)
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