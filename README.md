# Gestor de Contraseñas en Flask 🔐

Este es un proyecto personal desarrollado con Flask, enfocado en aprender sobre criptografía, seguridad informática y manejo seguro de contraseñas.
Se puede ver en: https://passadmin.onrender.com/
Ya que es la versión gratuita algunas peticiones pueden demorar hasta 50 segundos ya que el servidor se cae por inactividad.

## 🚀 Tecnologías utilizadas

- Python
- Flask
- Flask-Login
- Flask-Bcrypt
- SQLAlchemy (SQLite)
- `python-dotenv`
- AES + Argon2 para cifrado

## ⚙️ Requisitos

- Python 3.10+
- pip
- virtualenv (opcional, pero recomendado)

## 📦 Instalación

```bash
git clone https://github.com/tu_usuario/gestor-passwords.git
cd gestor-passwords
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r requirements.txt
```
Usa un archivo .env como este:
```
SECRET_KEY=clave_secreta
DATABASE_URL=sqlite:///database.db
```

