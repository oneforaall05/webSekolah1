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

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] =True
SECRET_KEY = "S4nd4l&sp1r1t_"
# TOKEN_KEY = "P1@_M3raLe0"
TOKEN_KEY = "mytoken"
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
      # print(username_receive)
      # print(password_receive)
      pw_hash = hashlib.sha256(password_receive.encode("utf-8")).hexdigest()
      # print(pw_hash)
      result = db.admin.find_one(
        {
            "username": username_receive,
            "password": pw_hash,
        }
      )
      if result:
         # print("sampai sini")
         payload = {
         "id": username_receive,
         # the token will be valid for 24 hours
         "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
         }
         # print(payload["id"],payload["exp"])
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
    token_receive = request.cookies.get(TOKEN_KEY)
   #  print(token_receive)
   #  print(SECRET_KEY)
   #  print(TOKEN_KEY)
    try:
      # print("masuk1")
      payload = jwt.decode(
            token_receive, SECRET_KEY, algorithms='HS256'
      )
      # userInfo = db.admin.find_one({'username':payload.get('id')})
      # print(userInfo)
      # print(payload+'yes')    
      struktur = list(db.struktur.find({}))
      return render_template('admin/profileSekolah/profileSekolah.html',struktur = struktur)
    except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
    except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))
    
       
      

# edit profile sekolah
@app.route('/adminEditProfileSekolah/<_id>',methods=['GET','POST'])
def AdminEditProfileSekolah(_id):
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
         payload = jwt.decode(
            token_receive, SECRET_KEY, algorithms='HS256'
         )
         if request.method == "POST":
               id = request.form["_id"]
               sejarah = request.form["sejarah"].strip()
               profile = request.form["profile"].strip()
               alamat = request.form["alamat"].strip()
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
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))
# profileSekolahAdmin end


# staffAdmin start

# staff 
@app.route('/adminStaff',methods=['GET'])
def AdminStaff():
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
   
      gurustaf =  list(db.gurustaff.find({}))
      print (gurustaf)
      return render_template('admin/gurustaff/staff.html', gurustaf=gurustaf)
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))

# edit staff
@app.route('/adminEditStaff/<_id>',methods=['GET','POST'])
def AdminEditStaff(_id):
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
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
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))


@app.route('/adminDeleteStaff/<_id>',methods=['GET','POST'])
def AdminDeleteStaff(_id):
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
      currentStaff = db.gurustaff.find_one({'_id': ObjectId(_id)})
      current_image = currentStaff.get('gambar', None)
      if current_image:
         current_image_path = os.path.join('static/fotostaff', current_image)
         if os.path.exists(current_image_path):
            os.remove(current_image_path)
      db.gurustaff.delete_one({'_id':ObjectId(_id)})
      return redirect(url_for('AdminStaff'))
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))

# add staff
@app.route('/adminAddStaff',methods=['GET','POST'])
def AdminAddStaff():
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
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
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))

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
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
      if request.method=='POST':
         id=request.form['_id']
         judul=request.form['judul']
         nama_gambar= request.files['gambar']
         Deskripsi=request.form['Deskripsi']
         currentBerita = db.berita.find_one({'_id': ObjectId(id)})
         current_image = currentBerita.get('gambar', None)
         doc={
               'judul' : judul,
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
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))
   

# add berita
@app.route('/adminAddBerita',methods=['GET','POST'])
def AdminAddBerita():
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
      if request.method=='POST':
         # ambil input
         nama_gambar= request.files['gambar']
         judul=request.form['judul']
         Deskripsi=request.form['Deskripsi']
         
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
               'gambar':nama_file_gambar,
               'judul' : judul,
               'Deskripsi':Deskripsi
               
         }
         db.berita.insert_one(doc)
         return redirect(url_for('AdminBerita'))
      return render_template('admin/berita/addBerita.html')
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))

# delete berita
@app.route('/adminDeleteBerita/<_id>',methods=['GET','POST'])
def AdminDeleteBerita(_id):
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
      currentdeskripsi= db.berita.find_one({'_id': ObjectId(_id)})
      current_image = currentdeskripsi.get('gambar', None)
      if current_image:
         current_image_path = os.path.join('static/fotoBerita', current_image)
         if os.path.exists(current_image_path):
            os.remove(current_image_path)
      
      db.berita.delete_one({'_id':ObjectId(_id)})
      db.komentar.delete_many({'berita_id':ObjectId(_id)})
      return redirect(url_for('AdminBerita'))
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))


# komentar
@app.route('/adminDataKomentar/<_id>',methods=['GET',"POST"])
def AdminDataKomentar(_id):
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
      komentar = list(db.komentar.find({'berita_id':ObjectId(_id)}))
      return render_template('admin/berita/dataKomentar.html',datas = komentar)
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))

# delete komentar
@app.route('/adminDeleteKomentar/<_id>', methods = ['GET','POST'])
def AdminDeleteKomentar(_id):
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
      currentKomentar = db.komentar.find_one({'_id':ObjectId(_id)})
      currentBerita = currentKomentar.get("berita_id")
      print(currentBerita)
      db.komentar.delete_one({"_id":ObjectId(_id)})
      return redirect(url_for('AdminDataKomentar',_id = currentBerita))
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))

# berita end


# pendaftaranAdmin start

# data pendaftaran
@app.route('/adminDataDaftar',methods=['GET','POST'])
def AdminDataDaftar():
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
      if request.method == 'POST':
         thn = request.form['tahun']
         dataDaftar = list(db.pendaftaran.find({'tahun': thn}))
         pendaftaran = list(db.pendaftaran.find({}))
         tahun = set()
         for dataThn in pendaftaran:
            tahun.add(dataThn.get('tahun'))

         year = list(tahun)
         year.reverse()
         years=year

         
      
         return render_template('admin/pendaftaran/dataDaftar.html', tahun=years,data=dataDaftar,thn=thn)

      pendaftaran = list(db.pendaftaran.find({}))
      tahun = set()
      for dataThn in pendaftaran:
         tahun.add(dataThn.get('tahun'))

      year = list(tahun)
      year.reverse()
      years=year
      
      today=datetime.now()
      mytime = today.strftime('%Y')
      thn=mytime
      dataDaftar = list(db.pendaftaran.find({'tahun': thn}))
      
      return render_template('admin/pendaftaran/dataDaftar.html', tahun=years,thn=thn,data=dataDaftar)

   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))

# detail pendaftaran
@app.route("/adminDetailDaftar/<_id>", methods=['GET','POST'])
def AdminDetailDaftar(_id):
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
      
      id=ObjectId(_id)
      detail=db.pendaftaran.find_one({'_id':id})
      return render_template('admin/pendaftaran/detailDaftar.html',data=detail)
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))

# edit data pendaftaran
@app.route('/adminEditDaftar/<_id>',methods=['GET','POST'])
def AdminEditDaftar(_id):
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
      if request.method=='POST':
         nama=request.form['nama'].strip()
         jenisKelamin=request.form['jenisKelamin'].strip()
         nik=request.form['nik'].strip()
         ttl=request.form['ttl'].strip()
         agama=request.form['agama'].strip()
         alamat=request.form['alamat'].strip()
         tempatTinggal=request.form['tempatTinggal'].strip()
         transportasi=request.form['transportasi'].strip()
         namaAyah=request.form['namaAyah'].strip()
         ttlAyah=request.form['ttlAyah'].strip()
         pendidikanAyah=request.form['pendidikanAyah'].strip()
         pekerjaanAyah=request.form['pekerjaanAyah'].strip()
         nomorAyah=request.form['nomorAyah'].strip()
         namaIbu=request.form['namaIbu'].strip()
         ttlIbu=request.form['ttlIbu'].strip()
         pendidikanIbu=request.form['pendidikanIbu'].strip()
         pekerjaanIbu=request.form['pekerjaanIbu'].strip()
         nomorIbu=request.form['nomorIbu'].strip()
         tinggi=request.form['tinggi'].strip()
         berat=request.form['berat'].strip()
         jarakSekolah=request.form['jarakSekolah'].strip()
         waktuSekolah=request.form['waktuSekolah'].strip()
         anakKe=request.form['anakKe'].strip()
         saudara=request.form['jumlahSaudara'].strip()
         
         doc={
            'nama':nama,
            'jk':jenisKelamin,
            'nik':nik,
            'ttl':ttl,
            'agama':agama,
            'alamat':alamat,
            't_tinggal':tempatTinggal,
            'transportasi':transportasi,
            'nama_ayah':namaAyah,
            'ttl_ayah':ttlAyah,
            'pendidikan_ayah':pendidikanAyah,
            'pekerjaan_ayah':pekerjaanAyah,
            'nomor_Hp_ayah':nomorAyah,
            'nama_Ibu':namaIbu,
            'ttl_Ibu':ttlIbu,
            'pendidikan_Ibu':pendidikanIbu,
            'pekerjaan_Ibu':pekerjaanIbu,
            'nomor_Hp_Ibu':nomorIbu,
            'tinggi':tinggi,
            'berat':berat,
            'jarak_sekolah':jarakSekolah,
            'waktu_sekolah':waktuSekolah,
            'anak_ke':anakKe,
            'saudara':saudara
         }
         id=ObjectId(_id)
         db.pendaftaran.update_one({'_id':id},{'$set':doc})
         return redirect(url_for('AdminDetailDaftar',_id=_id))
      id=ObjectId(_id)
      detail=db.pendaftaran.find_one({'_id':id})
      return render_template('admin/pendaftaran/editDaftar.html',data=detail)
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))

# pendaftaranAdmin end


# fasilitas start

# fasilitas
@app.route('/adminFasilitas',methods=['GET'])
def AdminFasilitas():
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
      fasilitas =  list(db.fasilitas.find({}))
      return render_template('admin/fasilitas/fasilitas.html',fasilitas=fasilitas)
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))

# edit fasilitas 
@app.route('/adminEditFasilitas/<_id>',methods=['GET','POST'])
def AdminEditFasilitas(_id):
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
      if request.method=='POST':
         id=request.form['_id'].strip()
         nama=request.form['namaFasilitas'].strip()
         deskripsi=request.form['deskripsiFasilitas'].strip()
            
         nama_gambar= request.files['gambarFasilitas'].strip()
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
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))

# add fasilitas
@app.route('/adminAddFasilitas',methods=['GET','POST'])
def AdminAddFasilitas():
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
      if request.method=='POST':
         # ambil input
         nama=request.form['namaFasilitas'].strip()
         deskripsi=request.form['deskripsiFasilitas'].strip()
         
         nama_gambar= request.files['gambarFasilitas'].strip()
         
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
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))

# delete fasilitas
@app.route('/adminDeleteFasilitas/<_id>',methods=['GET','POST'])
def AdminDeleteFasilitas(_id):
   token_receive = request.cookies.get(TOKEN_KEY)
   try:
      payload = jwt.decode(
         token_receive, SECRET_KEY, algorithms='HS256'
      )
      currentFasilitas = db.fasilitas.find_one({'_id': ObjectId(_id)})
      current_image = currentFasilitas.get('gambarFasilitas', None)
      if current_image:
         current_image_path = os.path.join('static/fotoFasilitas', current_image)
         if os.path.exists(current_image_path):
            os.remove(current_image_path) 
      db.fasilitas.delete_one({'_id':ObjectId(_id)})
      return redirect(url_for('AdminFasilitas'))
   except jwt.ExpiredSignatureError:
       return redirect(url_for("adminLogin",msg="session expired , lets try to login"))
   except jwt.exceptions.DecodeError:
       return redirect(url_for("adminLogin",msg="something wrong with your loggin"))
 
@app.route("/test",methods=['GET','POST'])
def test():
   if request.method == 'POST':
      thn = request.form['tahun']
      dataDaftar = list(db.pendaftaran.find({'tahun': thn}))
      pendaftaran = list(db.pendaftaran.find({}))
      tahun = set()
      for dataThn in pendaftaran:
         tahun.add(dataThn.get('tahun'))

      year = list(tahun)
      year.reverse()
      years=year
      print(years)
      
   
      return render_template('admin/pendaftaran/dataDaftar.html', tahun=years,data=dataDaftar,thn=thn)

   pendaftaran = list(db.pendaftaran.find({}))
   tahun = set()
   for dataThn in pendaftaran:
      tahun.add(dataThn.get('tahun'))

   year = list(tahun)
   year.reverse()
   years=year
   print(years)
   
   return render_template('admin/pendaftaran/dataDaftar.html', tahun=years)
# fasilitas end


# admin end

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)