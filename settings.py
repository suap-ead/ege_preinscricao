import os
from sc4py.env import env, env_as_bool
URL_PATH_PREFIX = env("URL_PATH_PREFIX", "sead/pre_matricula/")
os.environ.setdefault("URL_PATH_PREFIX", env("", "sead/pre_matricula/"))
os.environ.setdefault("MY_APPS", "solicitacao,dominio_suap,import_export")
os.environ.setdefault("POSTGRES_DB", env("POSTGRES_DB_PRE_MATRICULA", "sead_pre_matricula"))
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env("DJANGO_EMAIL_HOST", None)
EMAIL_PORT = env("DJANGO_EMAIL_PORT", None)
EMAIL_HOST_USER = env("DJANGO_EMAIL_HOST_USER", None)
EMAIL_HOST_PASSWORD = env("DJANGO_EMAIL_HOST_PASSWORD", None)
EMAIL_USE_TLS = env_as_bool("DJANGO_EMAIL_USE_TLS", None)
EMAIL_USE_SSL = env_as_bool("DJANGO_EMAIL_USE_SSL", None)

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
