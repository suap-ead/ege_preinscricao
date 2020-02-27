from django.db import models
# from .modelos.candidato import Candidato
# from .modelos.nacionalidade import Nacionalidade
# from .modelos.genero import Genero


# class Candidato(models.Model):
#     nome = models.CharField(max_length=350)
#     email = models.CharField(max_length=200)
#     cpf = models.CharField(max_length=14)
#     nacionalidade = models.ForeignKey(Nacionalidade, on_delete=models.CASCADE, default=1)
#     genero = models.ForeignKey(Genero, on_delete=models.CASCADE, default=1)
    
#     def __str__(self):
#         return self.nome

# Create your models here.


# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)


# from .modelos import Nacionalidade
# from .modelos import Genero
    
# class Candidato(models.Model):
#   nome = models.CharField(max_length=350)
#   email = models.CharField(max_length=200)
#   cpf = models.CharField(max_length=14)
#   # nacionalidade = models.ForeignKey(Nacionalidade, on_delete=models.CASCADE, default=1)
#   # genero = models.ForeignKey(Genero, on_delete=models.CASCADE, default=1)
  
#   def __str__(self):
#       return self.nome