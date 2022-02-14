
from dataclasses import dataclass
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cv2

def main():
    st.title('Analizando imagenes del fondo optico ocular!!!')
    st.sidebar.header('Parametros')

    #funcion para poner los parametrso en el sidebar
    def user_input_parameters(colum,fila):
        x = st.sidebar.slider('x', 0,fila-52,int(fila/2))
        y = st.sidebar.slider('y', 0,colum-52,int(colum/2))
        data = {'x': x,
                'y': y
                }
        features = pd.DataFrame(data, index=[0])
        return features

    
    x1 = "PerfilDelianApp es una WebApp con la cual podras seleccionar una parte de la imagen para analizarla y mostrar el perfil de linea.\n Los parametros son :\n\n"
    x2 = "$x$ : Abscisa del recorte de la imagen \n\n"
    x3 = "$y$ : Ordenada del recorte de la imagen \n\n"
    x4 = "$Lado$ : Cantidad de pixeles en el recorte\n\n"
    x5 = "$Perfil$ : La fila del recorte de la imagen que se dibujara"
    st.subheader(x1+x2+x3+x4+x5)
    #st.subheader(x1)
    #st.text(x2+x3+x4+x5)
    #st.latex(r'''Hola mundo''')
    #st.write(df)

    uploaded_file = st.file_uploader("",type="jpg")

    if uploaded_file is not None:
        # Convert the file to an opencv image.
        
        
        print("Nombre del archivo : ",str(uploaded_file))
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)

        dim_img = np.shape(opencv_image)
        df = user_input_parameters(dim_img[0],dim_img[1])

        #st.subheader(dim_img)

        x=df['x'][0]
        y=df['y'][0]

        #long = st.sidebar.slider('long', 10,20,30)
        
        #print(dim_img[0])
        #print(x)
        #print(min(dim_img[0]-x,dim_img[1]-y))
        #print(dim_img[0]-x , dim_img[1]-y)
        max_l = min(dim_img[1]-x-52,dim_img[0]-y-52)

        print(x,dim_img[1]-52)
        print("hola mubndo",max_l)
        if ( (x ==dim_img[1]-52) or (y ==dim_img[0]-52)  ):
            print("hola 2")
            long = st.sidebar.slider('lado',48,50,49)
        else:
            long = st.sidebar.slider('lado',50,int(max_l)-2,50)

        
        perfil = st.sidebar.slider('perfil',0,long,int(long/2))
        
        x0=np.array(range(x,x+long))
        y0=np.ones(long)*(y+long)

        x2=np.array(range(x,x+long))
        y2=np.ones(long)*y

        x1=np.ones(long)*x
        y1=np.array(range(y,y+long))

        x3=np.ones(long)*(x+long)
        y3=np.array(range(y,y+long))

        z=perfil
        x_blanca=np.array(range(0,long))
        y_blanca=np.ones(long)*z


        fig2 = plt.figure(figsize=(10,10))
        ax = fig2.subplots()
        #ax[0].axis("off")
        #ax[0].imshow(opencv_image,cmap='gray')
        #ax[0].axis("off")
        ax.imshow(opencv_image,cmap='gray')
        ax.plot(x0,y0,'--w')
        ax.plot(x1,y1,'--w')
        ax.plot(x2,y2,'--w')
        ax.plot(x3,y3,'--w')
        
        fig = plt.figure(figsize=(20,8))
        ax = fig.subplots(1,2)
        q= opencv_image[y:y+long,x:x+long]
        ax[0].set_title("Recorte de la imagen - banda verde")
        ax[0].imshow(q[:,:,1],cmap='gray')
        ax[0].plot(x_blanca,y_blanca,'--r')
        #ax[1].axis("off")

        ax[1].set_title("Perfil de linea")
        ax[1].plot(q[0:long,z,1],color='b')
        #ax[2].axis("off")

        st.pyplot(fig2)
        st.pyplot(fig)
        
        


if __name__ == '__main__':
    main()