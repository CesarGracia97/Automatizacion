import redis

class Redis_Configuration:
    def __init__(self, host='localhost', port=6379, db=0, password=None):
        """
        Inicializa la configuración de Redis.

        Parámetros:
        - host (str): Dirección del servidor Redis (por defecto 'localhost').
        - port (int): Puerto del servidor Redis (por defecto 6379).
        - db (int): Número de la base de datos Redis (por defecto 0).
        - password (str): Contraseña para Redis si es necesaria (por defecto None).
        """
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.connection = None

    def connect(self):
        """
        Establece la conexión con Redis y devuelve la instancia de conexión.
        """
        try:
            self.connection = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                decode_responses=True  # Decodificar respuestas a strings en lugar de bytes
            )
            # Verificar si la conexión es exitosa
            if self.connection.ping():
                print("Conexión a Redis exitosa.")
                return self.connection
        except redis.ConnectionError as e:
            print(f"Error al conectar con Redis: {e}")
            self.connection = None
            return None

    def disconnect(self):
        """
        Cierra la conexión con Redis.
        """
        if self.connection:
            self.connection.close()
            print("Conexión a Redis cerrada.")
            self.connection = None
        else:
            print("No hay una conexión activa con Redis para cerrar.")