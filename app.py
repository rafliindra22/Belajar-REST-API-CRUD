# import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

# import library sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os

# konfigurasi databse
basedir =  os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "mydb.sqlite")

# inisialisasi object flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database

# inisialisasi object flask restful
restapi = Api(app)

# inisialisasi object flask cors
CORS(app)

# inisialisasi object flask sqlalchemy
db = SQLAlchemy(app=app)

# membuat model databse
class ModelDatabase(db.Model):
    # membuat field database
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    tanggalLahir = db.Column(db.String(10))
    tempatLahir = db.Column(db.String(15))
    pesanKesan = db.Column(db.TEXT)

    # membuat metode untuk menyimpan data pada database
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

# create database
with app.app_context():
    db.create_all()

# inisialisasikan variable kosong bertipe dictionary untuk pembacaan JSON
isian = {}

# membuat class resource
class ResourceDB(Resource):
    # membuat methode
    ## method get all
    def get(self):
        # query get all database
        getquery = ModelDatabase.query.all()

        # lakukan looping agar semua data bisa dimunculkan
        output = [
            {
                # harus ada => key : value
                "id"           : data.id,
                "nama"         : data.nama,
                "tanggal lahir" : data.tanggalLahir,
                "tempat lahir"  : data.tempatLahir,
                "pesan dan kesan"   : data.pesanKesan
            }
            for data in getquery
        ]
        
        response = {
            "status"    : 200,
            "message"   : "Data keseluruhan berhasil ditampilkan",
            "data"      : output
        }
        return response

    ## methode post
    def post(self):
        
        # request form pengisian data
        dataNama = request.form["nama"]
        dataTanggallhr = request.form["tanggalLahir"]
        dataTempatllhr = request.form["tempatLahir"]
        dataPesankesan = request.form["pesanKesan"]

        # masukan data ke dalam database
        model = ModelDatabase(
            nama = dataNama,
            tanggalLahir = dataTanggallhr,
            tempatLahir = dataTempatllhr,
            pesanKesan = dataPesankesan
        )
        model.save()

        response = {
            "status"    : 200,
            "message"   : "data berhasil di-input dan disimpan"
        }
        return response
    
    def delete(self):
        # query delete all data
        delquery = ModelDatabase.query.all()

        # loping delete session
        for data in delquery :
            # panggil method delete
            db.session.delete(data)
            db.session.commit()
        
        response =  {
            "status"    : 200,
            "message"   : "semua data berhasil dihapus "
        }
        return response



# Class untuk memilih resource berdasarkan id
class ResourcebyId(Resource):
    ## method get by id
    def get(self, id):
        # query untuk consume id yang akan ditampilkan
        getquery = ModelDatabase.query.get(id)

        output = {
            # harus ada => key : value
            "nama"         : getquery.nama,
            "tanggal lahir" : getquery.tanggalLahir,
            "tempat lahir"  : getquery.tempatLahir,
            "pesan dan kesan"   : getquery.pesanKesan
        }
        response = {
            "status"    : 200,
            "message"   : "data dengan id "+id+" berhasil di tampilkan",
            "id : "+id  : output
        }
        return response

    def delete(self, id):
        # query untul consume id yang akan dihapus
        delquery = ModelDatabase.query.get(id)

        # method delete session by id
        db.session.delete(delquery)
        db.session.commit()

        response = {
            "status"    : 200,
            "message"   : " data dengan id "+id+" telah berhasil di hapus"
        }
        return response

    def put(self, id):
        # query untuk consume id yang akan diedit
        putquery = ModelDatabase.query.get(id)

        # membuat form pengeditan data
        editNama = request.form["nama"]
        editTglLahir = request.form["tanggalLahir"]
        editTmptLahir = request.form["tempatLahir"]
        editPesanKesan = request.form["pesanKesan"]

        # replace nilai yang ada pada setiap field + session commit
        putquery.nama = editNama
        putquery.tanggalLahir = editTglLahir
        putquery.tempatLahir = editTmptLahir
        putquery.pesanKesan = editPesanKesan
        db.session.commit()

        response = {
            "status" : 200,
            "message" : "data dengan id "+id+" telah berhasil diedit"
        }
        return response

# membuat endpoint
restapi.add_resource(ResourceDB, "/data", methods = ["GET", "POST", "DELETE"])
restapi.add_resource(ResourcebyId, "/data/<id>", methods = ["GET", "DELETE", "PUT"])

if __name__ == "__main__":
    app.run(debug=True, port=5000)