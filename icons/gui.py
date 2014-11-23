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

from icons import make_images, supported_devices, device_name


def _load_tkdnd(master):
    if sys.platform == 'win32':
        basis = sys.executable
    else:
        basis = __file__
    tkdndlib = tkdndlib = os.environ.get('TKDND_LIBRARY', None)
    if not tkdndlib or not os.path.exists(tkdndlib):
        tkdndlib = os.path.join(os.path.dirname(basis), 'tkdnd', sys.platform)
    master.tk.eval('global auto_path; lappend auto_path {%s}' % tkdndlib)
    master.tk.eval('package require tkdnd')
    master._tkdnd_loaded = True


class TkDND(object):
    def __init__(self, master):
        if not getattr(master, '_tkdnd_loaded', False):
            _load_tkdnd(master)
        self.master = master
        self.tk = master.tk

    def bindtarget(self, window, callback, dndtype, event='<Drop>',
                   priority=50):
        cmd = self._prepare_tkdnd_func(callback)
        return self.tk.call('dnd', 'bindtarget', window, dndtype, event,
                            cmd, priority)

    def bindtarget_query(self, window, dndtype=None, event='<Drop>'):
        return self.tk.call('dnd', 'bindtarget', window, dndtype, event)

    def cleartarget(self, window):
        self.tk.call('dnd', 'cleartarget', window)

    def bindsource(self, window, callback, dndtype, priority=50):
        cmd = self._prepare_tkdnd_func(callback)
        self.tk.call('dnd', 'bindsource', window, dndtype, cmd, priority)

    def bindsource_query(self, window, dndtype=None):
        return self.tk.call('dnd', 'bindsource', window, dndtype)

    def clearsource(self, window):
        self.tk.call('dnd', 'clearsource', window)

    def drag(self, window, actions=None, descriptions=None,
             cursorwin=None, callback=None):
        cmd = None
        if cursorwin is not None:
            if callback is not None:
                cmd = self._prepare_tkdnd_func(callback)
        self.tk.call('dnd', 'drag', window, actions, descriptions,
                     cursorwin, cmd)

    _subst_format = ('%A', '%a', '%b', '%D', '%d', '%m', '%T',
                     '%W', '%X', '%Y', '%x', '%y')
    _subst_format_str = " ".join(_subst_format)

    def _prepare_tkdnd_func(self, callback):
        funcid = self.master.register(callback, self._dndsubstitute)
        cmd = ('%s %s' % (funcid, self._subst_format_str))
        return cmd

    def _dndsubstitute(self, *args):
        if len(args) != len(self._subst_format):
            return args

        def try_int(x):
            x = str(x)
            try:
                return int(x)
            except ValueError:
                return x

        A, a, b, D, d, m, T, W, X, Y, x, y = args

        event = tk.Event()
        event.action = A
        event.action_list = a
        event.mouse_button = b
        event.data = D
        event.descr = d
        event.modifier = m
        event.dndtype = T
        event.widget = self.master.nametowidget(W)
        event.x_root = X
        event.y_root = Y
        event.x = x
        event.y = y

        event.action_list = str(event.action_list).split()
        for name in ('mouse_button', 'x', 'y', 'x_root', 'y_root'):
            setattr(event, name, try_int(getattr(event, name)))

        return (event, )


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
    window.attributes('-topmost', 1)
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    width = 515
    height = 475
    if sys.platform == 'win32':
        height = height + 30

    x = (screenwidth - width)*0.5
    y = (screenheight - height)*0.5
    window.geometry('{}x{}+{}+{}'.format(width, height, int(x), int(y)))
    window.is_picking_file = False

    output_path = tk.StringVar(window, '')

    icon_types = []
    icon_types.append(('icon', 'App Icon'))
    icon_types.append(('launch',
                      'App Lauch Image'))
    icon_types.append(('image', 'Icon'))
    icon_types.append(('favicon', 'Favicon'))
    icon_types.append(('toolbar',
                      'Toolbar Icon'))
    icon_types.append(('tab', 'Tabbar Icon'))
    icon_types.append(('notification',
                      'Notification Icon'))
    icon_type = tk.StringVar(window, 'icon')

    device_types = []

    baseline = tk.IntVar(window, 3, 'baseline')

    frame = tk.Frame(window, bg=background_color, padx=20, pady=20)
    frame.pack(fill='both', expand=True)

    drop_button = tk.Canvas(frame, bg=background_color, width=320, height=320,
                            borderwidth=0, highlightthickness=0)
    drop_button.create_rectangle(5, 5, 315, 315, width=10,
                                 dash=(30), activefill=background_color,
                                 outline="#717171", activeoutline='#0c0')
    drop_button.grid(row=0, column=0, rowspan=3, pady=40)

    types_frame = tk.LabelFrame(frame, bg=background_color,
                                text='Icon Types')
    for tmp in icon_types:
        tk.Radiobutton(types_frame, bg=background_color, variable=icon_type,
                       value=tmp[0], text=tmp[1]).pack(anchor='w')
    types_frame.grid(row=0, column=1, sticky='nwne', padx=10)

    baselines_frame = tk.LabelFrame(frame, bg=background_color,
                                    text='Baseline')
    tk.Radiobutton(baselines_frame, bg=background_color,
                   variable=baseline, value=3,
                   text='3').pack(anchor='w')
    tk.Radiobutton(baselines_frame, bg=background_color,
                   variable=baseline, value=4,
                   text='4').pack(anchor='w')

    toggle_icon_types = tk.BooleanVar(window, True)

    def on_toggle_icon_types(*args):
        state = toggle_icon_types.get()
        for device_type in device_types:
            device_type[0].set(state)
    toggle_icon_types.trace('w', on_toggle_icon_types)

    def on_icon_type_changed(*args):
        raw_icon_type = icon_type.get()
        devices = supported_devices(raw_icon_type)
        selected_devices = set()
        for (device_var, device, _) in device_types:
            if device_var.get():
                selected_devices.add(device)
        del device_types[:]
        toggle_icon_types.set(False)
        for device in devices:
            device_types.append((tk.BooleanVar(window,
                                               device in selected_devices),
                                device,
                                device_name(device)))
        devices_frame = tk.LabelFrame(frame, bg=background_color,
                                      text='Devices')
        for device_type in device_types:
            tk.Checkbutton(devices_frame, bg=background_color,
                           variable=device_type[0],
                           text=device_type[2]).pack(anchor='w')
        if len(device_types) > 1:
            tk.Checkbutton(devices_frame, bg=background_color,
                           variable=toggle_icon_types,
                           text='All').pack(anchor='w')
        for old_frame in frame.grid_slaves(row=1, column=1):
            old_frame.grid_remove()
        devices_frame.grid(row=1, column=1, sticky='nwne', padx=10)
        if raw_icon_type == 'image':
            baselines_frame.grid(row=2, column=1, sticky='nwne', padx=10)
        else:
            baselines_frame.grid_forget()
    icon_type.trace('w', on_icon_type_changed)
    on_icon_type_changed()

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
    output_select_button.grid(row=3, column=0, columnspan=2, sticky='we',
                              pady=5)

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
        if hasattr(event, 'data'):
            icon_path = event.data.split()[0]
            _, ext = os.path.splitext(icon_path)
            if ext.lower() not in ['.png', '.jpg', '.jpeg', '.bmp']:
                return
        else:
            icon_path = filedialog.\
                askopenfilename(title='Select your icon',
                                filetypes=[('Images', '.png .jpg .jpeg .bmp')])
        if icon_path:
            to_devices = []
            for device_type in device_types:
                if device_type[0].get():
                    to_devices.append(device_type[1])
            if to_devices:
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
                to_baseline = baseline.get()
                progressbar.add_task(target=make_images,
                                     args=(image, image_name,
                                           to_output_path,
                                           to_icon_type,
                                           to_devices, to_baseline))

                def callback():
                    _show_in_finder_(to_output_path)
                progressbar.start(callback)
        window.is_picking_file = False
    drop_button.bind('<ButtonRelease-1>', on_select_icon)
    dnd = TkDND(window)
    dnd.bindtarget(drop_button, on_select_icon, 'text/uri-list')

    window.lift()
    window.mainloop()

if __name__ == '__main__':
    _main_()
