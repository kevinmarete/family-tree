from flask import Flask

from data.pipeline import CsvPipeline
from src.models.person_model import Person
from src.services.family_service import FamilyService

app = Flask(__name__)
family_service = FamilyService()


def init_data():
    persons = CsvPipeline("data/people.csv").extract().transform().load()
    relations = CsvPipeline("data/relations.csv").extract().transform().load()

    for person in persons:
        new_person = Person(person["id_number"], person["name"], person["date_of_birth"], person["sex"])
        family_service.add_member(new_person)

    for relation in relations:
        child_member = family_service.get_member(relation["child_id"])
        parent_member = family_service.get_member(relation["parent_id"])

        child_member.add_parent(parent_member)
        parent_member.add_child(child_member)


@app.route('/')
def welcome():
    return "Welcome to Family Tree Service"


@app.route('/tree/<member_id>')
def get_tree(member_id):
    init_data()
    member = family_service.get_member(member_id)
    return {
        "info": {"id": member.id_number, "name": member.name},
        "relationships": {
            "GrandParents": [member.name for member in family_service.get_grand_parents(member_id)],
            "Parents": [member.name for member in family_service.get_parents(member_id)],
            "Siblings": [member.name for member in family_service.get_siblings(member_id)],
            "Uncles": [member.name for member in family_service.get_uncles(member_id)],
            "Aunts": [member.name for member in family_service.get_aunts(member_id)],
            "Cousins": [member.name for member in family_service.get_cousins(member_id)],
            "Ancestors": [member.name for member in family_service.get_ancestors(member_id)]
        }
    }


if __name__ == '__main__':
    app.run()
