"""
Uploads images with thumbnails if requested.
"""

from os import path
from os import system as cmd
from decimal import Decimal
from django.conf import settings
from django.db.models import ImageField, DecimalField, SubfieldBase
from django.db.models.fields.files import ImageFieldFile


class ThumbnailedImageFieldFile(ImageFieldFile):
    def __init__(self, *args, **kwargs):
        super(ThumbnailedImageFieldFile, self).__init__(*args, **kwargs)
        
        self.thumb_size = self.field.thumb_size
        self.watermark = self.field.watermark
        
        parts = tuple(self.url.rsplit('.', 1))
        
        if self.thumb_size:
            setattr(self, 'url_thumb', '%s_thumb.%s' % parts)
            
        if self.watermark:
            setattr(self, 'url_collected', '%s_collected.%s' % parts)
    
    def save(self, name, content, save=True):
        super(ThumbnailedImageFieldFile, self).save(name, content, save)
        
        if not self.thumb_size:
            return
        
        parts = tuple(self.name.rsplit('.', 1))
            
        thumb_name = '%s_thumb.%s' % parts
        if not thumb_name == self.storage.save(thumb_name, content):
            raise ValueError('Thumbnail file already exists with the same name `%s`.' % thumb_name)

        print(self.name)
        image_path = self.storage.path(self.name)
        print(image_path)
        print(thumb_name)
        thumb_path = self.storage.path(thumb_name)
        print(thumb_path)
        
        size = '%dx%d' % self.thumb_size
        
        cmd('convert %s -resize %s\> -size %s xc:white +swap -gravity center -composite %s'
                  % (image_path, size, size, thumb_path))
        
        if not self.watermark:
            return
        
        collected_name = '%s_collected.%s' % parts
        if not collected_name == self.storage.save(collected_name, content):
            raise ValueError('Watermarked file already exists with the same name `%s`.' % collected_name)
        
        collected_path = self.storage.path(collected_name)
        watermark_path = path.join(settings.STATIC_ROOT, self.watermark)
        
        cmd('composite -gravity center %s %s %s' % (watermark_path, thumb_path, collected_path))
    
    def delete(self, save=True):
        super(ThumbnailedImageFieldFile, self).delete(save)
        
        parts = self.name.rsplit('.', 1)
        for middle in ['thumb', 'collected']:
            file_name = "%s_%s.%s" % (parts[0], middle, parts[1])
            try:
                self.storage.delete(file_name)
            except:
                pass


class ThumbnailedImageField(ImageField):
    attr_class = ThumbnailedImageFieldFile
    
    def __init__(self, thumb_size=(100,100), watermark=None, **kwargs):
        super(ThumbnailedImageField, self).__init__(**kwargs)
        self.thumb_size = thumb_size
        self.watermark = watermark


class CurrencyField(DecimalField):
    __metaclass__ = SubfieldBase
    
    def to_python(self, value):
        try:
            return super(CurrencyField, self).to_python(value).quantize(Decimal('0.01'))
        except AttributeError:
            return None
