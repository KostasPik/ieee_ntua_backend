from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os



class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system

        # path = os.path.join(settings.MEDIA_ROOT, os.path.join(name.split('/')[0:len(name.split('/'))-1]))
        path = os.path.join(settings.MEDIA_ROOT, os.path.split(name)[0])

        path_exists = os.path.exists(path)
        if not path_exists:
            return name

        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                os.remove(os.path.join(path, file))

        return name