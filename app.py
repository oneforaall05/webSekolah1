import jwt.exceptions
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from bson import ObjectId

from flask import Flask, render_template,jsonify,request,redirect,url_for

from werkzeug.utils import secure_filename

stringUrl='mongodb+srv://group05:kosonglima@group05.a81awpa.mongodb.net/?retryWrites=true&w=majority&appName=group05'
client = MongoClient(stringUrl)
db = client.websekolah

app = Flask(__name__)

# user start
# home 
@app.route('/',methods=['GET'])
def home():
   return render_template('index.html')


# loginUser 
@app.route('/login',methods=['GET'])
def userLogin():
   return render_template('user/login.html')

# registerUser
@app.route('/register',methods=['GET'])
def userRegister():
   return render_template('user/register.html')

# profileSekolahUser
@app.route('/profileSekolah',methods=['GET'])
def userProfileSekolah():
   return render_template('user/profileSekolah.html')

# StaffUser
@app.route('/staff',methods=['GET'])
def userStaff():
   return render_template('user/staff.html')

# berita
@app.route('/berita',methods=['GET'])
def userBerita():
   return render_template('user/berita.html')

# show berita
@app.route('/showBerita',methods=['GET'])
def userShowBerita():
   return render_template('user/showBerita.html')

# fasilitasUser
@app.route('/Fasilitas',methods=['GET'])
def userFasilitas():
   return render_template('user/fasilitas.html')

# formdaftar
@app.route('/formDaftar',methods=['GET'])
def userFormDaftar():
   return render_template('user/formDaftar.html')

# syaratDaftar
@app.route('/syaratDaftar',methods=['GET'])
def userSyaratDaftar():
   return render_template('user/syaratDaftar.html')

# user end


# admin start


# loginAdmin
@app.route('/adminLogin',methods=['GET'])
def adminLogin():
   return render_template('admin/loginAdmin.html')


# profileSekolahAdmin start

# profile sekolah 
@app.route('/adminProfileSekolah',methods=['GET'])
def AdminProfileSekolah():
   return render_template('admin/profileSekolah/profileSekolah.html')

# edit profile sekolah
@app.route('/adminEditProfileSekolah',methods=['GET'])
def AdminEditProfileSekolah():
   return render_template('admin/profileSekolah/editProfileSekolah.html')

# profileSekolahAdmin end


# staffAdmin start

# staff 
@app.route('/adminStaff',methods=['GET'])
def AdminStaff():
   return render_template('admin/staff/staff.html')

# edit staff
@app.route('/adminEditStaff',methods=['GET'])
def AdminEditStaff():
   return render_template('admin/staff/editStaff.html')

# add staff
@app.route('/adminAddStaff',methods=['GET'])
def AdminAddStaff():
   return render_template('admin/staff/addStaff.html')

# staffAdmin end


# berita start

# berita
@app.route('/adminBerita',methods=['GET'])
def AdminBerita():
   return render_template('admin/berita/berita.html')

# edit berita
@app.route('/adminEditBerita',methods=['GET'])
def AdminEditBerita():
   return render_template('admin/berita/editBerita.html')

# add berita
@app.route('/adminAddBerita',methods=['GET'])
def AdminAddBerita():
   return render_template('admin/berita/addBerita.html')

# komentar
@app.route('/adminDataKomentar',methods=['GET'])
def AdminDataKomentar():
   return render_template('admin/berita/dataKomentar.html')

# berita end


# pendaftaranAdmin start

# data pendaftaran
@app.route('/adminDataDaftar',methods=['GET'])
def AdminDataDaftar():
   return render_template('admin/pendaftaran/dataDaftar.html')

# edit data pendaftaran
@app.route('/adminEditDaftar',methods=['GET'])
def AdminEditDaftar():
   return render_template('admin/pendaftaran/editDaftar.html')

# pendaftaranAdmin end


# fasilitas start

# fasilitas
@app.route('/adminFasilitas',methods=['GET'])
def AdminFasilitas():
   fasilitas =  list(db.fasilitas.find({}))
   print (fasilitas)
   return render_template('admin/fasilitas/fasilitas.html',fasilitas=fasilitas)

# edit fasilitas 
@app.route('/adminEditFasilitas/<_id>',methods=['GET','POST'])
def AdminEditFasilitas(_id):
   if request.method=='POST':
      id=request.form['_id']
      nama=request.form['namaFasilitas']
      deskripsi=request.form['deskripsiFasilitas']
         
      nama_gambar= request.files['gambarFasilitas']
      
      doc={
            'namaFasilitas': nama,
            'deskripsiFasilitas':deskripsi
         }
      if nama_gambar:
         nama_gambar_asli = nama_gambar.filename
         nama_file_gambar = nama_gambar_asli.split('/')[-1]
         file_path =f'static/assets/img/imgfsl/{nama_file_gambar}'
         nama_gambar.save(file_path)
         doc['gambarFasilitas']=nama_file_gambar
         
      db.fasilitas.update_one({'_id':ObjectId(id)},{'$set':doc})
      return redirect(url_for('AdminFasilitas'))
   id =  ObjectId(_id)
   print(id)
   # id = ObjectId('6650c8e8970a90fc4870c5b4')
   fasilitas = list(db.fasilitas.find({'_id':id}))
   return render_template('admin/fasilitas/editFasilitas.html',fasilitas=fasilitas)

# add fasilitas
@app.route('/adminAddFasilitas',methods=['GET','POST'])
def AdminAddFasilitas():
   if request.method=='POST':
      # ambil input
      nama=request.form['namaFasilitas']
      deskripsi=request.form['deskripsiFasilitas']
      
      nama_gambar= request.files['gambarFasilitas']
      if nama_gambar:
         nama_gambar_asli = nama_gambar.filename
         nama_file_gambar = nama_gambar_asli.split('/')[-1]
         file_path =f'static/assets/img/imgfsl/{nama_file_gambar}'
         nama_gambar.save(file_path)
      else :
         nama_gambar=None
      doc = {
            'namaFasilitas':nama,
            'gambarFasilitas':nama_file_gambar,
            'deskripsiFasilitas':deskripsi
        }
      db.fasilitas.insert_one(doc)
      return redirect(url_for('AdminFasilitas'))
   return render_template('admin/fasilitas/addfasilitas.html')

# delete fasilitas
@app.route('/adminDeleteFasilitas/<_id>',methods=['GET','POST'])
def AdminDeleteFasilitas(_id):
   db.fasilitas.delete_one({'_id':ObjectId(_id)})
   return redirect(url_for('AdminFasilitas'))
 
@app.route("/test")
def test():
   id = ObjectId('6650c8e8970a90fc4870c5b4')
   
   fasilitas = list(db.fasilitas.find({'_id':id}))
   return render_template('admin/fasilitas/editFasilitas.html',fasilitas=fasilitas)
# fasilitas end


# admin end

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)