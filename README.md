# ege_preinscricao

# Fases
 1. Processo seletivo
    1. Inscrição (online)
    2. Seleção (online)
2. Pré-matricula
   1. Cadastro (online)
   2. Homologação (avalidor)
   3. Autenticação (presencial)
3. Matricula
   1. Cadastro (SUAP)
   2. Criação da pasta do aluno (física)
   3. Criação de process0 da pasta do aluno (SUAP)

# Ambiente de DEV
## Usando Docker
```
docker-compose build
docker-compose up
```

## Criando banco de dados
```
docker-compose exec web sh database_create.sh
```
Usuário: admin@example.com
Senha: admin

## Atualizando banco de dados e migrações
```
docker-compose exec web sh database_update.sh
```