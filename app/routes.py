from app import app
from flask import Flask, jsonify, request, Response

from .mongo_crud import Mongo_crud 
from .error_handlers import InvalidData

crud = Mongo_crud(
	app.config['HOST'],
	app.config['USER'], 
	app.config['PASSWORD'], 
	app.config['AUTH_SOURCE'], 
	app.config['AUTH_MECHANISM'], 
	app.config['DB_NAME'], 
	app.config['DB_COL'])

@app.errorhandler(InvalidData)
def handle_invalid_data(error):
	"""Manejador de excepciones de Flask
	
	Parameters
	----------
	error: InvalidData
		Excepción flask definida
		
	Returns
	-------
	Response: flask.Response
		respuesta con la información del error
	"""
	print(error.to_dict())
	response = jsonify(error.to_dict())
	response.status_code = error.status_code
	return response

@app.route("/clinicalinfo", methods=['GET'])
def clinicalinfo_all():
	if request.method == 'GET':
		"""Devuelve toda la información de gen_clinical_info.

		Se aceptan los parámetros start y limit que indican desde qué
		registro se comienza a devolver información y cuál es el ńúmero devuelto.
		Por defecto, 0 y 10 respectivamente.

		Returns
		-------
		Response: flask.Response
			200: conversion del JSON al mimetype application/json
		"""
		start = request.args.get('start', default = 0, type = int)
		limit = request.args.get('limit', default = 10, type = int)
		result = crud.get_all_clinicalinfo(field, value, start, limit)
		if isinstance(result, InvalidData):
			raise result
		else:
			return jsonify(result)

@app.route("/clinicalinfo/search-by-disease", methods=['GET'])
def clinicalinfo_disease():
	if request.method == 'GET':
		"""Devuelve información de gen_clinical_info por enfermedad.
		
		Se acepta el parámetro value, que tiene el valor de enfermedad por el
		que se va a buscar.

		Se aceptan los parámetros start y limit que indican desde qué
		registro se comienza a devolver información y cuál es el ńúmero devuelto.
		Por defecto, 0 y 10 respectivamente.

		Returns
		-------
		Response: flask.Response
			200: conversion del JSON al mimetype application/json
		"""
		start = request.args.get('start', default = 0, type = int)
		limit = request.args.get('limit', default = 10, type = int)
		value = request.args.get('value', default = '', type = str)
		result = crud.get_by_disease(value, start, limit)
		if isinstance(result, InvalidData):
			raise result
		else:
			return jsonify(result)

@app.route("/clinicalinfo/search-by-phenotype", methods=['GET'])
def clinicalinfo_phenotype():
	if request.method == 'GET':
		"""Devuelve información de gen_clinical_info por fenotipo
		
		Se acepta el parámetro value, que tiene el valor de fenotipo por el
		que se va a buscar.

		Se aceptan los parámetros start y limit que indican desde qué
		registro se comienza a devolver información y cuál es el ńúmero devuelto.
		Por defecto, 0 y 10 respectivamente.

		Returns
		-------
		Response: flask.Response
			200: conversion del JSON al mimetype application/json
		"""
		start = request.args.get('start', default = 0, type = int)
		limit = request.args.get('limit', default = 10, type = int)
		value = request.args.get('value', default = '', type = str)
		result = crud.get_by_phenotype(value, start, limit)
		if isinstance(result, InvalidData):
			raise result
		else:
			return jsonify(result)

@app.route("/clinicalinfo/<id_symbol>", methods=['GET'])
def clinicalinfo(id_symbol):
	if request.method == 'GET':
		"""Devuelve información de gen_clinical_info por Approved_symbol o por
		algún sinónimo, en Synonims

		Returns
		-------
		Response: flask.Response
			200: conversion del JSON al mimetype application/json
		"""
		result = crud.get_one_clinicalinfo(str(id_symbol))
		return jsonify(result)

@app.route("/cancer", methods=['GET'])
def cancer():
	if request.method == 'GET':
		"""Devuelve información de gen_clinical_info por fenotipo
		
		Se acepta el parámetro value, que tiene el valor de fenotipo por el
		que se va a buscar.

		Se aceptan los parámetros start y limit que indican desde qué
		registro se comienza a devolver información y cuál es el ńúmero devuelto.
		Por defecto, 0 y 10 respectivamente.

		Returns
		-------
		Response: flask.Response
			200: conversion del JSON al mimetype application/json
		"""
		start = request.args.get('start', default = 0, type = int)
		limit = request.args.get('limit', default = 10, type = int)
		value = request.args.get('value', default = '', type = str)
		result = crud.get_risks_by_cancergroup(value, start, limit)
		if isinstance(result, InvalidData):
			raise result
		else:
			return jsonify(result)

@app.route("/cancer/search-by-risk", methods=['GET'])
def cancer_risk_factors():
	if request.method == 'GET':
		"""Devuelve información de gen_clinical_info por fenotipo
		
		Se acepta el parámetro value, que tiene el valor de fenotipo por el
		que se va a buscar.

		Se aceptan los parámetros start y limit que indican desde qué
		registro se comienza a devolver información y cuál es el ńúmero devuelto.
		Por defecto, 0 y 10 respectivamente.

		Returns
		-------
		Response: flask.Response
			200: conversion del JSON al mimetype application/json
		"""
		start = request.args.get('start', default = 0, type = int)
		limit = request.args.get('limit', default = 10, type = int)
		value = request.args.get('value', default = '', type = str)
		result = crud.get_risks_by_riskfactor(value, start, limit)
		if isinstance(result, InvalidData):
			raise result
		else:
			return jsonify(result)

@app.route("/cancer/search-by-gen", methods=['GET'])
def cancer_gen():
	if request.method == 'GET':
		"""Devuelve información de gen_clinical_info por fenotipo
		
		Se acepta el parámetro value, que tiene el valor de fenotipo por el
		que se va a buscar.

		Se aceptan los parámetros start y limit que indican desde qué
		registro se comienza a devolver información y cuál es el ńúmero devuelto.
		Por defecto, 0 y 10 respectivamente.

		Returns
		-------
		Response: flask.Response
			200: conversion del JSON al mimetype application/json
		"""
		start = request.args.get('start', default = 0, type = int)
		limit = request.args.get('limit', default = 10, type = int)
		value = request.args.get('value', default = '', type = str)
		result = crud.get_risks_by_gen(value, start, limit)
		if isinstance(result, InvalidData):
			raise result
		else:
			return jsonify(result)

