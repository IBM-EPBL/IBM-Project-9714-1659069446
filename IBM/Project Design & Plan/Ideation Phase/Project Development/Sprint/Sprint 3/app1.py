# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 12:19:41 2022

@author: Hp
"""
import numpy as np
import os
import tensorflow_hub as hub
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask,render_template,request,url_for
from logging import FileHandler,WARNING

app=Flask(__name__,template_folder='templates')
model=load_model("D:/skinlesion-classification-model/trained_model3skin.h5",custom_objects={'KerasLayer':hub.KerasLayer}
)

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)



dic={0:'Acne and Rosacea Photos', 1:'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions', 2:'Atopic Dermatitis Photos', 3:'Cellulitis Impetigo and other Bacterial Infections', 4:'Eczema Photos', 5:'Exanthems and Drug Eruptions', 6:'Herpes HPV and other STDs Photos',7: 'Lupus and other Connective Tissue diseases', 8:'Melanoma Skin Cancer Nevi and Moles',9: 'Scabies Lyme Disease and other Infestations and Bites', 10:'Seborrheic Keratoses and other Benign Tumors', 11:'Tinea Ringworm Candidiasis and other Fungal Infections',12: 'Vascular Tumors', 13:'Vasculitis Photos', 14:'Warts Molluscum and other Viral Infections'}



model.make_predict_function()


def predict_label(img_path):
    i = image.load_img(img_path, target_size=(299,299))
    i = image.img_to_array(i)
    i=np.expand_dims(i,axis=0)
    index=['Acne and Rosacea', 
           'Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions', 
           'Atopic Dermatitis', 
           'Cellulitis Impetigo and other Bacterial Infections', 
           'Eczema Photos', 'Exanthems and Drug Eruptions', 
           'Herpes HPV and other STDs',
           'Lupus and other Connective Tissue diseases', 
           'Melanoma Skin Cancer Nevi and Moles',
           'Scabies Lyme Disease and other Infestations and Bites', 
           'Seborrheic Keratoses and other Benign Tumors', 
           'Tinea Ringworm Candidiasis and other Fungal Infections',
           'Vascular Tumors',
           'Vasculitis', 
           'Warts Molluscum and other Viral Infections']
    pred=np.argmax(model.predict(i))
    return index[pred]

# routes
@app.route("//")
def main():
    return render_template("login.html")
database={"Kiruthika A":"123","Kiruthika P S":"456","Poomathi D":"789","Prithinga Devi":"910"}

@app.route('/form_login',methods=['GET', 'POST'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    if name1 not in database:
        return render_template('login.html',info='Invalid User')
    else:
        if database[name1]!=pwd:
            return render_template('login.html',info='Invalid Password')
        else:
            return render_template("indexf.html")

@app.route('/form_register',methods=['GET', 'POST'])
def main1():
    return render_template("register.html")
def register():
    name2=request.form['username']
    pwd2=request.form['password']
    if name2 in database:
        return render_template('register.html',info='Invalid Username')
    else:
        database[name2]=pwd2

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predict_label(img_path)

	return render_template("indexf.html", prediction = p, img_path = img_path)

@app.route("/logout")
def logout():
    return render_template("logout.html")
    
    
if __name__=='__main__':
    app.run(host='0.0.0.0', port=8892,debug=False)
    
    