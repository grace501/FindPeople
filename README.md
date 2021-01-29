# FindPeople
Programa en Python para identificar personas (previamente codificadas) en un video.

Este programa etiqueta rostros conocidos (previamente codificados) en un video de youtube.
1. Se leen las imágenes del folder 'img/' o 'img1/' y se codifican utilizando la librería 
face_recognition (https://github.com/ageitgey/face_recognition)
2. Se carga un video de youtube (librería pafy https://pypi.org/project/pafy/ ) dado un url, y se muestra en una ventana de opencv
3. Para cada frame del video se detectan todos los rostros y se determina: si corresponde a un rostro de una persona conocida
(de la carpeta 'img/' o 'img1/') entonces se etiqueta con el nombre correspondiente, en caso contrario
se etiqueta como 'desconocido'.
