import PySimpleGUI as sg
import io
import cv2
import numpy as np
from PIL import Image

file_type = [("All files (*.*)", "*.*"),
            ("JPEG (*.jpg)", "*.jpg"),
            ("PNG (*.png)", "*.png"),
    ]
or_img = [[sg.Image(filename='', key='-or_img-')]]
re_img = [[sg.Image(filename='', key='-re_img-')]]
sg.theme('LightGreen')

layout = [
    [
        sg.Text("Image File"),
        sg.Input(size=(25,1), key="-FILE-"),
        sg.FileBrowse(file_types=file_type),
        sg.Button("Load"),
    ],
    [sg.Frame(title='Original',layout=or_img),sg.Frame(title='Preview',layout=re_img),],
    [sg.Radio('None', 'Radio', True, size=(10, 1)), 
        sg.Radio('Grayscale', 'Radio', size=(10, 1), key='-GRAY-')],
    [sg.Radio('Threshold', 'Radio', size=(10, 1), key='-THRESH-'),
        sg.Slider((0, 255), 128, 1, orientation='h', size=(40, 15), key='-THRESH SLIDER-')],
    [sg.Radio('Canny', 'Radio', size=(10, 1), key='-CANNY-'),
        sg.Slider((0, 255), 128, 1, orientation='h', size=(19.4, 15), key='-CANNY SLIDER A-'),
        sg.Slider((0, 255), 128, 1, orientation='h', size=(19.4, 15), key='-CANNY SLIDER B-')],
    [sg.Radio('Blur', 'Radio', size=(10, 1), key='-BLUR-'),
        sg.Slider((1, 10), 1, 1, orientation='h', size=(40, 15), key='-BLUR SLIDER-')],
    [sg.Radio("Hue", "Radio", size=(10, 1), key="-HUE-"),
        sg.Slider((0, 225), 0, 1, orientation="h", size=(40, 15), key="-HUE SLIDER-",)],
    [sg.Radio("Enhance", "Radio", size=(10, 1), key="-ENHANCE-"),
        sg.Slider((1, 255), 128, 1, orientation="h", size=(40, 15), key="-ENHANCE SLIDER-",)],
    [sg.Button('Exit', size=(10, 1)), sg.Button('Save', size=(10, 1)),]
 ]

image_load = False

window = sg.Window("Image Processor", layout, resizable=True)

while True:
    event, values = window.read(timeout=20)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == "Load":
        filename = values["-FILE-"]
        img = cv2.imread(str(filename), cv2.IMREAD_COLOR)
        m_img = img.copy()
           
        window['-THRESH SLIDER-'].update(128)
        window['-CANNY SLIDER A-'].update(128)
        window['-CANNY SLIDER B-'].update(128)
        window['-BLUR SLIDER-'].update(1)
        window['-HUE SLIDER-'].update(0) 
        window['-ENHANCE SLIDER-'].update(128) 
         
        image_load = True

    if image_load:
      
        if event == "Save" :
            save_path = f'{filename[:-4]}_edit.png'
            cv2.imwrite(save_path, m_img)
            sg.popup('Saved image')

        if values['-THRESH-'] :
            if values['-THRESH SLIDER-'] :
                _, m_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 
                    values['-THRESH SLIDER-'], 255, cv2.THRESH_BINARY)
                
        elif values['-CANNY-']:
                m_img = cv2.Canny(img, values['-CANNY SLIDER A-'], values['-CANNY SLIDER B-'])
        elif values['-BLUR-'] :
            if values['-BLUR SLIDER-']:
                m_img = cv2.GaussianBlur(img, (21, 21), values['-BLUR SLIDER-'])
        elif values['-HUE-']:
            m_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            m_img[:, :, 0] += int(values['-HUE SLIDER-'])
            m_img = cv2.cvtColor(m_img, cv2.COLOR_HSV2BGR)
        elif values['-ENHANCE-']:
            enh_val = values['-ENHANCE SLIDER-'] / 40
            clahe = cv2.createCLAHE(clipLimit=enh_val, tileGridSize=(8, 8))
            lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            lab[:, :, 0] = clahe.apply(lab[:, :, 0])
            m_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

        elif values['-GRAY-']:
            m_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if img.shape[1] > 600 :
            width = int((img.shape[1]) / (img.shape[1] / 600))
            height = int((img.shape[0]) / (img.shape[1] / 600))
            thumb = (width, height)
            img_thumb = cv2.resize(img, thumb, interpolation = cv2.INTER_AREA)
            m_img_thumb = cv2.resize(m_img, thumb, interpolation = cv2.INTER_AREA)
        else:
            img_thumb = img.copy()
            m_img_thumb = m_img.copy()
        

        imgbytes = cv2.imencode('.png', img_thumb)[1].tobytes()
        m_imgbytes = cv2.imencode('.png', m_img_thumb)[1].tobytes()        
        window['-or_img-'].update(data=imgbytes)      
        window['-re_img-'].update(data=m_imgbytes)
    
window.close()




