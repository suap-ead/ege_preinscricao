from django.db import models

class Candidato(models.Model):
    nome = models.CharField(max_length=350)
    email = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14)

    def __str__(self):
        return self.nome
