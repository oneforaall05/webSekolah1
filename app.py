import jwt.exceptions
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
import os
from bson import ObjectId

from flask import Flask, render_template,jsonify,request,redirect,url_for

from werkzeug.utils import secure_filename

stringUrl='mongodb+srv://group05:kosonglima@group05.a81awpa.mongodb.net/?retryWrites=true&w=majority&appName=group05'
client = MongoClient(stringUrl)
db = client.websekolah

SECRET_KEY = "S4nd4l&sp1r1t_"
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
@app.route('/adminLogin',methods=['GET',"POST"])
def adminLogin():
   if request.method == "POST":
      username_receive = request.form["username_give"]
      password_receive = request.form["password_give"]
      print(username_receive)
      print(password_receive)
      pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
      print(pw_hash)
      result = db.admin.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
      )
      if result:
         payload = {
         "id": username_receive,
         # the token will be valid for 24 hours
         "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
         }
         token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

         return jsonify(
               {
                  "result": "success",
                  "token": token,
                  }
         )
      # Let's also handle the case where the id and
      # password combination cannot be found
      else:
         return jsonify(
               {
                  "result": "fail",
                  "msg": "We could not find a user with that id/password combination",
               }
         )
      
   return render_template('admin/loginAdmin.html')


# profileSekolahAdmin start

# profile sekolah 
@app.route('/adminProfileSekolah',methods=['GET'])
def AdminProfileSekolah():
   struktur = list(db.struktur.find({}))
   return render_template('admin/profileSekolah/profileSekolah.html',struktur = struktur)

# edit profile sekolah
@app.route('/adminEditProfileSekolah/<_id>',methods=['GET','POST'])
def AdminEditProfileSekolah(_id):
   if request.method == "POST":
          id = request.form["_id"]
          sejarah = request.form["sejarah"]
          profile = request.form["profile"]
          alamat = request.form["alamat"]
          nama_gambar = request.files["gambarStruktur"]
          currentStruktur = db.struktur.find_one({'_id': ObjectId(id)})
          current_image = currentStruktur.get('gambarStruktur', None)
          today=datetime.now()
          mytime = today.strftime('%Y-%m-%d-%H-%m-%S')
          doc = {
               "sejarah": sejarah,
               "profile": profile,
               "alamat": alamat,
               
          }
          if nama_gambar:
            if current_image:
               current_image_path = os.path.join('static/fotoStruktur', current_image)
               if os.path.exists(current_image_path):
                  os.remove(current_image_path)
            extension = nama_gambar.filename.split('.')[-1]
            nama_file_gambar = f'struktur-{mytime}.{extension}'
            file_path =f'static/fotoStruktur/{nama_file_gambar}'
            nama_gambar.save(file_path)
            doc['gambarStruktur']=nama_file_gambar
          db.struktur.update_one({'_id':ObjectId(id)},{"$set":doc})
          return redirect(url_for('AdminProfileSekolah'))
   id = ObjectId(_id)
   struktur = list(db.struktur.find({"_id":id}))
   return render_template('admin/profileSekolah/editProfileSekolah.html',struktur = struktur)

# profileSekolahAdmin end


# staffAdmin start

# staff 
@app.route('/adminStaff',methods=['GET'])
def AdminStaff():
   gurustaf =  list(db.gurustaff.find({}))
   print (gurustaf)
   return render_template('admin/gurustaff/staff.html', gurustaf=gurustaf)

# edit staff
@app.route('/adminEditStaff/<_id>',methods=['GET','POST'])
def AdminEditStaff(_id):
   if request.method=='POST':
      id=request.form['_id']
      nama=request.form['nama']
      nama_gambar= request.files['gambar']
      currentStaff = db.gurustaff.find_one({'_id': ObjectId(id)})
      current_image = currentStaff.get('gambar', None)
      doc={
            'nama': nama
         }
      today=datetime.now()
      mytime = today.strftime('%Y-%m-%d-%H-%m-%S')

      if nama_gambar:
         if current_image:
               current_image_path = os.path.join('static/fotostaff', current_image)
               if os.path.exists(current_image_path):
                  os.remove(current_image_path)
         extension = nama_gambar.filename.split('.')[-1]
         nama_file_gambar = f'staff-{mytime}.{extension}'
         file_path =f'static/fotostaff/{nama_file_gambar}'
         nama_gambar.save(file_path)
         doc['gambar']=nama_file_gambar
      db.gurustaff.update_one({'_id':ObjectId(id)},{'$set':doc})
      return redirect(url_for('AdminStaff'))
   gurustaff = list(db.gurustaff.find({'_id':ObjectId(_id)}))
   return render_template('admin/gurustaff/editstaff.html',gurustaff=gurustaff)


@app.route('/adminDeleteStaff/<_id>',methods=['GET','POST'])
def AdminDeleteStaff(_id):
   currentStaff = db.gurustaff.find_one({'_id': ObjectId(_id)})
   current_image = currentStaff.get('gambar', None)
   if current_image:
      current_image_path = os.path.join('static/fotostaff', current_image)
      if os.path.exists(current_image_path):
         os.remove(current_image_path)
   db.gurustaff.delete_one({'_id':ObjectId(_id)})
   return redirect(url_for('AdminStaff'))

# add staff
@app.route('/adminAddStaff',methods=['GET','POST'])
def AdminAddStaff():
   if request.method=='POST':
      # ambil input
      nama=request.form.get('nama')
      nama_gambar= request.files['gambar']
      
      today=datetime.now()
      mytime = today.strftime('%Y-%m-%d-%H-%m-%S')

      if nama_gambar:
         extension = nama_gambar.filename.split('.')[-1]
         nama_file_gambar = f'staff-{mytime}.{extension}'
         file_path =f'static/fotoStaff/{nama_file_gambar}'
         nama_gambar.save(file_path)
      else :
         nama_gambar=None
      doc = {
            'nama':nama,
            'gambar':nama_file_gambar   
        }
      db.gurustaff.insert_one(doc)
      return redirect(url_for('AdminStaff'))
   return render_template('admin/gurustaff/addStaff.html')

# staffAdmin end


# berita start

# berita
@app.route('/adminBerita',methods=['GET'])
def AdminBerita():
   Berita =  list(db.berita.find({}))
   print (Berita)
   return render_template('admin/berita/berita.html', Berita=Berita)

# edit berita
@app.route('/adminEditBerita/<_id>',methods=['GET','POST'])
def AdminEditBerita(_id):
   if request.method=='POST':
      id=request.form['_id']
      Deskripsi=request.form['Deskripsi']
      nama_gambar= request.files['gambar']
      currentBerita = db.berita.find_one({'_id': ObjectId(id)})
      current_image = currentBerita.get('gambar', None)
      doc={
            'Deskripsi': Deskripsi
         }
      today=datetime.now()
      mytime = today.strftime('%Y-%m-%d-%H-%m-%S')

      if nama_gambar:
         if current_image:
               current_image_path = os.path.join('static/fotoBerita', current_image)
               if os.path.exists(current_image_path):
                  os.remove(current_image_path)
         extension = nama_gambar.filename.split('.')[-1]
         nama_file_gambar = f'berita-{mytime}.{extension}'
         file_path =f'static/fotoBerita/{nama_file_gambar}'
         nama_gambar.save(file_path)
         doc['gambar']=nama_file_gambar
      db.berita.update_one({'_id':ObjectId(id)},{'$set':doc})
      return redirect(url_for('AdminBerita'))
   berita = list(db.berita.find({'_id':ObjectId(_id)}))
   return render_template('admin/berita/editBerita.html',berita=berita)
   

# add berita
@app.route('/adminAddBerita',methods=['GET','POST'])
def AdminAddBerita():
   if request.method=='POST':
      # ambil input
      Deskripsi=request.form['Deskripsi']
      nama_gambar= request.files['gambar']
      
      today=datetime.now()
      mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    
      if nama_gambar:
         extension = nama_gambar.filename.split('.')[-1]
         nama_file_gambar = f'Berita-{mytime}.{extension}'
         file_path =f'static/fotoBerita/{nama_file_gambar}'
         nama_gambar.save(file_path)
      else :
         nama_gambar=None
      doc = {
            'Deskripsi':Deskripsi,
            'gambar':nama_file_gambar,
            
        }
      db.berita.insert_one(doc)
      return redirect(url_for('AdminBerita'))
   return render_template('admin/berita/addBerita.html')

@app.route('/adminDeleteBerita/<_id>',methods=['GET','POST'])
def AdminDeleteBerita(_id):
   currentdeskripsi= db.berita.find_one({'_id': ObjectId(_id)})
   current_image = currentdeskripsi.get('gambar', None)
   if current_image:
      current_image_path = os.path.join('static/fotoBerita', current_image)
      if os.path.exists(current_image_path):
         os.remove(current_image_path)
   db.berita.delete_one({'_id':ObjectId(_id)})
   return redirect(url_for('AdminBerita'))


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
   return render_template('admin/fasilitas/fasilitas.html',fasilitas=fasilitas)

# edit fasilitas 
@app.route('/adminEditFasilitas/<_id>',methods=['GET','POST'])
def AdminEditFasilitas(_id):
   if request.method=='POST':
      id=request.form['_id']
      nama=request.form['namaFasilitas']
      deskripsi=request.form['deskripsiFasilitas']
         
      nama_gambar= request.files['gambarFasilitas']
      currentFasilitas = db.fasilitas.find_one({'_id': ObjectId(id)})
      current_image = currentFasilitas.get('gambarFasilitas', None)
      doc={
            'namaFasilitas': nama,
            'deskripsiFasilitas':deskripsi
         }
      
      today=datetime.now()
      mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
      
      if nama_gambar: 
         if current_image:
            current_image_path = os.path.join('static/fotoFasilitas', current_image)
            if os.path.exists(current_image_path):
               os.remove(current_image_path)        
         extension = nama_gambar.filename.split('.')[-1]
         nama_file_gambar = f'fasilitas-{mytime}.{extension}'
         file_path =f'static/fotoFasilitas/{nama_file_gambar}'
         nama_gambar.save(file_path)
         doc['gambarFasilitas']=nama_file_gambar
         
      db.fasilitas.update_one({'_id':ObjectId(id)},{'$set':doc})
      return redirect(url_for('AdminFasilitas'))
      
   fasilitas = list(db.fasilitas.find({'_id':ObjectId(_id)}))
   return render_template('admin/fasilitas/editFasilitas.html',fasilitas=fasilitas)

# add fasilitas
@app.route('/adminAddFasilitas',methods=['GET','POST'])
def AdminAddFasilitas():
   if request.method=='POST':
      # ambil input
      nama=request.form['namaFasilitas']
      deskripsi=request.form['deskripsiFasilitas']
      
      nama_gambar= request.files['gambarFasilitas']
      
      today=datetime.now()
      mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    
      if nama_gambar:
         extension = nama_gambar.filename.split('.')[-1]
         nama_file_gambar = f'fasilitas-{mytime}.{extension}'
         file_path =f'static/fotoFasilitas/{nama_file_gambar}'
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
   currentFasilitas = db.fasilitas.find_one({'_id': ObjectId(_id)})
   current_image = currentFasilitas.get('gambarFasilitas', None)
   if current_image:
      current_image_path = os.path.join('static/fotoFasilitas', current_image)
      if os.path.exists(current_image_path):
         os.remove(current_image_path) 
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