from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
import os

app = FastAPI()

# Permitir conexión desde tu HTML con Live Server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://TU-PAGINA.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Datos que recibe desde JavaScript
class LoginRequest(BaseModel):
    usuario: str
    password: str


# Conexión a MySQL
def conectar_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        port=int(os.getenv("MYSQLPORT")),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE")
    )


@app.get("/")
def inicio():
    return {"mensaje": "Servidor FastAPI funcionando correctamente"}


@app.post("/login")
def login(datos: LoginRequest):

    try:
        conexion = conectar_db()
        cursor = conexion.cursor(dictionary=True)

        consulta = """
            SELECT id, usuario, rol
            FROM usuarios
            WHERE usuario = %s
            AND password = %s
            AND estado = 1
            LIMIT 1
        """

        cursor.execute(consulta, (datos.usuario, datos.password))
        usuario = cursor.fetchone()

        cursor.close()
        conexion.close()

        if usuario:
            return {
                "ok": True,
                "mensaje": "Login correcto",
                "id": usuario["id"],
                "usuario": usuario["usuario"],
                "rol": usuario["rol"]
            }

        return {
            "ok": False,
            "mensaje": "Usuario o contraseña incorrectos"
        }

    except Exception as error:
        print("Error en login:", error)

        return {
            "ok": False,
            "mensaje": "Error de conexión con la base de datos"
        }