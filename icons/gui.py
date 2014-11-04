#!/usr/bin/env python3
# coding=utf-8

__author__ = 'Herb Brewer'

import os
import sys
import subprocess
import threading
try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog
except ImportError:
    import Tkinter as tk
    import ttk
    import tkFileDialog as filedialog
from collections import deque
from PIL import Image

from icons import make_images


def _show_in_finder_(target_path):
    if sys.platform == 'win32':
        os.startfile(target_path)
    else:
        opener = 'open' if sys.platform == 'darwin' else 'xdg-open'
        subprocess.call([opener, target_path])


def _main_():
    background_color = '#e9e9e9'

    window = tk.Tk()
    window.resizable(0, 0)
    window.title('Drop Icon Below')
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    width = 505
    if sys.platform == 'win32':
        height = 430
    else:
        height = 400
    x = (screenwidth - width)*0.5
    y = (screenheight - height)*0.5
    window.geometry('{}x{}+{}+{}'.format(width, height, int(x), int(y)))
    window.is_picking_file = False

    output_path = tk.StringVar(window, '')

    icon_types = []
    icon_types.append(('icon', 'App Icon'))
    icon_types.append(('launch',
                      'App Lauch Image'))
    icon_types.append(('toolbar',
                      'Toolbar Icon'))
    icon_types.append(('tab', 'Tabbar Icon'))
    icon_types.append(('image', 'Icon'))
    icon_types.append(('notification',
                      'Notification Icon'))
    icon_types.append(('webclip', 'Webclip'))
    icon_type = tk.StringVar(window, 'icon')

    baseline = tk.IntVar(window, 3, 'baseline')

    device_types = []
    device_types.append((tk.BooleanVar(window, True), 'ios', 'iOS'))
    device_types.append((tk.BooleanVar(window, True), 'android', 'Android'))

    frame = tk.Frame(window, bg=background_color, height=400, padx=20, pady=20)
    frame.pack(fill='both', expand=True)

    drop_button = tk.Canvas(frame, bg=background_color, width=320, height=320,
                            borderwidth=0, highlightthickness=0)
    drop_button.create_rectangle(5, 5, 315, 315, width=10,
                                 dash=(30), activefill=background_color,
                                 outline="#717171", activeoutline='#0c0')
    drop_button.grid(row=0, column=0, rowspan=3)

    types_frame = tk.LabelFrame(frame, bg=background_color,
                                text='Icon Types')
    for tmp in icon_types:
        tk.Radiobutton(types_frame, bg=background_color, variable=icon_type,
                       value=tmp[0], text=tmp[1]).pack(anchor='w')
    types_frame.grid(row=0, column=1, sticky='nwne', padx=10)

    devices_frame = tk.LabelFrame(frame, bg=background_color,
                                  text='Devices')
    for device_type in device_types:
        tk.Checkbutton(devices_frame, bg=background_color,
                       variable=device_type[0],
                       text=device_type[2]).pack(anchor='w')
    devices_frame.grid(row=1, column=1, sticky='nwne', padx=10)

    baselines_frame = tk.LabelFrame(frame, bg=background_color,
                                    text='Baseline')
    tk.Radiobutton(baselines_frame, bg=background_color,
                   variable=baseline, value=3,
                   text='3').pack(anchor='w')
    tk.Radiobutton(baselines_frame, bg=background_color,
                   variable=baseline, value=4,
                   text='4').pack(anchor='w')
    baselines_frame.grid(row=2, column=1, sticky='nwne', padx=10)

    def on_select_output():
        if window.is_picking_file:
            return
        window.is_picking_file = True
        path = filedialog.askdirectory(title='Select output directory')
        output_path.set(path)
        if path:
            output_select_button['text'] = 'Output: {}'.format(path)
        else:
            output_select_button['text'] = 'Output: next to original icon'
        window.is_picking_file = False

    ttk.Style().configure('TButton', background=background_color)
    output_select_button = ttk.Button(frame,
                                      text="Output: next to original icon",
                                      command=on_select_output)
    output_select_button.grid(row=3, column=0, columnspan=2, sticky='we')

    class Task(threading.Thread):
        def __init__(self, *args, **kwargs):
            self.callback = kwargs['callback']
            del kwargs['callback']
            super(Task, self).__init__(*args, **kwargs)

        def run(self):
            super(Task, self).run()
            self.callback(self)

    class Progressbar(ttk.Progressbar):
        def __init__(self, *args, **kwargs):
            ttk.Progressbar.__init__(self, *args, **kwargs)
            self.tasks = deque()
            self.pending_task = None
            self.callback = None
            self.hide()

        def show(self):
            self.grid(row=4, column=0, columnspan=2,
                      sticky='we')

        def hide(self):
            self.grid_forget()

        def add_task(self, target, args):
            task = Task(target=target, args=args,
                        callback=self._on_finished_)
            self.tasks.append(task)

        def start(self, callback=None):
            self.callback = callback
            self._check_()
            self.pending_task = self.tasks.pop()
            self.pending_task.start()
            self.show()
            ttk.Progressbar.start(self)

        @property
        def is_running(self):
            return self.tasks or self.pending_task

        def _on_finished_(self, task):
            if self.tasks:
                self.pending_task = self.tasks.pop()
                self.pending_task.start()
            else:
                self.pending_task = None

        def _check_(self):
            if self.is_running:
                self.after(1000, self._check_)
                return
            self.hide()
            self.stop()
            if self.callback:
                self.callback()

    progressbar = Progressbar(frame, orient='horizontal', mode='indeterminate')

    def on_select_icon(event):
        if progressbar.is_running:
            return
        if window.is_picking_file:
            return
        window.is_picking_file = True
        icon_path = filedialog.\
            askopenfilename(title='Select your icon',
                            filetypes=[('Images', '.png .jpg .jpeg .bmp')])
        if icon_path:
            try:
                image = Image.open(icon_path)
            except Exception:
                return

            image_name, _ = os.path.splitext(os.path.basename(icon_path))
            if output_path.get():
                to_output_path = output_path.get()
            else:
                to_output_path = os.path.dirname(icon_path)
            to_icon_type = icon_type.get()
            to_devices = []
            for device_type in device_types:
                if device_type[0].get():
                    to_devices.append(device_type[1])

            to_baseline = baseline.get()
            progressbar.add_task(target=make_images,
                                 args=(image, image_name,
                                       os.path.join(to_output_path,
                                                    to_icon_type),
                                       to_icon_type,
                                       to_devices, to_baseline))

            def callback():
                _show_in_finder_(to_output_path)
            progressbar.start(callback)
        window.is_picking_file = False
    drop_button.bind('<ButtonRelease-1>', on_select_icon)

    window.lift()
    window.mainloop()

if __name__ == '__main__':
    _main_()
