
import hashlib

class Hasher:
    @staticmethod
    def sha256(text: str) -> str:
        """
        Recibe un string y devuelve su hash SHA256 hexadecimal.
        """
        if not isinstance(text, str):
            raise ValueError("Input debe ser un string")
        encoded_text = text.encode("utf-8")
        hash_obj = hashlib.sha256(encoded_text)
        return hash_obj.hexdigest()

# hexdigest convierte el hash en una cadena de caracteres en formato hexadecimal, 
# que es más fácil de almacenar y mostrar que los bytes crudos.
# hashlib facilita la creación de hashes seguros en Python.
# sha256 es un algoritmo de hash que produce un hash de 256 bits.
# encode convierte el string en bytes, que es el formato requerido por el algoritmo de hash.
