from django.db import models

class Nacionalidade(models.Model):
  suap_id = models.IntegerField()
  titulo = models.CharField(max_length=200)
  apelido = models.CharField(max_length=200)

  def __str__(self):
    return self.titulo