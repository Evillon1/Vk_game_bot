#-------------------------------------------------------------------------#|#
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType             #|#
import vk_api                                                             #|#
import dont_touch as dt                                                   #|#
import keyboards as keyb                                                  #|#
import sqlite3                                                            #|#
import time                                                               #|#
import json                                                               #|#
from threading import Thread                                              #|#
import random                                                             #|#
#-------------------------------------------------------------------------#|#


##---------------------------------------------------------------MAIN--------------------------------------------------------##
vki = vk_api.VkApi(token=dt.TOK)                                                                                             ##
vk = vki.get_api()                                                                                                           ##
longpoll = VkBotLongPoll(vki, dt.ID)                                                                                         ##
                                                                                                                             ##
conn = sqlite3.connect('db.db', check_same_thread=False)                                                                     ##
c = conn.cursor()                                                                                                            ##
##---------------------------------------------------------------------------------------------------------------------------##




##---------------------------------------------------------------KEYBOARDS----------------------------------------------------------##
                                                                                                                                    ##
keyboard = {                                                                                                                        ##
    "one_time": False,                                                                                                              ##
    "buttons": [[                                                                                                                   ##
                 #{"action": {"type": "text", "payload": '{"button":"1"}', "label": "??????????"}, "color": "positive" },                ##
                 {"action": {"type": "text", "payload": '{"button":"4"}', "label": "????????????"}, "color": "secondary"},                ##
                 {"action": {"type": "text", "payload": '{"button":"5"}', "label": "????????????"}, "color": "secondary"},                ##
                 #{"action": {"type": "text", "payload": '{"button":"2"}', "label": "????????"}, "color": "primary"}
                 ],                   ##
                 [{"action": {"type": "text", "payload": '{"button":"3"}', "label": "????????"}, "color": "negative"},                  ##
                                                                                                                                    ##
               ]],                                                                                                                  ##
    "inline": False}                                                                                                                ##
                                                                                                                                    ##
market = {                                                                                                                          ##
    "one_time": False,                                                                                                              ##
    "buttons": [[                                                                                                                   ##
                 {"action": {"type": "text", "payload": '{"button":"6"}', "label": "??????????"}, "color": "secondary" },                ##
                 {"action": {"type": "text", "payload": '{"button":"7"}', "label": "??????????"}, "color": "secondary"},                 ##
                 {"action": {"type": "text", "payload": '{"button":"8"}', "label": "??????????????"}, "color": "secondary"}                ##
                                                                                                                                    ##
               ]],                                                                                                                  ##
    "inline": True}                                                                                                                 ##
                                                                                                                                    ##
                                                                                                                                    ##
                                                                                                                                    ##
                                                                                                                                    ##
start_button = {                                                                                                                    ##
    "one_time": False,                                                                                                              ##
    "buttons": [[                                                                                                                   ##
                {"action": {"type": "text", "payload": '{"command":"start"}', "label": "???????????? ????????????!"}, "color": "secondary"},    ##
               ]]}                                                                                                                  ##
                                                                                                                                    ##
start_button = json.dumps(start_button, ensure_ascii=False).encode('utf-8')                                                         ##
start_button = str(start_button.decode('utf-8'))                                                                                    ##
                                                                                                                                    ##
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')                                                                 ##
keyboard = str(keyboard.decode('utf-8'))                                                                                            ##
                                                                                                                                    ##
market = json.dumps(market, ensure_ascii=False).encode('utf-8')                                                                     ##
market = str(market.decode('utf-8'))                                                                                                ##
                                                                                                                                    ##
hide = {"buttons": []}                                                                                                              ##
hide = json.dumps(hide, ensure_ascii=False).encode('utf-8')                                                                         ##
hide = str(hide.decode('utf-8')) #keyboard=hide - ???????????? ??????????                                                                      ##
##----------------------------------------------------------------------------------------------------------------------------------##
def timer_status():
    c.execute("SELECT timer FROM user_info WHERE user_id={}".format(vk_id, ))
    return c.fetchone()[0]


##--------------------------------------------------------------------------------------------------------------------##
def timer_1():
    c.execute("UPDATE user_info SET timer=1 where user_id={}".format(vk_id, ))
    conn.commit()


##-----------------------------------------------------------------------------##
def timer_0():
    c.execute("UPDATE user_info SET timer=0 where user_id={}".format(vk_id, ))
    conn.commit()


##--------------------------------------------------------------------------------------------------------------------##
def ownment():
    global messages
    global vk_id
    c.execute("SELECT Farm, Factory, Workers FROM ownment WHERE user_id={}".format(vk_id, ))
    all = c.fetchone()
    farms = all[0]
    factory = all[1]
    workers = all[2]
    own = (farms, factory, workers)
    return own


##--------------------------------------------------------------------------------------------------------------------##
def balance():
    global messages
    global vk_id
    c.execute("SELECT balance FROM user_info WHERE user_id={}".format(vk_id, ))
    res = c.fetchone()[0]
    return round(res, 1)


##--------------------------------------------------------------------------------------------------------------------##

##---------------------------------------------------------------------------------------------------------------------##
def bot():
    c.execute("UPDATE user_info SET timer=1")
    conn.commit()
    while True:
        print("Bot Activated")
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                global messages
                global vk_id
                global vk_name
                global user_info
                ##-------------------------------------------------------------------------------------------------------------------------------------------------##
                messages = vk.messages.getConversations(offset=0, count=200, filter="unanswered")
                vk_id = messages['items'][0]['last_message']['peer_id']
                user_info = vk.users.get(user_ids=vk_id, fields='first_name')
                vk_name = user_info[0]["first_name"]
                c.execute("SELECT * FROM user_info WHERE User_ID = {}".format(vk_id))
                user = c.fetchone()
                ##-------------------------------------------------------------------------------------------------------------------------------------------------##
                if user == None:
                    random_int = random.randint(1, 66)
                    user_info = vk.users.get(user_ids=vk_id, fields='first_name')
                    user_name = user_info[0]["first_name"]
                    c.execute("INSERT INTO user_info (Name, User_ID, Balance, timer) VALUES ('{nam}', {id}, 0, 0)".format(nam=user_name.title() + str(random_int), id=vk_id))
                    c.execute("INSERT INTO ownment (User_ID, Farm, Factory, Workers) VALUES ({id}, 0, 0, 0)".format(id=vk_id))
                    conn.commit()
                    vk.messages.send(peer_id=event.object.peer_id,
                                     message="???? ?????????????????????????????? ?????? ?????????? {}!".format(user_name + str(random_int)),
                                     random_id=0, keyboard=keyboard)
                else:
                    timer_stat = timer_status()
                    def timer():
                        stat = timer_status()
                        print(stat)
                        while stat == 0:
                            c.execute("SELECT balance FROM user_info WHERE user_id={}".format(vk_id))
                            bal = c.fetchone()[0]
                            tick = bal + 0.1 + ((float(ownment()[0]) * 0.1) +
                                                (float(ownment()[1]) * 1) +
                                                (float(ownment()[2]) * 0.2))
                            print(str(round(tick, 1)) + " " + str(vk_id))
                            c.execute("UPDATE user_info SET balance = {balance} WHERE user_id = {id}".format(balance=tick, id=vk_id))
                            conn.commit()
                            time.sleep(1)
                        print('timer3')
                    if timer_stat == 1:
                        c.execute("UPDATE user_info SET timer=0")
                        conn.commit()
                        Thread(target=timer).start()
                    if event.object.text.lower() == "???????????? ????????????!" or event.object.payload == '{"command":"start"}':
                        vk.messages.send(peer_id=event.object.peer_id, message="????????????", random_id=0, keyboard=keyboard)
                    ##-------------------------------------------------------------------------------------------------------------------------------------------------##
                    # elif event.object.text.lower() == "!??????????" or event.object.payload == '{"button":"1"}':
                    #   timer_stat = timer_status()
                    #   c.execute("SELECT * FROM user_info WHERE User_ID = {}".format(vk_id))
                    #   result = c.fetchall()
                    #   if result == []:
                    #       vk.messages.send(peer_id=event.object.peer_id, message="?????? ???????????? ???????????? '!?????????????????????? ??????'!", random_id=0, keyboard=keyboard)
                    #   else:
                    #       if timer_stat == 1:
                    #           timer_0()
                    #           print('Timer Started for {}'.format(str(vk_name)))
                    #           vk.messages.send(peer_id=event.object.peer_id, message="?????????????????? ;)", random_id=0, keyboard=keyboard)
                    #       else:
                    #           vk.messages.send(peer_id=event.object.peer_id, message="?????? ????????????????????!", random_id=0, keyboard=keyboard)
                    ##-------------------------------------------------------------------------------------------------------------------------------------------------##
                    # if "!??????????????????????" in event.object.text.lower():
                    #   what = str(event.object.text.lower().split("!?????????????????????? ")[1])
                    #   c.execute("SELECT * FROM user_info WHERE User_ID = {}".format(vk_id))
                    #   result = c.fetchall()
                    #   if result == []:
                    #       c.execute("SELECT * FROM user_info WHERE Name = '{}'".format(str(what)))
                    #       nick = c.fetchall()
                    #       if nick == []:
                    #           user_info = vk.users.get(user_ids=vk_id, fields='first_name')
                    #           user_name = user_info[0]["first_name"]
                    #           c.execute("INSERT INTO user_info (Name, User_ID, Balance, timer) VALUES ('{nam}', {id}, 0, 0)".format(nam=what.title(), id=vk_id))
                    #           c.execute("INSERT INTO ownment (User_ID, Farm, Factory, Workers) VALUES ({id}, 0, 0, 0)".format(id=vk_id))
                    #           conn.commit()
                    #           vk.messages.send(peer_id=event.object.peer_id, message="???????????? ???? ??????????????????????????????!", random_id=0, keyboard=keyboard)
                    #       else:
                    #           vk.messages.send(peer_id=event.object.peer_id, message="??????, ???? ?????????? ?????? ?????? ??????????", random_id=0, keyboard=keyboard)
                    #   else:
                    #       vk.messages.send(peer_id=event.object.peer_id, message="???? ?????? ??????????????????????????????!", random_id=0, keyboard=keyboard)
                    ##-------------------------------------------------------------------------------------------------------------------------------------------------##
                    # elif event.object.text.lower() == "!????????" or event.object.payload == '{"button":"2"}':
                    #   timer_stat = timer_status()
                    #   c.execute("SELECT * FROM user_info WHERE User_ID = {}".format(vk_id))
                    #   result = c.fetchall()
                    #   if result == []:
                    #       vk.messages.send(peer_id=event.object.peer_id, message="?????? ???????????? ???????????? '!?????????????????????? ??????'!", random_id=0, keyboard=keyboard)
                    #   else:
                    #       if timer_stat == 0:
                    #           timer_1()
                    #           vk.messages.send(peer_id=event.object.peer_id, message="??????????????????", random_id=0, keyboard=keyboard)
                    #       else:
                    #           vk.messages.send(peer_id=event.object.peer_id, message="?????? ?? ???? ???????????????????? >:(", random_id=0, keyboard=keyboard)
                    # ##-------------------------------------------------------------------------------------------------------------------------------------------------##
                    elif event.object.text.lower() == "!????????????" or event.object.payload == '{"button":"4"}':
                        c.execute("SELECT * FROM user_info WHERE User_ID = {}".format(vk_id))
                        result = c.fetchall()
                        if result == []:
                            vk.messages.send(peer_id=event.object.peer_id,
                                             message="?????? ???????????? ???????????? '!?????????????????????? ??????'!", random_id=0,
                                             keyboard=keyboard)
                        else:
                            vk.messages.send(peer_id=event.object.peer_id,
                                             message="???????? ????????????: {bal}".format(bal=balance()), random_id=0,
                                             keyboard=keyboard)
                    ##-------------------------------------------------------------------------------------------------------------------------------------------------##
                    elif "!????????????" in event.object.text.lower():
                        c.execute("SELECT * FROM user_info WHERE User_ID = {}".format(vk_id))
                        result = c.fetchall()
                        if result == []:
                            vk.messages.send(peer_id=event.object.peer_id,
                                             message="?????? ???????????? ???????????? '!?????????????????????? ??????'!", random_id=0,
                                             keyboard=keyboard)
                        else:
                            if event.object.text.lower() == "!????????????" or event.object.text.lower() == "!???????????? ":
                                vk.messages.send(peer_id=event.object.peer_id,
                                                 message="?? ?????? ????????:\n??????????????(????????: 5)\n??????????(????????: 10)\n??????????(????????: 50)\n\n?????????? ????????????, ????????:\n!???????????? ?????????????????????????????? ??????-????",
                                                 random_id=0, keyboard=keyboard)
                            else:
                                what = str(event.object.text.lower().split("!????????????")[1])

                                def num():
                                    try:
                                        int(event.object.text.lower().split("!???????????? ")[2])
                                    except:
                                        num = -1
                                        return num
                                    else:
                                        return int(event.object.text.lower().split("!???????????? ")[2])

                                c.execute("SELECT Balance FROM user_info WHERE user_id={}".format(vk_id))
                                mon = c.fetchone()[0]
                                if what == '??????????':
                                    c.execute("SELECT Farm FROM ownment WHERE user_id={}".format(vk_id))
                                    qty = c.fetchone()[0]
                                    if mon >= 10 * num():
                                        if num() <= 0 or num() == ' ':
                                            vk.messages.send(peer_id=event.object.peer_id,
                                                             message="?????????? ???????????????????? ??????????!", random_id=0,
                                                             keyboard=keyboard)
                                        else:
                                            c.execute(
                                                "UPDATE user_info SET Balance = {balance} WHERE user_id = {id}".format(
                                                    balance=mon - 10 * num(), id=vk_id))
                                            c.execute("UPDATE ownment SET farm = {own} WHERE user_id = {id}".format(
                                                own=int(qty) + num(), id=vk_id))
                                            conn.commit()
                                            vk.messages.send(peer_id=event.object.peer_id,
                                                             message="???? ?????????? ????????: {}".format(num()), random_id=0,
                                                             keyboard=keyboard)
                                    else:
                                        vk.messages.send(peer_id=event.object.peer_id,
                                                         message="?? ?????? ???????????????????????? ??????????????(????????: 10)", random_id=0,
                                                         keyboard=keyboard)
                                elif what == '??????????':
                                    if num() <= 0 or num() == ' ':
                                        vk.messages.send(peer_id=event.object.peer_id,
                                                         message="?????????? ???????????????????? ??????????!", random_id=0,
                                                         keyboard=keyboard)
                                    else:
                                        c.execute("SELECT Factory FROM ownment WHERE user_id={}".format(vk_id))
                                        qty = c.fetchone()[0]
                                        if mon >= 50 * num():
                                            c.execute(
                                                "UPDATE user_info SET Balance = {balance} WHERE user_id = {id}".format(
                                                    balance=mon - 50 * num(), id=vk_id))
                                            c.execute("UPDATE ownment SET factory = {own} WHERE user_id = {id}".format(
                                                own=int(qty) + num(), id=vk_id))
                                            conn.commit()
                                            vk.messages.send(peer_id=event.object.peer_id,
                                                             message="???? ?????????? ??????????????: {}".format(num()), random_id=0,
                                                             keyboard=keyboard)
                                        else:
                                            vk.messages.send(peer_id=event.object.peer_id,
                                                             message="?? ?????? ???????????????????????? ??????????????(????????: 50)",
                                                             random_id=0, keyboard=keyboard)
                                elif what == '??????????????':
                                    if num() <= 0 or num() == ' ':
                                        vk.messages.send(peer_id=event.object.peer_id,
                                                         message="?????????? ???????????????????? ??????????!", random_id=0)
                                    else:
                                        c.execute("SELECT Workers FROM ownment WHERE user_id={}".format(vk_id))
                                        qty = c.fetchone()[0]
                                        if mon >= 5 * num():
                                            c.execute(
                                                "UPDATE user_info SET Balance = {balance} WHERE user_id = {id}".format(
                                                    balance=mon - 5 * num(), id=vk_id))
                                            c.execute("UPDATE ownment SET workers = {own} WHERE user_id = {id}".format(
                                                own=int(qty) + num(), id=vk_id))
                                            conn.commit()
                                            vk.messages.send(peer_id=event.object.peer_id,
                                                             message="???? ?????????? ??????????????: {}".format(num()), random_id=0,
                                                             keyboard=keyboard)
                                        else:
                                            vk.messages.send(peer_id=event.object.peer_id,
                                                             message="?? ?????? ???????????????????????? ??????????????(????????: 5)", random_id=0,
                                                             keyboard=keyboard)
                                else:
                                    vk.messages.send(peer_id=event.object.peer_id,
                                                     message="?????????? ???????????? ???????????? ??????????????, ????????????:\n!????????????",
                                                     random_id=0, keyboard=keyboard)
                    ##-------------------------------------------------------------------------------------------------------------------------------------------------##
                    elif event.object.payload == '{"button":"5"}':
                        c.execute("SELECT * FROM user_info WHERE User_ID = {}".format(vk_id))
                        result = c.fetchall()
                        if result == []:
                            vk.messages.send(peer_id=event.object.peer_id,
                                             message="?????? ???????????? ???????????? '!?????????????????????? ??????'!", random_id=0,
                                             keyboard=keyboard)
                        else:
                            vk.messages.send(peer_id=event.object.peer_id, message="?????? ?????????????", random_id=0,
                                             keyboard=market)  # ????????????: ????????????
                    ##-------------------------------------------------------------------------------------------------------------------------------------------------##
                    elif event.object.payload == '{"button":"6"}':
                        c.execute("SELECT * FROM user_info WHERE User_ID = {}".format(vk_id))
                        result = c.fetchall()
                        if result == []:
                            vk.messages.send(peer_id=event.object.peer_id,
                                             message="?????? ???????????? ???????????? '!?????????????????????? ??????'!", random_id=0,
                                             keyboard=keyboard)
                        else:
                            c.execute("SELECT Balance FROM user_info WHERE user_id={}".format(vk_id))
                            mon = c.fetchone()[0]
                            c.execute("SELECT Farm FROM ownment WHERE user_id={}".format(vk_id))
                            qty = c.fetchone()[0]
                            if mon >= 10:
                                c.execute("UPDATE user_info SET Balance = {balance} WHERE user_id = {id}".format(
                                    balance=mon - 10, id=vk_id))
                                c.execute(
                                    "UPDATE ownment SET farm = {own} WHERE user_id = {id}".format(own=int(qty) + 1,
                                                                                                  id=vk_id))
                                conn.commit()
                                vk.messages.send(peer_id=event.object.peer_id, message="???? ?????????? 1 ??????????", random_id=0,
                                                 keyboard=keyboard)
                            else:
                                vk.messages.send(peer_id=event.object.peer_id,
                                                 message="?? ?????? ???????????????????????? ??????????????(????????: 10)", random_id=0,
                                                 keyboard=keyboard)  # ????????????: ??????????
                    ##-------------------------------------------------------------------------------------------------------------------------------------------------##
                    elif event.object.payload == '{"button":"7"}':
                        c.execute("SELECT * FROM user_info WHERE User_ID = {}".format(vk_id))
                        result = c.fetchall()
                        if result == []:
                            vk.messages.send(peer_id=event.object.peer_id,
                                             message="?????? ???????????? ???????????? '!?????????????????????? ??????'!", random_id=0,
                                             keyboard=keyboard)
                        else:
                            c.execute("SELECT Balance FROM user_info WHERE user_id={}".format(vk_id))
                            mon = c.fetchone()[0]
                            c.execute("SELECT Factory FROM ownment WHERE user_id={}".format(vk_id))
                            qty = c.fetchone()[0]
                            if mon >= 50:
                                c.execute("UPDATE user_info SET Balance = {balance} WHERE user_id = {id}".format(
                                    balance=mon - 50, id=vk_id))
                                c.execute(
                                    "UPDATE ownment SET factory = {own} WHERE user_id = {id}".format(own=int(qty) + 1,
                                                                                                     id=vk_id))
                                conn.commit()
                                vk.messages.send(peer_id=event.object.peer_id, message="???? ?????????? 1 ??????????", random_id=0,
                                                 keyboard=keyboard)
                            else:
                                vk.messages.send(peer_id=event.object.peer_id,
                                                 message="?? ?????? ???????????????????????? ??????????????(????????: 50)", random_id=0,
                                                 keyboard=keyboard)  # ????????????: ??????????
                    ##-------------------------------------------------------------------------------------------------------------------------------------------------##
                    elif event.object.payload == '{"button":"8"}':
                        c.execute("SELECT * FROM user_info WHERE User_ID = {}".format(vk_id))
                        result = c.fetchall()
                        if result == []:
                            vk.messages.send(peer_id=event.object.peer_id,
                                             message="?????? ???????????? ???????????? '!?????????????????????? ??????'!", random_id=0,
                                             keyboard=keyboard)
                        else:
                            c.execute("SELECT Balance FROM user_info WHERE user_id={}".format(vk_id))
                            mon = c.fetchone()[0]
                            c.execute("SELECT Workers FROM ownment WHERE user_id={}".format(vk_id))
                            qty = c.fetchone()[0]
                            if mon >= 5:
                                c.execute("UPDATE user_info SET Balance = {balance} WHERE user_id = {id}".format(
                                    balance=mon - 5, id=vk_id))
                                c.execute(
                                    "UPDATE ownment SET workers = {own} WHERE user_id = {id}".format(own=int(qty) + 1,
                                                                                                     id=vk_id))
                                conn.commit()
                                vk.messages.send(peer_id=event.object.peer_id, message="???? ?????????? 1 ????????????????",
                                                 random_id=0, keyboard=keyboard)
                            else:
                                vk.messages.send(peer_id=event.object.peer_id,
                                                 message="?? ?????? ???????????????????????? ??????????????(????????: 5)", random_id=0,
                                                 keyboard=keyboard)  # ????????????: ??????????????
                    ##-------------------------------------------------------------------------------------------------------------------------------------------------##
                    elif event.object.text.lower() == "!????????" or event.object.payload == '{"button":"3"}':
                        if vk_id == 132617326 or vk_id == 336708052:
                            c.execute("UPDATE user_info SET timer=1")
                            conn.commit()
                            print('??????????')
                            vk.messages.send(peer_id=event.object.peer_id, message="?? ????????????...", random_id=0,
                                             keyboard=hide)
                            exit(0)
                            break
                        else:
                            vk.messages.send(peer_id=event.object.peer_id, message="?????? ?????????????? ???????????????? ???????????? ??????????????????????????????", random_id=0)
                    ##-------------------------------------------------------------------------------------------------------------------------------------------------##
                    else:
                        vk.messages.send(peer_id=event.object.peer_id, message="?????????? ?????????????? ??????", random_id=0,
                                        keyboard=keyboard)


##-----------------------------#
if __name__ == '__main__':
    Thread(target=bot).start()
# ???????????????? ????????????
# text.title() - ?????????????????? ???????????? ?????????? ???????? ???????? ?? ?????????????? ??????????????!