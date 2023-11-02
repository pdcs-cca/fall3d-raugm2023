import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.animation import FuncAnimation


def update(num, image_list, img):
    img.set_data(image_list[num])
    return img,

def crear_animacion(working_path,varName,date,hora,altura):

    arreglo_imagenes = []
    for i in range(1, 10): 
        imag = plt.imread(f'{working_path}/{varName}_{date}_{hora}_{altura}_{i:03}.png') 
        arreglo_imagenes.append(imag)
    fig = plt.figure()
    # Crea un objeto Axes
    ax = plt.axes([0, 0, 1, 1])
    ax.axis('off')
    plt.close()

    # Crea una imagen en blanco
    img = ax.imshow(arreglo_imagenes[0])
    animacion = FuncAnimation(fig, update, frames=range(len(arreglo_imagenes)), fargs=[arreglo_imagenes, img],
                  interval=200, blit=True)
    return animacion




