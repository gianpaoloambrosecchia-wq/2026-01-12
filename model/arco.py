from dataclasses import dataclass

from model.Constructor import Constructor


@dataclass
class Arco:
    c1: Constructor
    c2: Constructor
    peso: int

    def __hash__(self):
        return hash((self.c1,self.c2))

    def __eq__(self, other):
        return self.c1 == other.c1 and self.c2 == other.c2

    def __str__(self):
        return f"{self.c1.name} --> {self.c2.name} ({self.peso} piloti condivisi)"




