import PySimpleGUI as psg
import io
import cv2
import numpy as np
from PIL import Image

file_type = [("All files (*.*)", "*.*"),
            ("JPEG (*.jpg)", "*.jpg"),
            ("GIF (*.gif)", "*.gif"),
            ("PNG (*.png)", "*.png"),
    ]
or_img = [[psg.Image(filename='', key='-or_img-')]]
re_img = [[psg.Image(filename='', key='-re_img-')]]
psg.theme('LightGreen')

layout = [
    [
        psg.Text("Image File"),
        psg.Input(size=(25,1), key="-FILE-"),
        psg.FileBrowse(file_types=file_type),
        psg.Button("Load"),
    ],
    [psg.Frame(title='Original',layout=or_img),psg.Frame(title='Results',layout=re_img),],
    [psg.Radio('None', 'Radio', True, size=(10, 1))],
    [psg.Radio('threshold', 'Radio', size=(10, 1), key='-THRESH-'),
    psg.Slider((0, 255), 128, 1, orientation='h', size=(40, 15), key='-THRESH SLIDER-')],
    [psg.Radio('canny', 'Radio', size=(10, 1), key='-CANNY-'),
    psg.Slider((0, 255), 128, 1, orientation='h', size=(19.4, 15), key='-CANNY SLIDER A-'),
    psg.Slider((0, 255), 128, 1, orientation='h', size=(19.4, 15), key='-CANNY SLIDER B-')],
    [psg.Radio('blur', 'Radio', size=(10, 1), key='-BLUR-'),
    psg.Slider((1, 10), 1, 1, orientation='h', size=(40, 15), key='-BLUR SLIDER-')],
    [psg.Button('Exit', size=(10, 1)), psg.Button('Save', size=(10, 1))]
 ]

image_load = False

window = psg.Window("Image Processor", layout, resizable=True)

while True:
    event, values = window.read(timeout=20)
    if event == "Exit" or event == psg.WIN_CLOSED:
        break

    if event == "Load":
        filename = values["-FILE-"]
        img = cv2.imread(str(filename), cv2.IMREAD_COLOR)
        imgbytes = cv2.imencode('.png', img)[1].tobytes()
        m_img = img.copy()
        window['-or_img-'].update(data=imgbytes)
        window['-re_img-'].update(data=imgbytes)
        window['-THRESH SLIDER-'].update(128)
        window['-CANNY SLIDER A-'].update(128)
        window['-CANNY SLIDER B-'].update(128)
        window['-BLUR SLIDER-'].update(1)
              
        image_load = True

    if image_load:
        if event == "Save":
            save_path = f'{filename[:-4]}_edit.png'
            cv2.imwrite(save_path, m_img)
            psg.popup('Saved image')

        if values['-THRESH-'] :
            if values['-THRESH SLIDER-'] :
                _, m_img = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), values['-THRESH SLIDER-'], 255, cv2.THRESH_BINARY)
        elif values['-CANNY-']:
                m_img = cv2.Canny(img, values['-CANNY SLIDER A-'], values['-CANNY SLIDER B-'])
        elif values['-BLUR-'] :
            if values['-BLUR SLIDER-']:
                m_img = cv2.GaussianBlur(img, (21, 21), values['-BLUR SLIDER-'])
        else :
            m_img = img.copy()
        m_imgbytes = cv2.imencode('.png', m_img)[1].tobytes()              
        window['-re_img-'].update(data=m_imgbytes)
    
window.close()




