class Owner:
    def __init__(self, id: int, name: str, email: str, password: str, plan_id: int):
        self.id = id
        self.name = name
        self.email = email
        self.password = password  #encriptado
        self.plan_id = plan_id
