#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:23:49 2021

@author: Graciela Gaona Bernabé


Este programa etiqueta rostros conocidos (previamente codificados) en un video de youtube.

1. Se leen las imágenes del folder 'img/' o 'img1/' y se codifican utilizando la librería 
face_recognition
2. Se carga un video de youtube (librería pafy) dado un url, y se muestra en una ventana de opencv
3. Para cada frame del video se detectan todos los rostros y si corresponde a un rostro de una persona conocida
(de la carpeta 'img/' o 'img1/') entonces se etiqueta con el nombre correspondiente, en caso contrario
se etiqueta como 'desconocido'

"""

#Importar librerías
import face_recognition
import cv2
import os
import numpy as np
import pafy


#Cargar imágenes de una carpeta, recuperar el nombre de las personas a identificar
def load_images_from_folder(folder):
    images = []
    file_names = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
            file_names.append(filename.split('.')[0].replace('_',' '))
            
    return images,file_names


#Codificar imágenes de personas a identificar en el video
def encode_images(images):
    
    known_face_encodings = []
    
    for img in images:
        image_encoding = []
        image_encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(image_encoding)
    
    return known_face_encodings


#Detectar rostros y etiquetar con su nombre o como desconocido
def find_people(frame):
    
    #Redimensionar el video, para un procesamiento más rápido
    small_frame = cv2.resize(frame,(0,0),fx=0.5,fy=0.5)
    
    #convertir la images de BGR a RGB
    rgb_small_frame = small_frame[:,:,::-1]
    

    #Localizar todos los rostros en frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
   
    face_names = []
    for face_encoding in face_encodings:
        #Verificar si corresponde a un rostro conocido
        matches = face_recognition.compare_faces(encoded_images,face_encoding)
        name = "Desconocido"
    
        face_distances = face_recognition.face_distance(encoded_images,face_encoding)
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = name_images[best_match_index]
            
        face_names.append(name)
            
    
    #Mostrar resultados
    for (top,right,bottom,left),name in zip(face_locations,face_names):
        #Regresar a su escala normal
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2
        
        #Dibujar un rectángulo alrededor del rostro
        cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)
        
        #Colocar la etiqueta con el nombre correspondiente
        cv2.rectangle(frame,(left,bottom-15),(right,bottom),(0,0,255),cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame,name,(left+6,bottom-6),font,0.5,(255,255,255),1)
    
    return frame


#Leer video a partir de una url 
def read_video_from_url(url_video):
    vPafy = pafy.new(url_video)
    play = vPafy.getbest(preftype="mp4")
    
    cap = cv2.VideoCapture(play.url)
    
    while (True):
        #Obtener cada frame del video
        ret,frame = cap.read()
        #Identificar personas
        find_people(frame)
        #Mostrar el frame en una ventana de opencv
        cv2.imshow('frame',frame)
        
        
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break    
    
    cap.release()
    cv2.destroyAllWindows()

    
    

'''
Cargar imágenes de carpeta
'''
dir_name = "img1/"
images,name_images = load_images_from_folder(dir_name)
process_this_frame = True

if len(images)>0:
    #Imágenes codificadas
    encoded_images = encode_images(images)   
    url = 'https://www.youtube.com/watch?v=uuncphZu5E4'
    #Leer video
    read_video_from_url(url)
    
