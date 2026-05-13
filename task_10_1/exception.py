class CustomExceptionA(Exception):
    """Исключение для случаев, когда не выполняется бизнес-условие"""
    def __init__(self, message: str = "Нарушено бизнес-правило"):
        self.message = message
        self.status_code = 400


class CustomExceptionB(Exception):
    """Исключение для случаев, когда ресурс не найден"""
    def __init__(self, resource_name: str = "Ресурс"):
        self.message = f"{resource_name} не найден"
        self.status_code = 404