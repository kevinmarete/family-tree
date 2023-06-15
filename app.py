import json

from flask import Flask, render_template

from data.pipeline import CsvPipeline
from src.models.person_model import Person
from src.services.family_service import FamilyService

app = Flask(__name__)
family_service = FamilyService()


def init_data():
    persons = CsvPipeline("data/people.csv").extract().transform().load()
    parent_relations = CsvPipeline("data/parent_relations.csv").extract().transform().load()
    partner_relations = CsvPipeline("data/partner_relations.csv").extract().transform().load()

    for person in persons:
        new_person = Person(person["id_number"], person["name"], person["date_of_birth"], person["sex"])
        family_service.add_member(new_person)

    for parent_relation in parent_relations:
        child_member = family_service.get_member(parent_relation["child_id"])
        parent_member = family_service.get_member(parent_relation["parent_id"])

        child_member.add_parent(parent_member)
        parent_member.add_child(child_member)

    for partner_relation in partner_relations:
        person_member = family_service.get_member(partner_relation["person_id"])
        partner_member = family_service.get_member(partner_relation["partner_id"])

        person_member.add_partner(partner_member)
        partner_member.add_partner(person_member)


@app.route('/')
def welcome():
    init_data()
    return render_template('index.html', people=family_service.get_members())


@app.route('/tree/<member_id>')
def get_tree(member_id):
    init_data()
    return render_template('tree.html', tree=list(family_service.get_family(member_id).values()))


if __name__ == '__main__':
    app.run()
