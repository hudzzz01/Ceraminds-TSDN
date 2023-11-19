# INI KODE DEBUGGING NYA

from PIL import Image, ImageDraw
import easyocr
import easyOcr

def fillGambar(path,box):
    print("box",box)
    # Load gambar
    image_path = path
    image = Image.open(image_path)

    # Inisialisasi EasyOCR
    reader = easyocr.Reader(['en'], gpu=False) #CONTOHNYA PAKE INGGRIS

    # Deteksi teks pada gambar
    #results = reader.readtext(image_path)
    results = easyOcr.bacaGambar(path)["box"]
    print("Output Results: ", results)

    # Memproses hasil deteksi teks
    draw = ImageDraw.Draw(image)
    for (bbox, text_detected, ini_gatau_apaan_tapi_kayanya_akurasi), iter in zip(results, range(len(results))):
        print(f"\nini iterasi ke {iter+1}")
        print(f"koordinat bounding box: {bbox}, \ntext_detected: {text_detected}, \nini_gatau_apaan_tapi_kayanya_akurasi: {ini_gatau_apaan_tapi_kayanya_akurasi}")
        # Mendapatkan koordinat kotak
        # yang dimbil cuma koordinat titik kiri atas dan titik kanan bawah
        x1, y1 = map(int, bbox[0])
        print(f"x1 dan y1 iterasi ke {iter+1}: {x1}, {y1}")
        x2, y2 = map(int, bbox[2])
        print(f"x2 dan y2 iterasi ke {iter+1}: {x2}, {y2}")

        # Menggambar kotak hitam pada teks yang terdeteksi
        draw.rectangle([(x1, y1), (x2, y2)], fill='black')

    # Menyimpan gambar hasil
    output_path = 'uploads/output_gambar.jpg'
    image.save(output_path)
    return {
        'path' : "output_gambar.jpg"
    }