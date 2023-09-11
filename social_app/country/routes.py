from flask import jsonify

from social_app.models.country import Country
from social_app.country import country_bp


@country_bp.get('/countries')
def get_countries():
    countries = Country.query.all()
    countries_data = [{'name': country.name, 'code': country.code} for country in countries]
    return jsonify(countries_data)
