## ================================================
##              监听键盘
## ================================================
from pynput.keyboard import Key, Listener, Controller
from pynput.mouse import Listener as MouseListener
from pynput import mouse
from pynput import keyboard
from threading import Thread, Lock


runing = True

class KeyMouCounter():

    def __init__(self):
        self.keyboard = Controller()  #实例化键盘对象
        self.locker = Lock()
        runing = True

    def on_press(self, key):  # 按键被按压调用这个函数
        # 输出按压的按键名字
        print('{0} pressed'.format(key))

    def on_release(self, key):  # 按键被松开调用这个函数
        # 输出松开的按键名字
        global runing
        print('{0} release'.format(key))
        if isinstance(key, keyboard.KeyCode):
            print(key.char)
        else:
            print(key)
        if key == Key.esc:  # 如果按了Esc键就停止监听
            self.locker.acquire()
            runing = False
            self.locker.release()
            #print("Runging Stat" , runing)
            print("Stop Keyboard listener")
            return False  # Stop listener

    def on_move(self, x, y):  # 监听鼠标移动
        #print('Pointer moved to {0}'.format((x, y)))
        pass

    def on_click(self, x, y, button, pressed):  # 监听鼠标点击
        print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
        try:
            print(type(button))
            print(button.name)
        except:
            pass
        global runing
        #print("Runging Stat" , runing)
        if not runing:  # 如果没有按压就结束程序（即，单击一下鼠标会结束程序）
            # Stop listener
            print("Stop Mouse listener")
            return False

    def on_scroll(self, x, y, dx, dy):  # 监听鼠标滚轮
        #print('Scrolled {0}'.format((x, y)))
        pass

    def mouse_listener(self):
        print('Listener Mouse ...')
        with mouse.Events() as event:
            for i in event:
                #迭代用法。
                if isinstance(i, mouse.Events.Click):
                    #鼠标点击事件。
                    print(i.x, i.y, i.button, i.pressed)

    def keyboard_listener(self):
        print('Listener Keyboard ...')
        with self.keyboard.Events() as event:
            for i in event:
                #迭代用法。
                if isinstance(i, mouse.Events.Click):
                    #鼠标点击事件。
                    print(i.x, i.y, i.button, i.pressed)

    def lister_keyboard(self):
        print('Listener Keyboard ...')
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def lister_mouse(self):
        print('Listener Mouse ...')
        with MouseListener(on_click=self.on_click) as listener:
            listener.join()

    def run(self):
        t_keyboard = Thread(target=self.lister_keyboard)
        t_mouse = Thread(target=self.lister_mouse)

        t_mouse.start()
        t_keyboard.start()

        t_keyboard.join()
        t_mouse.join()


if __name__ == "__main__":
    kmc = KeyMouCounter()
    kmc.run()