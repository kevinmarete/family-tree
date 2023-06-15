import datetime

from src.models.sex_model import Sex


class Person:
    def __init__(self, id_number: str, name: str, date_of_birth: datetime.date, sex: Sex):
        self.id_number: str = id_number
        self.name: str = name
        self.date_of_birth: datetime.date = date_of_birth
        self.sex: Sex = sex
        self.parents: dict = {}
        self.partners: dict = {}
        self.children: dict = {}

    def add_parent(self, parent):
        self.parents[parent.id_number] = parent

    def add_partner(self, partner):
        self.partners[partner.id_number] = partner

    def add_child(self, child):
        self.children[child.id_number] = child

    def get_parents(self) -> list:
        return list(self.parents.values())

    def get_partners(self) -> list:
        return list(self.partners.values())

    def get_children(self) -> list:
        return list(self.children.values())
