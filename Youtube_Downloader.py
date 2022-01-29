from tkinter import Button, Label, Entry, messagebox, Tk, StringVar, Canvas, NW, END, Menu
from tkinter.ttk import Combobox, Progressbar, Style
from tkinter import filedialog
import HTTP_REQUESTS
import threading
from PIL import Image, ImageTk
import get_theme_info
from HTTP_REQUESTS import requests
from sys import exit


def get_theme():
    global theme
    theme = get_theme_info.get_last_theme_details()
    set_theme(theme)

def openLocation():
    global FOLDER_NAME
    FOLDER_NAME = filedialog.askdirectory()
    path_entry.delete(0, END)
    path_entry.insert(0, FOLDER_NAME)


def check(*event):
    set_lable_text("Please wait until response...")
    url = link_text.get()
    global valid
    valid = HTTP_REQUESTS.check_url(url)
    if type(valid) == dict:
        threading.Thread(target=get_info).start()
    else:
        messagebox.showerror("ERROR", "Please insert true URL or run as admin or check your connection or use a VPN")
        set_lable_text("Connection Failed!\nPlease check your connection or use a VPN or run as admin")


def download():
    link_entry['state'] = 'disabled'
    path_entry['state'] = 'disabled'
    quality_combo['state'] = 'disabled'
    url = link_text.get()
    valid = HTTP_REQUESTS.check_url(url)
    if type(valid) == dict:
        download_video()
    else:
        messagebox.showerror("ERROR", "Please insert true URL or use a VPN or run as admin")
        set_lable_text("Connection Failed!\nPlease check your connection or use a VPN or run as admin")


def download_video():
    try:
        url = link_text.get()
        valid = HTTP_REQUESTS.check_url(url)
        res = quality_text.get()
        lo = path_text.get()
        if res == "":
            res = HTTP_REQUESTS.get_qualitys(valid)[0]
        k = str(res).split("k: ")[-1]
        vid_url = HTTP_REQUESTS.get_vid(valid)
        dlink = HTTP_REQUESTS.get_dlink(k, vid_url)
        proxies = HTTP_REQUESTS.proxies
        response = requests.get(dlink, stream=True, proxies=proxies, verify=False)
        file_size = int(response.headers['Content-Length'])
        block_size = 1024
        progress.configure(maximum=file_size)
        vid_title = HTTP_REQUESTS.get_title(valid)
        vid_title = get_title(vid_title)
        progress["value"] = 0
        vid_format = HTTP_REQUESTS.get_format()
        vid_path = vid_title + "." + vid_format
        if lo == "":
            folder_name = filedialog.askdirectory()
            lo = folder_name
            vid_path = lo + "/" + vid_title + "." + vid_format
        with open(vid_path, "wb") as file:
            for data in response.iter_content(block_size):
                progress["value"] += len(data)
                file.write(data)
            if len(data) == 0:
                raise Exception("Download link is not valid")
        messagebox.showinfo("Success", "File saved in: " + vid_path)
    except Exception as e:
        messagebox.showerror("ERROR", "Could not download or save file")
        set_lable_text("Connection Failed!\nPlease check your connection, check your entered path or use a VPN")


def get_title(title):
    if len(title) > 15:
        title = title[:16]
    return title


def set_lable_text(text):
    i = 30
    while i < len(text):
        text = text[:i] + "\n" + text[i:]
        i += 30
    vid_lbl["text"] = text


def creat_label(text):
    lbl = Label(root, text=text)
    return lbl


def create_Entry(textvariable):
    entry = Entry(root, width=50, textvariable=textvariable)
    return entry


def create_Button(text, x):
    button = Button(root, width=8, height=1, text=text, command=x)
    return button


def get_info():
    global image
    vid_url = HTTP_REQUESTS.get_vid(valid)
    vid_title = HTTP_REQUESTS.get_title(valid)
    qualitys = HTTP_REQUESTS.get_qualitys(valid)
    img = HTTP_REQUESTS.get_jpg(vid_url)
    if type(img) == Image.Image:
        set_lable_text(vid_title)
        image = ImageTk.PhotoImage(img)
        canvas.grid(row=4, column=0, columnspan=3, rowspan=2, padx=5, pady=20)
        canvas.create_image(0, 0, anchor=NW, image=image)
        quality_combo['values'] = qualitys
    else:
        set_lable_text("Connection Failed!\nPlease check your connection or use a VPN")
        messagebox.showerror("ERROR", "Please use a VPN")


def paste():
    link_entry.insert(0, root.clipboard_get())


def set_theme(value):
    if value == 'Dark':
        set_dark()
    if value == 'Colored':
        set_colored()
    if value == 'Default':
        set_default()
    if value == 'Light':
        set_light()


def set_dark():
    global theme
    detail = get_theme_info.dark_theme_details()
    img_lbl.config(image='', background=detail[0])
    lbl_color_config(detail[0], detail[1])
    button_color_config(detail[2], detail[3])
    entry_color_config(detail[4], detail[5])
    vid_lbl.configure(background=detail[6], foreground=detail[1])
    theme = 'Dark'


def set_light():
    global theme
    detail = get_theme_info.light_theme_details()
    img_lbl.config(image='', background=detail[0])
    lbl_color_config(detail[0], detail[1])
    button_color_config(detail[2], detail[3])
    entry_color_config(detail[4], detail[5])
    vid_lbl.configure(background=detail[6], foreground=detail[1])
    theme = 'Light'


def set_default():
    global theme
    detail = get_theme_info.default_theme_details()
    img_lbl.config(image=img)
    lbl_color_config(detail[0], detail[1])
    button_color_config(detail[2], detail[3])
    entry_color_config(detail[4], detail[5])
    vid_lbl.configure(background=detail[6], foreground=detail[1])
    theme = 'Default'


def set_colored():
    global theme
    detail = get_theme_info.colored_theme_details()
    img_lbl.config(image='', background=detail[0])
    lbl_color_config(detail[0], detail[1])
    button_color_config(detail[2], detail[3])
    entry_color_config(detail[4], detail[5])
    vid_lbl.configure(background=detail[6], foreground=detail[1])
    theme = 'Colored'

def add_menubars():
    for menu in menubars:
        filemenu.add_command(label=menu, command=lambda x=menu: set_theme(x))


def lbl_color_config(background, foreground):
    link_lbl.configure(background=background, foreground=foreground)
    path_lbl.configure(background=background, foreground=foreground)
    quality_lbl.configure(background=background, foreground=foreground)
    percentage_lbl.configure(background=background, foreground=foreground)
    author_lbl.configure(background=background, foreground=foreground)


def entry_color_config(background, foreground):
    link_entry.configure(background=background, foreground=foreground)
    path_entry.configure(background=background, foreground=foreground)


def button_color_config(background, foreground):
    paste_btn.configure(background=background, foreground=foreground)
    browse.configure(background=background, foreground=foreground)
    download.configure(background=background, foreground=foreground)


def on_close():
    global theme
    get_theme_info.set_last_theme(theme)
    exit()

theme = ''
menubars = ['Dark', 'Light', 'Colored', 'Default']
root = Tk()
root.geometry('528x509')
root.resizable(width=False, height=False)
style = Style(root)
style.theme_use('vista')
root.configure()
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Appearance", menu=filemenu)
add_menubars()
img_open = Image.open('15f9007cc00d7f54dec4ba5ab8dd5816.jpg').resize((528, 509))
img = ImageTk.PhotoImage(img_open)
img_lbl = Label(root, width=528, height=509)
img_lbl.place(anchor=NW)
quality_text = StringVar()
link_text = StringVar()
path_text = StringVar()
link_lbl = creat_label('Link:')
path_lbl = creat_label('Path:')
quality_lbl = creat_label('Quality:')
author_lbl = creat_label('Created by Mani Jabari')
percentage_lbl = creat_label("Percentage:")
vid_lbl = Label(root, width=30, height=4)
link_entry = create_Entry(link_text)
path_entry = create_Entry(path_text)
quality_combo = Combobox(root, width=45, textvariable=quality_text)
download_th = threading.Thread(target=download)
download = create_Button("Download", download_th.start)
browse = create_Button("Browse", openLocation)
paste_th = threading.Thread(target=paste)
paste_btn = create_Button("Paste", paste_th.start)
progress = Progressbar(root, length=300)
root.title("Youtube Downloader")
canvas = Canvas(root, width=150, height=150)
link_lbl.grid(row=0, column=0, padx=5, pady=10)
link_entry.grid(row=0, column=1, columnspan=3, padx=5, pady=10)
paste_btn.grid(row=0, column=4, padx=5, pady=10)
path_lbl.grid(row=1, column=0, padx=5, pady=40)
path_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=40)
browse.grid(row=1, column=4, padx=5, pady=40)
quality_lbl.grid(row=2, column=0, padx=5, pady=20)
quality_combo.grid(row=2, column=1, columnspan=3, padx=5, pady=20)
download.grid(row=2, column=4, padx=5, pady=20)
percentage_lbl.grid(row=3, column=0, padx=5, pady=40)
progress.grid(row=3, column=2, columnspan=2, padx=5, pady=40)
author_lbl.grid(row=3, column=4, padx=5, pady=40)
vid_lbl.grid(row=4, column=3, columnspan=4, rowspan=2)
root.iconbitmap('icon.ico')
link_text.trace('w', check)
root.config(menu=menubar)
root.protocol("WM_DELETE_WINDOW", on_close)
get_theme()
root.mainloop()
