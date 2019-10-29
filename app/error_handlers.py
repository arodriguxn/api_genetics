from flask import jsonify

class InvalidData(Exception):
    """Implementación de una excepción Flask.

    Devuelve el código HTTP de error y un mensaje informando de tal error.
    Por defecto, el error es 400.

    Parameters
    ----------
    message: str
        mensaje de error
    status_code: int
        código HTTP de error
    payload: json
        cualquier información extra

    Attributes
    ----------
    message: str
        mensaje de error
    status_code: int
        código HTTP de error
    payload: json
        cualquier información extra
    """ 

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Convierte a un diccionario el contenido de la excepción

        Returns
        -------
        dict
            la información convertida
        """
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv
