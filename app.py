import subprocess

import pytesseract
import rumps
from PIL import Image
from pynput import keyboard

APP_TITLE = 'i2t'
APP_ICON = 'icon.png'


class App(rumps.App):
    def __init__(self):
        super().__init__(APP_TITLE, icon=APP_ICON, quit_button='Exit')

    @rumps.clicked("Screenshot")
    def screenshot(self, _):
        screenshot()
        # on_click = OnClickListener()
        # with mouse.Listener(on_click=on_click_screenshot) as listener:
        #     listener.join()
        # image = ImageGrab.grab(bbox=(*on_click.start, *on_click.end))
        # image.save('demo.jpg')

        # image.show()

    # @rumps.clicked("Listen?")
    # def onoff(self, sender):
    #     sender.state = not sender.state
    #     onListener = OnPressListener()
    #     with keyboard.Listener(on_press=onListener,
    #                            on_release=onListener.on_release()) as listener:
    #         if sender.state:
    #             listener.start()
    #         else:
    #             listener.stop()


def screenshot():
    subprocess.run(['screencapture', '-i', 'demo.jpg'])
    print('image grabbed')
    text = pytesseract.image_to_string(Image.open('demo.jpg'), lang="chi_sim")
    text = text.replace(' ', '').replace(',', '，')
    print('text:', text)
    write_to_clipboard(text)


class OnPressListener:
    def __init__(self):
        self.command = False
        self.option = False

    def __call__(self, key):
        if key.char == 'z' and self.command and self.option:
            self.command = False
            self.option = False
            screenshot()

    def on_release(self):
        def release(key):
            if key == keyboard.Key.cmd:
                self.command = False
            elif key == keyboard.Key.ctrl:
                self.option = False

        return release


# def on_press(key):
#     if key.char == 'z' and :
#     print('{0} released'.format(
#         key))
#     if key == keyboard.Key.esc:
#         # Stop listener
#         return False


def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))


# class OnClickListener:
#     def __init__(self):
#         self.start = None
#         self.end = None
#
#     def __call__(self, x, y, button, pressed):
#         if pressed:
#             self.start = Point(x, y)
#         else:
#             self.end = Point(x, y)
#             print(self.start, self.end)
#             return False


if __name__ == '__main__':
    App().run()
    # print(pytesseract.image_to_string(Image.open('demo.png')))
