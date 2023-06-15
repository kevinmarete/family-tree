import json

from src.models.person_model import Person
from src.models.sex_model import Sex
from src.utils.list_utils import get_flat_list


class FamilyService:
    def __init__(self):
        self.members: dict = {}

    def add_member(self, member: Person) -> None:
        self.members[member.id_number] = member

    def remove_member(self, member: Person) -> None:
        self.members.pop(member.id_number)

    def get_member(self, member_id: str) -> Person:
        return self.members.get(member_id)

    def get_members(self) -> list[Person]:
        return list(self.members.values())

    def get_parents(self, member_id: str) -> list[Person]:
        return self.get_member(member_id).get_parents()

    def get_fathers(self, member_id: str) -> list[Person]:
        return [parent for parent in self.get_parents(member_id) if parent.sex == Sex.MALE.value]

    def get_mothers(self, member_id: str) -> list[Person]:
        return [parent for parent in self.get_parents(member_id) if parent.sex == Sex.FEMALE.value]

    def get_partners(self, member_id: str) -> list[Person]:
        return self.get_member(member_id).get_partners()

    def get_children(self, member_id: str) -> list[Person]:
        return self.get_member(member_id).get_children()

    def get_sons(self, member_id: str) -> list[Person]:
        return [child for child in self.get_children(member_id) if child.sex == Sex.MALE.value]

    def get_daughters(self, member_id: str) -> list[Person]:
        return [child for child in self.get_children(member_id) if child.sex == Sex.FEMALE.value]

    def get_siblings(self, member_id: str) -> list[Person]:
        children = get_flat_list([self.get_children(parent.id_number) for parent in self.get_parents(member_id)])
        return [child for child in children if child.id_number != member_id]

    def get_brothers(self, member_id: str) -> list[Person]:
        return [sibling for sibling in self.get_siblings(member_id) if sibling.sex == Sex.MALE.value]

    def get_sisters(self, member_id: str) -> list[Person]:
        return [sibling for sibling in self.get_siblings(member_id) if sibling.sex == Sex.FEMALE.value]

    def get_grand_parents(self, member_id: str) -> list[Person]:
        return get_flat_list([self.get_parents(parent.id_number) for parent in self.get_parents(member_id)])

    def get_grandfathers(self, member_id: str) -> list[Person]:
        return [grand_parent for grand_parent in self.get_grand_parents(member_id) if
                grand_parent.sex == Sex.MALE.value]

    def get_grandmothers(self, member_id: str) -> list[Person]:
        return [grand_parent for grand_parent in self.get_grand_parents(member_id) if
                grand_parent.sex == Sex.FEMALE.value]

    def get_parent_siblings(self, member_id: str) -> list[Person]:
        return get_flat_list([self.get_siblings(parent.id_number) for parent in self.get_parents(member_id)])

    def get_uncles(self, member_id: str) -> list[Person]:
        return [parent_sibling for parent_sibling in self.get_parent_siblings(member_id) if
                parent_sibling.sex == Sex.MALE.value]

    def get_aunts(self, member_id: str) -> list[Person]:
        return [parent_sibling for parent_sibling in self.get_parent_siblings(member_id) if
                parent_sibling.sex == Sex.FEMALE.value]

    def get_cousins(self, member_id) -> list[Person]:
        return get_flat_list(
            [self.get_children(parent_sibling.id_number) for parent_sibling in self.get_parent_siblings(member_id)])

    def get_ancestors(self, member_id, ancestors=None):
        if ancestors is None:
            ancestors = []
        parents = self.get_parents(member_id)
        if parents:
            ancestors = parents
            return get_flat_list([self.get_ancestors(ancestor.id_number, ancestors) for ancestor in ancestors])
        return ancestors

    def get_relations(self, member_id):
        return {
            "GrandParents": [member.name for member in self.get_grand_parents(member_id)],
            "Parents": [member.name for member in self.get_parents(member_id)],
            "Siblings": [member.name for member in self.get_siblings(member_id)],
            "Partners": [member.name for member in self.get_partners(member_id)],
            "Uncles": [member.name for member in self.get_uncles(member_id)],
            "Aunts": [member.name for member in self.get_aunts(member_id)],
            "Cousins": [member.name for member in self.get_cousins(member_id)],
            "Ancestors": [member.name for member in self.get_ancestors(member_id)]
        }

    def get_family(self, member_id):
        member = self.get_member(member_id)
        unprocessed_members = [member]
        family = {}

        while unprocessed_members:
            member = unprocessed_members.pop()
            if member.id_number in family:
                continue

            family[member.id_number] = {
                "id": member.id_number,
                "name": member.name,
                "dob": member.date_of_birth,
                "gender": str(member.sex).lower()
            }

            fathers = self.get_fathers(member.id_number)
            mothers = self.get_mothers(member.id_number)
            partners = self.get_partners(member.id_number)
            children = self.get_children(member.id_number)

            if fathers:
                father = next(iter(fathers))
                family[member.id_number]["fid"] = father.id_number
                unprocessed_members.append(father)
            if mothers:
                mother = next(iter(mothers))
                family[member.id_number]["mid"] = mother.id_number
                unprocessed_members.append(mother)
            if partners:
                unprocessed_members.extend(partners)
                family[member.id_number]["pids"] = [partners.id_number for partners in partners]
            if children:
                unprocessed_members.extend(children)

        return family
