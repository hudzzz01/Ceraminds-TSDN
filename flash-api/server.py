from flask import Flask, request, jsonify, send_from_directory,render_template
from flask_cors import CORS  # Untuk mengatasi masalah CORS
import os
import uuid
import easyOcr
import conn
import sqlite3
import fill
from PIL import Image, ImageDraw

box = []


app = Flask(__name__)
CORS(app)  # Menambahkan CORS ke aplikasi Flask

cursor = conn.cursor
connenction = conn.connection

# Direktori penyimpanan gambar
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#fungsi hapus file
def hapus_file(nama_file):
    try:
        os.remove(nama_file)
        return(f"File '{nama_file}' berhasil dihapus.")
    except OSError as e:
        return(f"Gagal menghapus file '{nama_file}': {e}")

# Fungsi untuk mengambil daftar gambar yang sudah diunggah
def get_uploaded_images():
    image_files = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
    return image_files

#fungsi read image
def fill_boinding_box(path):
    try:
        return path
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return "Terjadi kesalahan: {e}"

def ocr_analisa_text(text):
    try:
        return text
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return "Terjadi kesalahan: {e}"


@app.route('/index')
def upload_form():
    return render_template('upload.html')


@app.route('/')
def home():
    return jsonify({
                "status" : "ok",
                "message" : "it's work dude",
                "data" : {
            
                }
            }) 
    
@app.route('/cekIsiDb')
def cek_db():
    try :
        with sqlite3.connect("db/database.db") as con:
            query = "SELECT * FROM photo"
            cur = con.cursor()
            data = cur.execute(query).fetchall()
            con.commit()
            print("Data get successfully")  
            return jsonify({
                "status" : "ok",
                "message" : "data berhasil di ambil",
                "data" : data
            })     
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return jsonify({
                "status" : "err",
                "message" : "data gagal di ambil",
                "data" : ""
            })   
    
@app.route('/covering/<path:path>', methods=['POST', 'GET'])
def covering_image(path):
    print(path)
    if request.method == 'GET':
        print("test")
        try :
             with sqlite3.connect("db/database.db") as con:
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                cur.execute("select * from photo where id='e840af32-7189-4db7-aacd-5988a215038e_asli.jpg")
                rows = cur.fetchall()
                print(rows)
                print("Data get successfully")  
                print("boxxx ",box)
                return jsonify({
                    "status" : "ok",
                    "message" : "data berhasil di ambil",
                    "data" : rows
                })     
        except sqlite3.Error as e:
             print(f"Error: {e}")
             return jsonify({
                    "status" : "error",
                    "message" : "data gagal di ambil",
                    "data" : e
                })     

@app.route('/fillGambar', methods=['POST', 'GET'] )
def fillImage():
    if request.method == 'POST':
        data = request.get_json()
        path = "uploads/"+data["nama_file"]
        
        #nopal code
        try:
            print("boxx ",box)
            out = fill.fillGambar(path,box)
            return jsonify({"out": out})
        except Exception as e:
            print(e)
            return jsonify({"err": e})
            
        
        
       

@app.route('/analisaGambar', methods=['POST', 'GET'])
def upload_image():
    if request.method == 'POST':
        if 'photo' not in request.files:
            return jsonify({"message": "Tidak ada file yang diunggah"})

        photo = request.files['photo']
        if photo.filename == '':
            return jsonify({"message": "Nama file kosong"})

        if photo:
            newFileName = str(uuid.uuid4()) + "_" +"asli"+"."+photo.filename.split(".")[len(photo.filename.split("."))-1]
            path = os.path.join(app.config['UPLOAD_FOLDER'], newFileName)
            photo.save(path)
            #baca gambar
            #print(path)
            hasilBacaGambarUntukOcr = easyOcr.bacaGambar(path)
            #simpan ke db
            print("menyimpan bounding box <=:=> nama file")
            box = hasilBacaGambarUntukOcr["box"]
            
            
            
            try :
                with sqlite3.connect("db/database.db") as con:
                    insert_query = "INSERT INTO photo (id, Bounding_Box) VALUES (?, ?)"
                    data = (str(newFileName), str(hasilBacaGambarUntukOcr["box"]))
                    print(data)
                    cur = con.cursor()
                    cur.execute(insert_query, data)
                    con.commit()
                    msg = "Done"
                    print("Data inserted successfully")
                 
            except sqlite3.Error as e:
                print(f"Error: {e}")
                

            return jsonify({
                "status" : "ok",
                "message" : "gambar berhasil di upload",
                "data" : {
                    "nama_file" : newFileName,
                    "lokasi" : "/uploaded/"+newFileName,
                    "keterangan" : {
                        "hasil_ocr" :  {
                            "found" : hasilBacaGambarUntukOcr["found"],
                            "text-smilar-data-pribadi" : hasilBacaGambarUntukOcr["text-smilar-data-pribadi"]    
                        },
                    }
                }
            })

    elif request.method == 'GET':
        uploaded_images = get_uploaded_images()
        return jsonify({"uploaded_images": uploaded_images})
    
@app.route('/uploaded/<path:path>')
def send_report(path):
    print(path)
    return send_from_directory('uploads', path)

@app.route('/delete/<path:path>',methods=['DELETE'])
def delete_image(path):
    #path ini isinya nama file yak !!!!!
    if request.method == "DELETE":
        #print(path)
        status = "ok"
        result = hapus_file("uploads/"+path)
        if result[0] == "G":
            status = "error"
        #print(result[0])
    
        #menghapus data dari database
        try :
            with sqlite3.connect("db/database.db") as con:
                query = "DELETE FROM photo WHERE id = ?"
                data = (path,)
                print(data)
                cur = con.cursor()
                cur.execute(query, data)
                con.commit()
                print("Data deleted successfully")
                 
        except sqlite3.Error as e:
                print(f"Error: {e}")
        
    return jsonify({
                "status" : status,
                "message" : result,
                "data" : {
                    "nama_file" : path,
                    "lokasi" : "/uploaded/"+path,
                }
            })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

