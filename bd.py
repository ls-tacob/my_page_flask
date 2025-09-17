import pymysql
import logging
from pymysql.cursors import DictCursor

def obtener_conexion():
    try:
        conexion = pymysql.connect(
            host='localhost',
            user='root',
            password='Le0messi10%',
            db='batson_cia_ltda',  # sin @ para evitar conflictos
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        logging.info("Conexión exitosa a la base de datos.")
        return conexion
    except pymysql.MySQLError as e:
        logging.error(f"Error al conectar con la base de datos: {e}")
        return None