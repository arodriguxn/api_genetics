from pymongo import MongoClient
import re

from .error_handlers import InvalidData

class Mongo_crud:
	"""CRUD con las operaciones de la API.
	
	Parameters
	----------
	host: str
		IP donde está funcionando la base de datos
	username: str
		Usuario de la bd
	password: str
		contraseña de la bd
	auth_source: str
		base de datos de autenticación
	auth_mechanism: str
		método de autenticación
	db_name: str
		nombre de la base de datos usada
	col_name: str
		nombre de la colección usada

	Attributes
	----------
	client: pymongo.mongo_client.MongoClient
		Cliente de la conexión con Mongo
	db: pymongo.database.Database
		Base de datos del proyecto
	col: pymongo.collection.Collection
		Colección de Mongo sobre la que se realizan las operaciones
	clinicalinfo_att: dict
		Filtro para clinical info
	cancer_att: dict
		Filtro para onco_gene_risks_factors
	"""

	def __init__(self, host, username, password, auth_source, auth_mechanism, db_name, col_name):
		self.client = MongoClient(host, username=username, password=password, authSource=auth_source, authMechanism=auth_mechanism)
		self.db = self.client[db_name]
		self.gene_col = self.db[col_name]
		self.clinicalinfo_att = {'type': 'gene_clinical_info'}
		self.cancer_att = {'type': 'onco_gene_risk_factors'}

	def get_all_clinicalinfo(self, start, limit):
		"""Devuelve toda la información de gen_clinical_info
		
		Parameters
		----------
		start: int
			número de documentos por el cual se empieza a 
			devolver información
		limit: int
			número de documentos devueltos

		Returns
		-------
		List: list
			toda la información en una lista
		"""
		clinicalinfo_list = []
		query_field = "data." + field
		cursor = self.gene_col.find({query_field: value}).skip(start).limit(limit)
		for record in cursor:
			# elimina el identificador
			record.pop('_id')
			clinicalinfo_list.append(record)
		return	clinicalinfo_list

	def get_one_clinicalinfo(self, symbol):
		"""Devuelve gen_clinical_info buscando por Approved_symbol o por Synonim

		Returns
		-------
		List: list
			lista de gen_clinical_info
		"""
		genes = []
		cursor = self.gene_col.find({**self.clinicalinfo_att, "Approved_symbol": symbol})
		for record in cursor:
			# elimina el identificador
			record.pop('_id')
			genes.append(record)
		return genes

	def get_by_disease(self, disease, start, limit):
		"""Devuelve gen_clinical_info buscando por enfermedad
		
		Parameters
		----------
		disease: str
			enfermedad por la que se va a buscar
		start: int
			número de documentos por el cual se empieza a 
			devolver información
		limit: int
			número de documentos devueltos

		Returns
		-------
		List: list
			lista de gen_clinical_info
		"""
		clinicalinfo_list = []
		reg_value = re.compile(".*" + disease + ".*", re.IGNORECASE)
		cursor = self.gene_col.find(
			{"$or": [
				{"HPO_omim.omimDiseaseName": reg_value},
				{"HPO_orpha.HPO_orphaDiseaseName": reg_value},
				{"MONARCH.MONARCH_diseaseName": reg_value},
				{"DECIPHER.DECIPHER_omimDiseaseName": reg_value},
				{"clinvar_pathogenicUncertain_disease": reg_value}
			]}
				)
		for record in cursor:
			# elimina el identificador
			record.pop('_id')
			clinicalinfo_list.append(record)
		return	clinicalinfo_list

	def get_by_phenotype(self, phenotype, start, limit):
		"""Devuelve gen_clinical_info buscando por fenotipo
		
		Parameters
		----------
		phenotype: str
			fenotipo por el que se va a buscar
		start: int
			número de documentos por el cual se empieza a 
			devolver información
		limit: int
			número de documentos devueltos

		Returns
		-------
		List: list
			lista de gen_clinical_info
		"""
		clinicalinfo_list = []
		reg_value = re.compile(".*" + phenotype + ".*", re.IGNORECASE)
		cursor = self.gene_col.find(
			{"$or": [
				{"HPO_omim.HPO_omimHpoTerms": reg_value},
				{"HPO_orpha.HPO_orphaHpoTerms": reg_value},
				{"MONARCH.MONARCH_hpoTerms": reg_value},
				{"DECIPHER.DECIPHER_omimHpoTerms": reg_value}
			]}
				)
		for record in cursor:
			# elimina el identificador
			record.pop('_id')
			clinicalinfo_list.append(record)
		return	clinicalinfo_list

	def get_risks_by_cancergroup(self, cancer_group, start, limit):
		"""Devuelve onco_gene_risk_factors buscando por grupo de cáncer
		
		Parameters
		----------
		cancer_group: str
			grupo de cáncer por el que se va a buscar
		start: int
			número de documentos por el cual se empieza a 
			devolver información
		limit: int
			número de documentos devueltos

		Returns
		-------
		List: list
			lista de onco_gene_risk_factors
		"""
		cancer_list = []
		reg_value = re.compile(".*" + cancer_group + ".*", re.IGNORECASE)
		cursor = self.gene_col.find({**self.cancer_att, "cancer_group": reg_value})
		for record in cursor:
			# elimina el identificador
			record.pop('_id')
			cancer_list.append(record)
		return	cancer_list

	def get_risks_by_riskfactor(self, risk_factor, start, limit):
		"""Devuelve onco_gene_risk_factors buscando por gen
		
		Parameters
		----------
		risk_factor: str
			factor de riesgo por el que se va a buscar
		start: int
			número de documentos por el cual se empieza a 
			devolver información
		limit: int
			número de documentos devueltos

		Returns
		-------
		List: list
			lista de onco_gene_risk_factors
		"""
		cancer_list = []
		reg_value = re.compile(".*" + risk_factor + ".*", re.IGNORECASE)
		cursor = self.gene_col.find({**self.cancer_att, 
			"$or": [
				{"risk_factors_IARCC": reg_value},
				{"risk_factors_NTP": reg_value}
			]})
		for record in cursor:
			# elimina el identificador
			record.pop('_id')
			cancer_list.append(record)
		return	cancer_list

	def get_risks_by_gen(self, gen, start, limit):
		"""Devuelve onco_gene_risk_factors buscando por gen
		
		Parameters
		----------
		gen: str
			grupo de cáncer por el que se va a buscar
		start: int
			número de documentos por el cual se empieza a 
			devolver información
		limit: int
			número de documentos devueltos

		Returns
		-------
		List: list
			lista de onco_gene_risk_factors
		"""
		cancer_list = []
		query_genes_somatic = "cancer_types_list.genes_somatic." + gen
		query_genes_germline = "cancer_types_list.genes_germline." + gen
		cursor = self.gene_col.find({**self.cancer_att, "$or": [
				{query_genes_somatic: {"$exists": True}},
				{query_genes_germline: {"$exists": True}}
			]}).skip(start).limit(limit)
		for record in cursor:
			# elimina el identificador
			record.pop('_id')
			cancer_list.append(record)
		return cancer_list