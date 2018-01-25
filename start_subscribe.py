from tkinter import *
import os
import webbrowser
import time
import cv2
import numpy as np
import pyscreenshot as ImageGrab
import pyautogui


def find_patt(image, patt, thres):
    img_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (patt_H, patt_W) = patt.shape[:2]
    res = cv2.matchTemplate(img_grey, patt, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res > thres)
    return patt_H, patt_W, list(zip(*loc[::-1]))


def screen(name_img):
    # делаем скриншот только части экрана # X1,Y1,X2,Y2
    # для ускорения работы программы
    screenshot = ImageGrab.grab(bbox=(0, 0, 400, 400))

    img = np.array(screenshot.getdata(), dtype='uint8').reshape((screenshot.size[1], screenshot.size[0], 3))
    patt = cv2.imread(name_img, 0)
    h, w, points = find_patt(img, patt, 0.60)

    if len(points) != 0:
        pyautogui.moveTo(points[0][0] + w / 2, points[0][1] + h / 2)
        pyautogui.click()


def open_link(proof):
    # стандартный путь к браузеру
    ffpath = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'
    webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(ffpath), 1)
    ff = webbrowser.get('firefox')
    # ссылка
    ff.open_new_tab(proof)
    # засыпание на 8 секунд для прогрузки страницы
    time.sleep(8)
    screen('subscribe.png')
    screen('close.png')


def get_in():
    list = output.get(1.0, END).split()
    print(list[1])
    # забрасываем пруф
    for i in list:
        open_link(i)


def start_program():
    root_admin = Tk()
    root_admin.title('Subscribe')
    root_admin.minsize(430, 330)
    root_admin.resizable(width=False, height=False)

    # создаем текстовое окошко для вывода
    output = Text(root_admin, bg='white', font='Arial 12')
    output.place(x=20, y=70, width=390, height=250)

    scr = Scrollbar(root_admin, command=output.yview)  # создаем скролл бар
    output.configure(yscrollcommand=scr.set)
    scr.place(x=410, y=165)
    # данные для примера
    output.insert('0.0', 'https://www.instagram.com/nikolaitarnogradskii/\nhttps://www.instagram.com/eriksondr/')
    but3 = Button(root_admin, text='START', width=8, height=2, command=get_in)
    but3.place(x=20, y=10)

    root_admin.mainloop()


if __name__ == '__main__':
    start_program()
