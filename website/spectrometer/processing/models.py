from django.db import models
from PIL import Image

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class SpectralImage(models.Model):
    # docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    tag = models.CharField(max_length=255)
    source = models.ImageField(upload_to='documents/%Y/%m/%d')

    def save(self, size=(300, 100)):
       """
       Save Photo after ensuring it is not blank.  Resize as needed.
       """

       if not self.id and not self.source:            
       	 return

       super(SpectralImage, self).save()

       filename = self.source.path
       image = Image.open(filename)
       image = image.crop((230, 140, 610, 240))#image.crop((110, 240, 500, 300))(left, upper, right, lower)
       image = image.resize((300,100), Image.ANTIALIAS)
    
       image.save(filename)