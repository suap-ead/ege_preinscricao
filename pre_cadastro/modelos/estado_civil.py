from django.db import models

class EstadoCivil(models.Model):
	suap_id = models.IntegerField()
	titulo = models.CharField(max_length=100)
	apelido = models.CharField(max_length=100)
	
	def __str__(self):
		return self.titulo