from enum import Enum
from PySide6.QtCore import QThread, Signal
from pynput import mouse
from pynput import keyboard

class KeyboardThread(QThread):

    signal = Signal(str)

    def __init__(self, *args, **kwargs):
        super(KeyboardThread, self).__init__()
        self.window = kwargs.get('window')
        self.debug = kwargs.get('debug')
        self.signal.connect(self.add_counter)
    
    def run(self):
        print('Listener Keyboard ...')
        with keyboard.Listener(on_release=self.on_release) as self.listener:
            self.listener.join()

    def stop(self):
        self.listener.stop()  
    
    def on_release(self, key):  # 按键被松开调用这个函数
        # 输出松开的按键名字
        if self.debug:
            print('{0} release'.format(key))
            #print(type(key))
        
        if isinstance(key, keyboard.KeyCode):
            if self.debug:
                print(type(key.char))
                print(key.vk)
            if not isinstance(key.char, Enum):
                self.signal.emit(str(key.vk))
        #else:
            #self.signal.emit(key.name)
        '''
        if key == keyboard.Key.esc:  # 如果按了Esc键就停止监听
            self.locker.acquire()
            self.window.is_counter = False
            self.locker.release()
            #print("Runging Stat" , runing)
            print("Stop Keyboard listener")
            return False  # Stop listener
        '''
    
    def add_counter(self, key):
        self.window.cur_db.add_events(name=key, is_key=True)
        self.window.day_keyboard_count += 1
        self.window.month_keyboard_count += 1
        self.window.year_keyboard_count += 1
        self.window.ui.lineEdit.setText(str(self.window.day_keyboard_count))
        self.window.ui.lineEdit_2.setText(str(self.window.month_keyboard_count))
        self.window.ui.lineEdit_3.setText(str(self.window.year_keyboard_count))

class MouseThread(QThread):

    signal = Signal(str)

    def __init__(self, *args, **kwargs):
        super(MouseThread, self).__init__()
        self.window = kwargs.get('window')
        self.debug = kwargs.get('debug')
        self.signal.connect(self.add_counter)
    
    def run(self):
        print('Listener Mouse ...')
        with mouse.Listener(on_click=self.on_click) as self.listener:
            self.listener.join()

    def stop(self):
        self.listener.stop()
        
    def on_click(self, x, y, button, pressed):  # 监听鼠标点击
        if self.debug:
            #print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
            print("Mouse is Clicked at (",x,",",y,")","with",button)
        
        if pressed:
            mouse_click = { 'left': '-1', 'right': '-2', 'middle': '-3', 'x1':'-4', 'x2':'-5'}
            self.signal.emit(mouse_click[button.name])
        '''
        #print("Runging Stat" , runing)
        if not self.window.is_counter:  # 如果没有按压就结束程序（即，单击一下鼠标会结束程序）
            # Stop listener
            print("Stop Mouse listener")
            return False
        '''

    def add_counter(self, key):
        self.window.cur_db.add_events(name=key, is_key=False)
        self.window.day_mouse_count += 1
        self.window.month_mouse_count += 1
        self.window.year_mouse_count += 1
        self.window.ui.lineEdit_4.setText(str(self.window.day_mouse_count))
        self.window.ui.lineEdit_5.setText(str(self.window.month_mouse_count))
        self.window.ui.lineEdit_6.setText(str(self.window.year_mouse_count))