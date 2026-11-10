"""
Manejo de contraseñas.

ESTADO ACTUAL: texto plano (para probar que todo funciona).

PARA ACTIVAR EL HASH:
  1) Descomenta el bloque "HASH".
  2) Comenta o borra el bloque "TEXTO PLANO".
  3) Los usuarios guardados con texto plano dejarán de poder entrar:
     hay que volver a crearlos o cambiarles la contraseña desde el módulo
     Usuarios (el hash ocupa ~97 caracteres, cabe en VARCHAR(255)).

Login.py y ModUsuario.py solo usan encriptar() y verificar(),
así que este es el único archivo que hay que tocar.
"""

# ============================================================
# BLOQUE "HASH"  ->  DESCOMENTAR PARA ACTIVAR
# ============================================================
# import hashlib
# import hmac
# import os
#
#
# def encriptar(password):
#     """Devuelve 'salt$hash' (salt aleatorio distinto por usuario)."""
#     salt = os.urandom(16)
#     digest = hashlib.pbkdf2_hmac(
#         "sha256", password.encode("utf-8"), salt, 100_000
#     )
#     return salt.hex() + "$" + digest.hex()
#
#
# def verificar(password, guardado):
#     """True si la contraseña escrita coincide con la guardada."""
#     try:
#         salt_hex, hash_hex = guardado.split("$")
#         digest = hashlib.pbkdf2_hmac(
#             "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), 100_000
#         )
#     except (ValueError, AttributeError):
#         return False
#     return hmac.compare_digest(digest.hex(), hash_hex)


# ============================================================
# BLOQUE "TEXTO PLANO"  ->  COMENTAR O BORRAR AL ACTIVAR EL HASH
# ============================================================
def encriptar(password):
    return password
