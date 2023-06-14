import vk_api
import tkinter, time
import vk_captchasolver as vc
from threading import Thread
from random import randint
from config import *

sid, solving_captcha = None, None
VERSION = "v.0.1.0"

def sendmessage(msg, conv_id, to_conv = True, captcha_code = None, captcha_sid = None):
    if to_conv:
        user_id = 2000000000 + conv_id
    else:
        user_id = conv_id
    if debug: print("Jiberu ogan", user_id)
    return vk.messages.send(peer_id = user_id, message = msg, random_id = 0, captcha_sid = captcha_sid, captcha_key = captcha_code)

def edit_message(msg, msg_id, conv_id, to_conv=True, captcha_sid=None, captcha_code=None):
    if to_conv:
        user_id = 2000000000 + conv_id
    else:
        user_id = conv_id
    print(user_id)
    return vk.messages.edit(peer_id = user_id, message = msg, message_id = msg_id, random_id = 0, captcha_sid=captcha_sid, captcha_key = captcha_code)

def raidstart(conv_id, to_ls, counter_text):
    global counter, sid, solving_captcha
    while True:
        try:
            if anti_iris_mode.get():
                message_id = sendmessage("Ассаламалейкум!", conv_id, to_ls, captcha_sid=sid, captcha_code=solving_captcha)
                edit_message(3*msg+str(randint(1000,9999)), message_id, conv_id, to_ls, captcha_code = solving_captcha, captcha_sid = sid)
            else:
                sendmessage(3 * msg + str(randint(1000, 9999)), conv_id, to_ls, captcha_sid=sid, captcha_code=solving_captcha)
            counter += 1
            counter_text["text"] = "Жіберілді: " + str(counter)
        except vk_api.Captcha as captcha:
            if debug: print("Captcha needed. Solving...")
            sid = captcha.sid
            if debug: print(f"Captcha data {sid}")
            solving_captcha = vc.solve(sid=sid, s=1)
            if debug: print(f"Solved code {solving_captcha}")

def launcher():
    start_button.destroy()
    counter_text = tkinter.Label(text = "Жіберілді")
    counter_text.pack()
    Thread(target = raidstart, args=(int(conv_id.get()), to_ls.get(), counter_text)).start()

session = vk_api.VkApi(token = my_token)
vk = session.get_api()

root = tkinter.Tk()

counter = 0
to_ls = tkinter.BooleanVar()
to_ls.set(0)
anti_iris_mode = tkinter.BooleanVar()
anti_iris_mode.set(0)

root.title("StickMouse VK рейдері")

tkinter.Label(text = "Рейд баптауы...", font="Arial 22").pack()
tkinter.Label(text = "Рейд үшін Топ/Жеке хабарламалар ID").pack()
conv_id = tkinter.Entry()
conv_id.pack()
to_ls_checkbox = tkinter.Checkbutton(text = "Әңгімелесуге рейд", variable=to_ls)
to_ls_checkbox.pack()
to_antiiris_checkbox = tkinter.Checkbutton(text = "Ирис боттін аттап өту", variable = anti_iris_mode)
to_antiiris_checkbox.pack()
tkinter.Label(text = "Спам арада интервалы секундтерде(1; 0.05; 0.5)").pack()
timer = tkinter.Entry(text = "0.5")
timer.pack()
timer.insert(0, "0.5")
start_button = tkinter.Button(text = "Рейд бастау", command=launcher)
start_button.pack()

root.mainloop()

    

