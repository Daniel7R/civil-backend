from importlib.metadata import requires
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app= Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/civil'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db= SQLAlchemy(app)
ma= Marshmallow(app)


class Tbl_User(db.Model):
    cedula= db.Column(db.String(20), primary_key=True)
    primer_nombre= db.Column(db.String(50))
    segundo_nombre= db.Column(db.String(50))
    primer_apellido= db.Column(db.String(50))
    segundo_apellido= db.Column(db.String(50))
    email= db.Column(db.String(50), unique=True)
    direccion= db.Column(db.String(50))
    unidad= db.Column(db.String(40))
    departamento= db.Column(db.String(30))
    municipio= db.Column(db.String(30))
    barrio= db.Column(db.String(30))
    phone= db.Column(db.String(10))
    escolaridad= db.Column(db.String(20))
    latitud= db.Column(db.String(20))
    longitud= db.Column(db.String(20))
    
    def __init__(self, cedula, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, 
                 email, direccion, unidad, departamento, municipio, barrio, phone, escolaridad,
                 latitud, longitud):
        
        self.cedula= cedula
        self.primer_nombre= primer_nombre
        self.segundo_nombre= segundo_nombre
        self.primer_apellido= primer_apellido
        self.segundo_apellido= segundo_apellido
        self.email= email
        self.direccion= direccion
        self.unidad= unidad
        self.departamento= departamento
        self.municipio= municipio
        self.barrio= barrio
        self.phone= phone
        self.escolaridad= escolaridad
        self.latitud= latitud
        self.longitud= longitud
    
db.create_all()

class EncuestadoSchema(ma.Schema):
    class Meta:
        fields= ('cedula', 'primer_nombre', "segundo_nombre", "primer_apellido", 
                 "segundo_apellido", 'email', 'direccion','unidad', 'departamento', 
                 'municipio', 'barrio', 'phone', 'escolaridad', 'latitud','longitud')
        
encuestado_schema= EncuestadoSchema()

@app.route("/personal-info", methods= ["POST"])
def create_personal_data():
    cedula= request.json['cedula']
    primer_nombre= request.json["primer_nombre"]
    segundo_nombre= request.json["segundo_nombre"]
    primer_apellido =request.json["primer_apellido"]
    segundo_apellido= request.json["segundo_apellido"]
    email= request.json["email"]
    direccion= request.json["direccion"]
    unidad= request.json["unidad"]
    departamento= request.json["departamento"]
    municipio= request.json["municipio"]
    barrio= request.json["barrio"]
    phone= request.json["phone"]
    escolaridad= request.json["escolaridad"]
    latitud= request.json["latitud"]
    longitud= request.json["longitud"]
    
    new_encuestado= Tbl_User(cedula, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, 
                             email, direccion,unidad, departamento, municipio, barrio, phone, escolaridad,
                             latitud, longitud)
    
    db.session.add(new_encuestado)
    db.session.commit()
    
    return encuestado_schema.jsonify(new_encuestado)

class RespuestasExteriorVivienda(db.Model):
    
    cedula= db.Column(db.String(20), db.ForeignKey('tbl__user.cedula'), primary_key= True)
    anio= db.Column(db.String(20))
    constructora= db.Column(db.String(2))
    nombre_contructora= db.Column(db.String(30))
    area_vivienda= db.Column(db.String(30))
    imagen_vivienda= db.Column(db.Text)
    ubicacion= db.Column(db.String(10))
    elementos_cercanos= db.Column(db.String(20))
    uso_actual= db.Column(db.String(30))
    uso_diferente= db.Column(db.String(2))
    uso_diferente_anterior= db.Column(db.String(30))
    uso_primer_piso= db.Column(db.String(30))
    numero_pisos= db.Column(db.String(20))
    piso_vivienda= db.Column(db.String(20))
    sotanos= db.Column(db.String(20))
    comparte_muro= db.Column(db.String(2))
    equipos= db.Column(db.String(25))
    
    def __init__(self, cedula, anio, constructora, nombre_constructora, area_vivienda, imagen_vivienda, ubicacion,
                 elementos_cercanos, uso_actual, uso_diferente, uso_diferente_anterior, uso_primer_piso, numero_pisos, piso_vivienda,
                 sotanos, comparte_muro, equipos):
        self.cedula= cedula
        self.anio= anio
        self.constructora= constructora
        self.nombre_contructora= nombre_constructora
        self.area_vivienda= area_vivienda
        self.imagen_vivienda= imagen_vivienda
        self.ubicacion= ubicacion
        self.elementos_cercanos= elementos_cercanos
        self.uso_actual= uso_actual
        self.uso_diferente= uso_diferente
        self.uso_diferente_anterior= uso_diferente_anterior
        self.uso_primer_piso= uso_primer_piso
        self.numero_pisos= numero_pisos
        self.piso_vivienda= piso_vivienda
        self.sotanos= sotanos
        self.comparte_muro= comparte_muro
        self.equipos= equipos

class RespuestasInteriorVivienda(db.Model):
    
    cedula= db.Column(db.String(20), db.ForeignKey('tbl__user.cedula'), primary_key= True)
    altura_pisos= db.Column(db.String(25))
    material_construccion= db.Column(db.String(20))
    tipo_construccion= db.Column(db.String(30))
    tipo_piso= db.Column(db.String(40))
    tipo_techo= db.Column(db.String(40))
    hundimiento= db.Column(db.String(2))
    imagen_lejana_hundimiento= db.Column(db.Text)
    imagen_cercana_hundimiento= db.Column(db.Text)
    grietas= db.Column(db.Text)
    imagen_lejana_grieta= db.Column(db.Text)
    imagen_cercana_grieta= db.Column(db.Text) 
    
    def __init__(self, cedula, altura_pisos, material_construccion, tipo_construccion, tipo_piso, tipo_techo,
                 hundimiento, imagen_lejana_hundimiento, imagen_cercana_hundimiento, grietas, imagen_lejana_grieta, 
                 imagen_cercana_grieta ):
        
        self.cedula= cedula
        self.altura_pisos= altura_pisos
        self.material_construccion= material_construccion
        self.tipo_construccion= tipo_construccion
        self.tipo_piso= tipo_piso
        self.tipo_techo= tipo_techo
        self.hundimiento= hundimiento
        self.imagen_lejana_hundimiento= imagen_lejana_hundimiento
        self.imagen_cercana_hundimiento= imagen_cercana_hundimiento
        self.grietas= grietas
        self.imagen_lejana_grieta= imagen_lejana_grieta
        self.imagen_cercana_grieta= imagen_cercana_grieta

db.create_all()
        
class RespuestasExteriorViviendaSchema(ma.Schema):
    
    class Meta:
        fields=  ('cedula', 'anio', 'constructora', 'nombre_constructora', 'area_vivienda', 'imagen_vivienda',
                 'ubicacion', 'elementos_cercanos', 'uso_actual', 'uso_diferente', 'uso_diferente_anterior',
                 'uso_primer_piso', 'numero_pisos', 'piso_vivienda', 'sotanos', 'comparte_muro', 
                 'equipos')

respuestas_exterior_vivienda_schema= RespuestasExteriorViviendaSchema()

class RespuestasInteriorViviendaSchema(ma.Schema):
    
    class Meta:
        fields= ("cedula", "altura_pisos", "material_construccion", "tipo_construccion", "tipo_piso", "tipo_techo",
                 "hundimiento", "imagen_lejana_hundimiento", "imagen_cercana_hundimiento", "grietas", "imagen_lejana_grieta",
                 "imagen_cercana_grieta")

respuestas_interior_vivienda_schema= RespuestasInteriorViviendaSchema()

@app.route("/respuestas", methods=["POST"])
def saveAnswers():
    cedula= request.json["cedula"]
    anio= request.json["anio"]
    constructora= request.json["constructora"]
    nombre_contructora= request.json["nombre_constructora"]
    area_vivienda= request.json["area_vivienda"]
    imagen_vivienda= request.json["imagen_vivienda"]
    ubicacion= request.json["ubicacion"]
    elementos_cercanos= request.json["elementos_cercanos"]
    uso_actual= request.json["uso_actual"]
    uso_diferente= request.json["uso_diferente"]
    uso_diferente_anterior= request.json["uso_diferente_anterior"]
    uso_primer_piso= request.json["uso_primer_piso"]
    numero_pisos= request.json["numero_pisos"]
    piso_vivienda= request.json["piso_vivienda"]
    sotanos= request.json["sotanos"]
    comparte_muro= request.json["comparte_muro"]
    equipos= request.json["equipos"]
    
    exterior_vivienda= RespuestasExteriorVivienda(cedula, anio, constructora, nombre_contructora, area_vivienda, imagen_vivienda,
                                                  ubicacion, elementos_cercanos, uso_actual, uso_diferente, uso_diferente_anterior, uso_primer_piso,
                                                  numero_pisos, piso_vivienda, sotanos, comparte_muro, equipos)
    
    altura_pisos= request.json["altura_pisos"]
    material_construccion= request.json["material_construccion"]
    tipo_construccion= request.json["tipo_construccion"]
    tipo_piso= request.json["tipo_piso"]
    tipo_techo= request.json["tipo_techo"]
    hundimiento= request.json["hundimiento"]
    imagen_lejana_hundimiento= request.json["imagen_lejana_hundimiento"]
    imagen_cercana_hundimiento= request.json["imagen_cercana_hundimiento"]
    grietas= request.json["grietas"]
    imagen_lejana_grieta= request.json["imagen_lejana_grieta"]
    imagen_cercana_grieta= request.json["imagen_cercana_grieta"]
    
    interior_vivienda= RespuestasInteriorVivienda(cedula, altura_pisos, material_construccion, tipo_construccion, tipo_piso, tipo_techo,
                                                  hundimiento, imagen_lejana_hundimiento, imagen_cercana_hundimiento, grietas, imagen_lejana_grieta,
                                                  imagen_cercana_grieta)
    
    db.session.add(exterior_vivienda)
    db.session.add(interior_vivienda)
    db.session.commit() 
    
    return "saved"


if(__name__ == "__main__"):
    app.run(debug=True)

# @app.route("/respuestas", methods= ["POST"])
# def upload_answers():
#     cedula= request.json["cedula"]
    
class Upload(db.Model):
    id= db.Column(db.Integer, primary_key= True)
    file= db.Column(db.Text)
    
    def __init__(self,id, file):
        self.id= id
        self.file= file

db.create_all()


@app.route("/test", methods=["POST"])
def uploadImg():
    id= 17
    file= request.json["file"]
    
    new_upload= Upload(id, file)
    db.session.add(new_upload)
    db.session.commit()
    
    return "uploaded"


"""
@app.route('/tasks',methods= ['POST'])
def  create_task():
    title= request.json['title']
    description= request.json['description']
    
    new_task= Data(title,description)
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)

@app.route("/tasks", methods=['GET'])
def  get_tasks():
    all_tasks= Data.query.all()
    result= tasks_schema.dump(all_tasks)
    return tasks_schema.jsonify(result)

@app.route("/tasks/<id>",methods=["GET"])
def get_task(id):
    task= Data.query.get(id)
    return task_schema.jsonify(task)


@app.route('/tasks/<id>',methods=["PUT"])
def update_task(id):
    task= Data.query.get(id)
    
    title= request.json["title"]
    description= request.json["description"]
    
    task.title= title
    task.description= description
    
    db.session.commit()
    
    return task_schema.jsonify(task)
"""
    
"""
class Data(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(70),unique=True)
    description= db.Column(db.String(100))
    
    def __init__(self,title,description):
        self.title= title
        self.description= description
        
db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields= ('id','title','description')
        
task_schema= TaskSchema()
tasks_schema= TaskSchema(many= True)
"""

# class Respuestas(db.Model):
    
#     cedula= db.Column(db.String(20), db.ForeignKey('tbl__user.cedula'), primary_key= True)
#     anio= db.Column(db.String(20))
#     constructora= db.Column(db.String(2))
#     nombre_contructora= db.Column(db.String(30))
#     area_vivienda= db.Column(db.String(30))
#     imagen_vivienda= db.Column(db.Text)
#     ubicacion= db.Column(db.String(10))
#     elementos_cercanos= db.Column(db.String(20))
#     uso_actual= db.Column(db.String(30))
#     uso_diferente= db.Column(db.String(2))
#     uso_diferente_anterior= db.Column(db.String(30))
#     uso_primer_piso= db.Column(db.String(30))
#     numero_pisos= db.Column(db.String(20))
#     piso_vivienda= db.Column(db.String(20))
#     sotanos= db.Column(db.String(20))
#     comparte_muro= db.Column(db.String(2))
#     equipos= db.Column(db.String(25))
#     altura_pisos= db.Column(db.String(25))
#     material_construccion= db.Column(db.String(20))
#     tipo_construccion= db.Column(db.String(30))
#     tipo_piso= db.Column(db.String(40))
#     tipo_techo= db.Column(db.String(40))
#     hundimiento= db.Column(db.String(2))
#     #faltan 2 imagenes del hundimiento
    
#     def __init__(self, cedula, anio, constructora, nombre_constructora, area_vivienda, ubicacion,
#                  elementos_cercanos, uso_actual, uso_diferente, uso_diferente_anterior, uso_primer_piso, numero_pisos, piso_vivienda,
#                  sotanos, comparte_muro, equipos, altura_pisos, material_construccion, tipo_construccion,
#                  tipo_piso, tipo_techo, hundimiento):
#         self.cedula= cedula
#         self.anio= anio
#         self.constructora= constructora
#         self.nombre_contructora= nombre_constructora
#         self.area_vivienda= area_vivienda
        
#         self.ubicacion= ubicacion
#         self.elementos_cercanos= elementos_cercanos
#         self.uso_actual= uso_actual
#         self.uso_diferente= uso_diferente
#         self.uso_diferente_anterior= uso_diferente_anterior
#         self.uso_primer_piso= uso_primer_piso
#         self.numero_pisos= numero_pisos
#         self.piso_vivienda= piso_vivienda
#         self.sotanos= sotanos
#         self.comparte_muro= comparte_muro
#         self.equipos= equipos
#         self.altura_pisos= altura_pisos
#         self.material_construccion= material_construccion
#         self.tipo_construccion= tipo_construccion
#         self.tipo_piso= tipo_piso
#         self.tipo_techo= tipo_techo
#         self.hundimiento= hundimiento
# db.create_all()


# class RespuestasSchema(ma.Schema):
#     class Meta:
#         fields= ('cedula', 'anio', 'constructora', 'nombre_constructora', 'area_vivienda',
#                  'ubicacion', 'elementos_cercanos', 'uso_actual', 'uso_diferente', 'uso_diferente_anterior',
#                  'uso_primer_piso', 'numero_pisos', 'piso_vivienda', 'sotanos', 'comparte_muro', 
#                  'equipos', 'altura_pisos', 'material_construccion', 'tipo_construccion', 'tipo_piso', 'tipo_techo',
#                  'hundimiento')
        
# respuestas_schema= RespuestasSchema()
