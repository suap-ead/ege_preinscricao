import os
from sc4py.env import env
URL_PATH_PREFIX = env("URL_PATH_PREFIX", "pre_matricula/")
os.environ.setdefault("URL_PATH_PREFIX", env("", "pre_matricula/"))
os.environ.setdefault("MY_APPS", "solicitacao,dominio_suap")
os.environ.setdefault("POSTGRES_DB", env("POSTGRES_DB_PRE_MATRICULA", "sead_pre_matricula"))
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
os.environ.setdefault("MIDDLEWARE", 
                      env("MIDDLEWARE", 
                          'django.middleware.security.SecurityMiddleware,'
                          'django.contrib.sessions.middleware.SessionMiddleware,'
                          'django.middleware.common.CommonMiddleware,'
                          'django.middleware.csrf.CsrfViewMiddleware,'
                          'solicitacao.middlewares.SelecionadoMiddleware,'
                          'django.contrib.auth.middleware.AuthenticationMiddleware,'
                          'django.contrib.messages.middleware.MessageMiddleware,'
                          'django.middleware.clickjacking.XFrameOptionsMiddleware'))
from suap_ead.template_settings import *
