

class Memory:
    def __init__(self):

        self.data = {}

    def save(self,
             key: str,
             value:str):
        self.data[key] = value

    def load(self,key:str):
        return self.data.get(key)


    def get_all(self) -> dict:
        return self.data
