class ExceptionTemplate():
    def __init__(self, type, messages, template, generated=False):
        self.type = type
        self.messages = messages
        self.template = template
        self.generated = generated

        self.messages.sort()

    def __str__(self):
        return f"{self.type}: {self.template}"

    def __repr__(self):
        return self.__str__()