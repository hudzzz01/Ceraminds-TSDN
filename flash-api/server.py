from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Untuk mengatasi masalah CORS
import os
import uuid

app = Flask(__name__)
CORS(app)  # Menambahkan CORS ke aplikasi Flask

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
def baca_gambar_ocr(path):
    try:
        return path
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return "Terjadi kesalahan: {e}"

def analisa_text(text):
    try:
        return text
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return "Terjadi kesalahan: {e}"

@app.route('/')
def home():
    return jsonify({
                "status" : "ok",
                "message" : "it's work dude",
                "data" : {
            
                }
            }) 

@app.route('/upload', methods=['POST', 'GET'])
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
            hasilBacaGambarUntukOcr = baca_gambar_ocr(path)
            hasilAnalisaText = analisa_text("text_yang_mau_di_analisa")
            
            return jsonify({
                "status" : "ok",
                "message" : "gambar berhasil di upload",
                "data" : {
                    "nama_file" : newFileName,
                    "lokasi" : "/uploaded/"+newFileName,
                    "keterangan" : {
                        "hasil_ocr " :  hasilBacaGambarUntukOcr,
                        "hasil_analisa_text" :  hasilBacaGambarUntukOcr,
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
    if request.method == "DELETE":
        #print(path)
        status = "ok"
        result = hapus_file("uploads/"+path)
        if result[0] == "G":
            status = "error"
        #print(result[0])
    
        
    return jsonify({
                "status" : status,
                "message" : result,
                "data" : {
                    "nama_file" : path,
                    "lokasi" : "/uploaded/"+path,
                }
            })


if __name__ == '__main__':
    app.run(debug=True)
