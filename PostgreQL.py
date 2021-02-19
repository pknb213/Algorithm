"""
http://sanghun.xyz/2016/11/python%EC%97%90%EC%84%9C-postgres-db-%EC%97%B0%EA%B2%B0%ED%95%B4%EC%84%9C-%EC%BF%BC%EB%A6%AC-%EC%A1%B0%ED%9A%8C%ED%95%98%EA%B8%B0/
"""


import psycopg2 as pg2

conn = pg2.connect(database="test", user="postgres", password="1228", host="localhost", port="5432")
print(conn)

