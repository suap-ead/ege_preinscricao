from django.db import models

class AnoConclusao(models.Model):
  suap_id = models.IntegerField()
  titulo = models.CharField(max_length=4)
  
  def __str__(self):
    return self.titulo