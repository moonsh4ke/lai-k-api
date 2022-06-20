class Usuario():
    """
    @id = id del usuario, autoincremento
    @nom = nombre del usuario
    @apell = apellido del usuario
    @com = id de la comuna
    @calle = nombre de la calle
    @num = numero de la casa
    @tel = numero de telefono
    @email = direccion de correo
    @tu = tipo de usuario
    @espec = especialidad
    """
    def __init__(self,nom,apell,com,calle,num,tel,email,tu):
        self.nombres = nom
        self.apellidos = apell
        self.comuna = com
        self.calle = calle,
        self.numero = num
        self.telefono = tel
        self.email = email
        self.tipo_usuario = tu
    
