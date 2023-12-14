class Degree():
        def __init__(self, Grado_ID, Grado, Universidad,  COD_UNI, Precio_anyo, Duracion,rama_academica_1):
            self._Grado_ID = Grado_ID
            self._Grado = Grado
            self._Universidad = Universidad
            self._COD_UNI = COD_UNI
            self._Precio_anyo = Precio_anyo
            self._Duracion = Duracion
            self._rama_academica_1 = rama_academica_1
            self._priority = 0
        
        def __str__(self):
            return  "----\n Grado_ID: " + self._Grado_ID + "\n" + "Grado: " + self._Grado + "\n" + "Universidad: " + self._Universidad + "\n" + "COD_UNI: " + "\n" + self._COD_UNI + "Precio anual: " + str(self._Precio_anyo) + "\n" + "Duración: " + str(self._Duracion) + " años \n---\n"
