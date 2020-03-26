#!/usr/bin/python

import sys
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

con = psycopg2.connect(dbname='postgres', user=sys.argv[2], host='db', password=sys.argv[3])
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()
cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(sys.argv[1])))