"""
Uploads images with thumbnails if requested.
"""

import os

from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile


class ThumbnailImageFieldFile(ImageFieldFile):
    def __init__(self, *args, **kwargs):
        super(ThumbnailImageFieldFile, self).__init__(*args, **kwargs)
        self.sizes = self.field.sizes
        
        if self.sizes:
            name_split = self.url.rsplit('.', 1)
            for w, h in self.sizes:
                attr_name = "url_%sx%s" % (w, h)
                attr_value = "%s_%sx%s.%s" % (name_split[0], w, h, name_split[1])
                setattr(self, attr_name, attr_value)
    
    def save(self, name, content, save=True):
        super(ThumbnailImageFieldFile, self).save(name, content, save)
        if self.sizes:
            name_split = self.name.rsplit('.', 1)
            for w, h in self.sizes:
                thumb_name = "%s_%sx%s.%s" % (name_split[0], w, h, name_split[1])
                thumb_name_ = self.storage.save(thumb_name, content)
                if not thumb_name == thumb_name_:
                    raise ValueError('File already exists with the same name `%s`.' % thumb_name)
                self_path = self.storage.path(self.name)
                thumb_path = self.storage.path(thumb_name)
                dim = "%sx%s" % (w, h)
                cmd = 'convert %s -resize %s\> -size %s xc:white +swap -gravity center -composite %s' % (self_path, dim, dim, thumb_path)
                os.system(cmd)
    
    def delete(self, save=True):
        super(ThumbnailImageFieldFile, self).delete(save)
        if self.sizes:
            name_split = self.name.rsplit('.', 1)
            for w, h in self.sizes:
                file_name = "%s_%sx%s.%s" % (name_split[0], w, h, name_split[1])
                try:
                    self.storage.delete(file_name)
                except:
                    pass


class ThumbnailImageField(ImageField):
    attr_class = ThumbnailImageFieldFile
    
    def __init__(self, sizes=None, **kwargs):
        super(ThumbnailImageField, self).__init__(**kwargs)
        self.sizes = sizes
