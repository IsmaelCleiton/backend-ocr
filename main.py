from flask import Flask,request,redirect,flash
import cv2
import pytesseract
import numpy as np


pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"


app = Flask("OCR")

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

RG_FIELDS = {'NOME', 'FILIAÇÃO', 'DATA NASCIMENTO', 'ORGÃO EXPEDIDOR','NATURALIDADE'}

@app.route('/')
def home():
    return redirect('/lerdocumento')

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/lerdocumento", methods = ['POST','GET'])
def lerDocumento():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Arquivo não enviado')
            return redirect('/')
        file = request.files['file']
        if file.filename == '':
            flash('Arquivo não selecionado')
            return redirect('/')
        if file and allowed_file(file.filename):
            arr = np.asarray(bytearray(file.read()), dtype=np.uint8)
            img = cv2.imdecode(arr,-1)
            pytesseract.get_languages(config='')
            result = pytesseract.image_to_string(img, lang='por')
            return {
                'document_id':'EM BREVE',
                'texto': result,
            }
    return  '''
            <!doctype html>
            <title>Carregue seu RG</title>
            <h1>Upload</h1>
            <form method=post enctype=multipart/form-data>
            <input type=file name=file>
            <input type=submit value=Upload>
            </form>
            '''
    
    # def identificarDocumento(text):
    #     return
    # def isRG(text):
    #     return

        

app.run()
