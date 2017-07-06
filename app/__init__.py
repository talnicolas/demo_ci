# app/__init__.py

from flask import request, jsonify, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from app.domain import Datasource
    
    @app.route('/datasources/', methods=['POST', 'GET'])
    def datasources():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            driver = str(request.data.get('driver', ''))
            host = str(request.data.get('host', ''))
            port = str(request.data.get('port', ''))
            db = str(request.data.get('db', ''))
            if name:
                datasource = Datasource(name=name,driver=driver,host=host,port=port,db=db)
                datasource.save()
                response = jsonify({
                    'id': datasource.id,
                    'name': datasource.name,
                    'connection_string': datasource.connection_string,
                    'date_created': datasource.date_created,
                    'date_modified': datasource.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET
            datasources = Datasource.get_all()
            results = []

            for datasource in datasources:
                obj = {
                    'id': datasource.id,
                    'name': datasource.name,
                    'connection_string': datasource.connection_string,
                    'date_created': datasource.date_created,
                    'date_modified': datasource.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/datasources/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def datasource_manipulation(id, **kwargs):
        datasource = Datasource.query.filter_by(id=id).first()
        if not datasource:
            abort(404)

        if request.method == 'DELETE':
            datasource.delete()
            return {
            "message": "datasource {} deleted successfully".format(datasource.id)
         }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            datasource.name = name
            datasource.save()
            response = jsonify({
                'id': datasource.id,
                'name': datasource.name,
                'connection_string': datasource.connection_string,
                'date_created': datasource.date_created,
                'date_modified': datasource.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': datasource.id,
                'name': datasource.name,
                'connection_string': datasource.connection_string,
                'date_created': datasource.date_created,
                'date_modified': datasource.date_modified
            })
            response.status_code = 200
            return response

    return app
