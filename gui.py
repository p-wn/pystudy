import PySimpleGUI as psg
import os
import io
import cv2
import numpy as np
from PIL import Image, ImageTk

file_type = [("All files (*.*)", "*.*"),
            ("JPEG (*.jpg)", "*.jpg"),
            ("GIF (*.gif)", "*.gif"),
            ("PNG (*.png)", "*.png"),
    ]
ori_img = [[psg.Image(filename='', key='-ori_img-')]]
mod_img = [[psg.Image(filename='', key='-mod_img-')]]

def main() :
    psg.theme('Dark Blue 3')
    layout = [
        [
            psg.Text("Image File"),
            psg.Input(size=(25,1), key="-FILE-"),
            psg.FileBrowse(file_types=file_type),
            psg.Button("Load"),
        ],
        [psg.Frame(title='Original',layout=ori_img),psg.Frame(title='Results',layout=mod_img),],
        [psg.Radio('None', 'Radio', True, size=(10, 1))],
        [psg.Radio('threshold', 'Radio', size=(10, 1), key='-THRESH-'),
        psg.Slider((0, 255), 128, 1, orientation='h', size=(40, 15), key='-THRESH SLIDER-')],
        [psg.Radio('canny', 'Radio', size=(10, 1), key='-CANNY-'),
        psg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='-CANNY SLIDER A-'),
        psg.Slider((0, 255), 128, 1, orientation='h', size=(20, 15), key='-CANNY SLIDER B-')],
        [psg.Radio('blur', 'Radio', size=(10, 1), key='-BLUR-'),
        psg.Slider((1, 11), 1, 1, orientation='h', size=(40, 15), key='-BLUR SLIDER-')],
        [psg.Button('Exit', size=(10, 1)), psg.Button('Save', size=(10, 1))]

        
    ]
    window = psg.Window("Image View", layout, resizable=True)

    while True:
        event, values = window.read()
        if event == "Exit"or event == psg.WIN_CLOSED:
            break
        if event == "Load":
            filename = values["-FILE-"]
            if os.path.exists(filename):
                img = cv2.imread(str(filename), cv2.IMREAD_UNCHANGED)
                imgbytes = cv2.imencode('.png', img)[1].tobytes()
                m_img = img.copy()
                window['-ori_img-'].update(data=imgbytes)
                #window['-THRESH SLIDER-'].update(128)
               # window['-CANNY SLIDER A-'].update(128)
               # window['-CANNY SLIDER B-'].update(128)
                #window['-BLUR SLIDER-'].update(1)

                load = True
        if load:
            if event == "Save":
                out_path = f'{filename[:-4]}_r.png'
                cv2.imwrite(out_path, m_img)
                psg.popup('Saved image')

            elif values['-THRESH-']:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, m_img = cv2.threshold(img, values['-THRESH SLIDER-'], 255, cv2.THRESH_BINARY)
            elif values['-CANNY-']:
                m_img = cv2.Canny(img, values['-CANNY SLIDER A-'], values['-CANNY SLIDER B-'])
            elif values['-BLUR-']:
                m_img = cv2.GaussianBlur(img, (21, 21), values['-BLUR SLIDER-'])

                #imgbytes = cv2.imencode('.png', img)[1].tobytes()
            m_imgbytes = cv2.imencode('.png', m_img)[1].tobytes()
                
            window['-mod_img-'].update(data=m_imgbytes)
                #window["-IMAGE-"].update(data=image)
    window.close()

if __name__ == "__main__":
    main()


