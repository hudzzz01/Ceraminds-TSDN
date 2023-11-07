import Levenshtein

def cekSmilar(text):
    print("mengecek smilaity data pribadi")
    private_id= ["Nama", "Tempat/Tgl lahir", "Alamat", "RT", "RW", "Kelurahan", "Kel/Desa", "Kecamatan", "Agama", "Status Perkawinan", "Pekerjaan", "Kewarganegaraan", "NIK", "S.KOM", "M.T", "M.Kom", "Dr." "NIP.", "NIM"]

    smilar=[]
    
    for words in text:
        for id in private_id:
            distance = Levenshtein.distance(words, id)

            threshold = 2 #work on threshold

            if distance <= threshold:
                smilar.append(f'{words} and {id} are similar')
                print(f'{words} and {id} are similar')
    return smilar