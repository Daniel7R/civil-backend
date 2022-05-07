from calendar import c
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from sqlalchemy import true
from sqlalchemy.sql.expression import asc,desc

app= Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/civil'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db= SQLAlchemy(app)
ma= Marshmallow(app)


class Tbl_User(db.Model):
    id_encuestado= db.Column(db.Integer, primary_key= True)
    cedula= db.Column(db.String(20))
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
        fields= ('id_encuestado','cedula', 'primer_nombre', "segundo_nombre", "primer_apellido", 
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
    id_respuestas= db.Column(db.Integer, primary_key= True)
    id_encuestado= db.Column(db.Integer, db.ForeignKey('tbl__user.id_encuestado'))
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
    
    def __init__(self, id_encuestado, anio, constructora, nombre_constructora, area_vivienda, imagen_vivienda, ubicacion,
                 elementos_cercanos, uso_actual, uso_diferente, uso_diferente_anterior, uso_primer_piso, numero_pisos, piso_vivienda,
                 sotanos, comparte_muro, equipos):
        self.id_encuestado= id_encuestado
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
    
    id_respuestas= db.Column(db.Integer, primary_key=True)
    id_encuestado= db.Column(db.Integer, db.ForeignKey('tbl__user.id_encuestado'))
    altura_pisos= db.Column(db.String(25))
    material_construccion= db.Column(db.String(20))
    tipo_construccion= db.Column(db.String(30))
    tipo_piso= db.Column(db.String(40))
    tipo_techo= db.Column(db.String(40))
    hundimiento= db.Column(db.String(2))
    imagen_lejana_hundimiento= db.Column(db.Text)
    imagen_cercana_hundimiento= db.Column(db.Text)
    grietas= db.Column(db.String(2))
    imagen_lejana_grieta= db.Column(db.Text)
    imagen_cercana_grieta= db.Column(db.Text) 
    
    def __init__(self, id_encuestado, altura_pisos, material_construccion, tipo_construccion, tipo_piso, tipo_techo,
                 hundimiento, imagen_lejana_hundimiento, imagen_cercana_hundimiento, grietas, imagen_lejana_grieta, 
                 imagen_cercana_grieta ):
        
        self.id_encuestado= id_encuestado
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

class ResultadosGenerales(db.Model):
    id_respuesta= db.Column(db.Integer, primary_key= True)
    id_encuestado=db.Column(db.Integer, db.ForeignKey("tbl__user.id_encuestado"))
    escala_vulnerabilidad= db.Column(db.String(30))
    porcentaje= db.Column(db.String(5))
    
    def __init__(self, id_encuestado, escala_vulnerabilidad, porcentaje):
        self.id_encuestado= id_encuestado
        self.escala_vulnerabilidad= escala_vulnerabilidad
        self.porcentaje= porcentaje
        
db.create_all()
        
class RespuestasExteriorViviendaSchema(ma.Schema):
    
    class Meta:
        fields=  ('id_encuestado', 'anio', 'constructora', 'nombre_constructora', 'area_vivienda', 'imagen_vivienda',
                 'ubicacion', 'elementos_cercanos', 'uso_actual', 'uso_diferente', 'uso_diferente_anterior',
                 'uso_primer_piso', 'numero_pisos', 'piso_vivienda', 'sotanos', 'comparte_muro', 
                 'equipos')

respuestas_exterior_vivienda_schema= RespuestasExteriorViviendaSchema()

class RespuestasInteriorViviendaSchema(ma.Schema):
    
    class Meta:
        fields= ("id_encuestado", "altura_pisos", "material_construccion", "tipo_construccion", "tipo_piso", "tipo_techo",
                 "hundimiento", "imagen_lejana_hundimiento", "imagen_cercana_hundimiento", "grietas", "imagen_lejana_grieta",
                 "imagen_cercana_grieta")

respuestas_interior_vivienda_schema= RespuestasInteriorViviendaSchema()

class ResultadosGeneralesSchema(ma.Schema):
    
    class Meta:
        fields= ('id_encuestado', 'escala_vulnerabilidad', 'porcentaje')

resultados_generales_schema= ResultadosGeneralesSchema()

class AllResultadosSchema(ma.Schema):
    
    class Meta:
        fields= ( 'id_encuestado','cedula', 'primer_nombre', "segundo_nombre", "primer_apellido", 
                 "segundo_apellido", 'email', 'direccion','unidad', 'departamento', 'municipio', 
                 'barrio', 'phone', 'escolaridad', 'latitud','longitud',"altura_pisos", "material_construccion",
                 "tipo_construccion", "tipo_piso", "tipo_techo","hundimiento", "imagen_lejana_hundimiento", 
                 "imagen_cercana_hundimiento", "grietas", "imagen_lejana_grieta","imagen_cercana_grieta",'anio', 
                 'constructora', 'nombre_constructora', 'area_vivienda', 'imagen_vivienda','ubicacion', 'elementos_cercanos',
                 'uso_actual', 'uso_diferente', 'uso_diferente_anterior','uso_primer_piso', 'numero_pisos', 'piso_vivienda',
                 'sotanos', 'comparte_muro', 'equipos')
        
all_schema= AllResultadosSchema(many= True)

@app.route("/respuestas", methods=["POST"])
def saveAnswers():
    id_encuestado= request.json["id_encuestado"]
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
    
    exterior_vivienda= RespuestasExteriorVivienda(id_encuestado, anio, constructora, nombre_contructora, area_vivienda, imagen_vivienda,
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
    
    interior_vivienda= RespuestasInteriorVivienda(id_encuestado, altura_pisos, material_construccion, tipo_construccion, tipo_piso, tipo_techo,
                                                  hundimiento, imagen_lejana_hundimiento, imagen_cercana_hundimiento, grietas, imagen_lejana_grieta,
                                                  imagen_cercana_grieta)
    
    escala_vulnerabilidad= request.json["escala_vulnerabilidad"]
    porcentaje= request.json["porcentaje"]
    
    resultados_generales= ResultadosGenerales(id_encuestado, escala_vulnerabilidad, porcentaje)
    
    
    db.session.add(exterior_vivienda)
    db.session.add(interior_vivienda)
    db.session.add(resultados_generales)
    db.session.commit() 
    
    return "saved"

@app.route("/login")
def login():
    
    if request.method == "POST":
        username= request.json["username"]
        password= request.json["password"]
        
        usernamedata= db.execute("SELECT user FROM tbl_admin WHERE username=:username",
                             {"username":username}).fetchone() 
        passworddata= db.execute("SELECT password FROM tbl_admin WHERE username=:username",
                                {"username": username}).fetchone()
        
    if usernamedata is None:
        return("Usuario no registrado")

#Declaro schemas para traer todos los datos de cada tabla
encuestados_schema= EncuestadoSchema(many= True)
exterior_schema= RespuestasExteriorViviendaSchema(many= True)
interior_schema= RespuestasInteriorViviendaSchema(many= True)
resultados_schema= ResultadosGeneralesSchema(many= True)

#Para obtener toda la información personal de los encuestados
@app.route("/get-data-personal", methods=["GET"])
def data_personal():
    encuestados= db.session.query(Tbl_User).order_by(asc(Tbl_User.id_encuestado)).all()
    ordered_encuestados= encuestados_schema.dump(encuestados)
    
    return encuestados_schema.jsonify(ordered_encuestados)

#Para traer todas las respuestas de los encuestados en lo que corresponde al exterior
@app.route("/get-data-exterior", methods=["GET"])
def data_exterior():
    exterior= db.session.query(RespuestasExteriorVivienda).order_by(asc(RespuestasExteriorVivienda.id_encuestado)).all()
    ordered_exterior= exterior_schema.dump(exterior)
    
    return exterior_schema.jsonify(ordered_exterior)

@app.route("/get-data-interior", methods=["GET"])
def data_interior():
    interior= db.session.query(RespuestasInteriorVivienda).order_by(asc(RespuestasInteriorVivienda.id_encuestado)).all()
    ordered_interior= interior_schema.dump(interior)
    
    return interior_schema.jsonify(ordered_interior)

@app.route("/get-data-results", methods=["GET"])
def data_general():
    resultados_generales= db.session.query(ResultadosGenerales).order_by(asc(ResultadosGenerales.id_encuestado)).all()
    ordered_resultados= resultados_schema.dump(resultados_generales)
    
    return resultados_schema.jsonify(ordered_resultados)
            
@app.route("/get-fka/<cedula>", methods=["GET"])
def get_fk(cedula):
    d= db.session.query(Tbl_User).filter_by(cedula=cedula).all()
    
    return encuestado_schema.jsonify(d[-1])

if(__name__ == "__main__"):
    app.run(debug=True)


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