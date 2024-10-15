import streamlit as st
import pandas as pd
import numpy as np

def stride(mat_orig, kernel, saltos):
    if kernel == "Vertical":
        kernel1 = np.array([[1,0,1],[1,0,1],[1,0,1]])
    elif kernel == "Horizontal":
        kernel1 = np.array([[1,1,1],[0,0,0],[1,1,1]])
    
    filas = ((mat_orig.shape[0] - kernel1.shape[0])/saltos) + 1
    columnas = ((mat_orig.shape[1] - kernel1.shape[1])/saltos) + 1
    resultado = np.zeros([int(filas),int(columnas)])
        
    for k in range(resultado.shape[0]):
        for i in range(resultado.shape[1]):
            resultado[k,i] = (kernel1 * mat_orig[(saltos*k+0):(3+saltos*k),(0+saltos*i):(3+saltos*i)]).sum()
    return resultado

def padding(mat_orig, n_pad):
    paddin_col = np.zeros([mat_orig.shape[0],n_pad])
    imagen_pad = np.concatenate((mat_orig, paddin_col), axis = 1)
    
    paddin_fil = np.zeros([n_pad,imagen_pad.shape[1]])
    imagen_pad = np.concatenate((imagen_pad, paddin_fil), axis = 0)
    
    paddin_col = np.zeros([imagen_pad.shape[0],n_pad])
    imagen_pad = np.concatenate((paddin_col,imagen_pad), axis = 1)
    
    paddin_fil = np.zeros([n_pad,imagen_pad.shape[1]])
    imagen_pad = np.concatenate((paddin_fil,imagen_pad), axis = 0)
    return imagen_pad

def stacking(mat_orig, n_mapas):
    mapas = []
    for _ in range(n_mapas):
        tipo = np.random.choice(['horizontal', 'vertical'])
        kernel = np.zeros((3, 3))
        if tipo == 'horizontal':
            kernel[0, :] = np.random.randint(1, 5, 3)
            kernel[2, :] = np.random.randint(1, 5, 3)
        else:
            kernel[:, 0] = np.random.randint(1, 5, 3) 
            kernel[:, 2] = np.random.randint(1, 5, 3)
        
        filas = (mat_orig.shape[0] - kernel.shape[0]) + 1
        columnas = (mat_orig.shape[1] - kernel.shape[1]) + 1
        resultado = np.zeros((filas, columnas))
    
        for k in range(filas):
            for i in range(columnas):
                matriz = mat_orig[k:k + kernel.shape[0], i:i + kernel.shape[1]]
                resultado[k, i] = (kernel * matriz).sum()
        
        mapas.append(resultado)
        
    
    return mapas

def max_pooling(mat_orig, saltos):
    kernel = 2
    filas = (mat_orig.shape[0] - kernel) // saltos + 1
    columnas = (mat_orig.shape[1] - kernel) // saltos + 1
    resultado = np.zeros((filas, columnas))
    
    for k in range(filas):
        for i in range(columnas):
            matriz = mat_orig[k * saltos:k * saltos + kernel, i * saltos:i * saltos + kernel]
            resultado[k, i] = np.max(matriz)
    
    return resultado

st.title("Transformaciones basicas para el procesamiento de imagenes")

archivo = st.file_uploader("Cargar archivo Excel", type=["xlsx"])
if archivo is not None:
    try:
        imagen = pd.read_excel(archivo, header=None)
        imagen = imagen.values
        opcion = st.selectbox("Seleecione la transformacion", ["","Convolución","Padding","Stride",
                                                               "Stacking","MaxPool"])
        if opcion == "Convolución":
            tipo = st.selectbox("Seleccione el tipo de kernel", ["Vertical","Horizontal"])
            if st.button("Calcular"):
                resultado = stride(mat_orig = imagen, kernel = tipo, saltos = 1)
                st.write("La matriz resultado es:")
                st.write(resultado)
        elif opcion == "Padding":
            agregado = st.number_input("Ingrese el número de filas para agregar", min_value=1, value=1)
            if st.button("Calcular"):
                resultado = padding(imagen,agregado)
                st.write("La matriz resultado es:")
                st.write(resultado)
        elif opcion == "Stride":
            kernel = st.selectbox("Seleccione el tipo de kernel", ["Vertical","Horizontal"])
            saltos = st.number_input("Ingrese el número de saltos", min_value=1, value=2)
            if st.button("Calcular"):
                resultado = stride(imagen, kernel, saltos)
                st.write("La matriz resultado es:")
                st.write(resultado)
        elif opcion == "Stacking":
            mapas = st.number_input("Ingrese la cantidad de mapas de caracteristicas", min_value=1, value = 5)
            if st.button("Calcular"):
                mapas = stacking(imagen, mapas)
                st.write("La matriz resultado es:")
                st.write(mapas)
        elif opcion == "MaxPool":
            saltos1 = st.number_input("Ingrese el número de saltos", min_value=1, value = 2)
            if st.button("Calcular"):
                resultado = max_pooling(imagen, saltos1)
                st.write("La matriz resultado es:")
                st.write(resultado)

    except Exception as e:
        st.error("Por favor, cargue un archivo válido.")