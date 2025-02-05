class Owner:
    def __init__(self, name: str, email: str, password: str, phone: str, plan_id: int, id: int = None):
        self.id = id  # Se asignará cuando se guarde en la DB
        self.name = name
        self.email = email
        self.password = password  # Encriptado
        self.phone = phone
        self.plan_id = plan_id
