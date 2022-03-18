import tkinter as tk
import tkinter.messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

WINDOW_SIZE = "508x530"
WATER_MARK_PHOTO_PATH = "water_mark.png"
PREVIEW_PHOTO_PATH = "preview.png"

x = 0
y = 0

photo_path = ""


def open_file():
    global photo_path
    global user_image_preview
    global water_mark_photo_tk
    global user_image
    photo_path = askopenfilename()
    user_image = preview_image = Image.open(photo_path)

    # resize photo to fit into window
    if (user_image.height > 500) or (user_image.width > 500):
        if user_image.height > user_image.width:
            preview_image = user_image.resize((int(500*user_image.width/user_image.height), 500), Image.ANTIALIAS)
        elif user_image.height < user_image.width:
            preview_image = user_image.resize((500, int(500*user_image.height/user_image.width)), Image.ANTIALIAS)
        elif (user_image.height == user_image.width) and (user_image.height > 500):
            preview_image = user_image.resize((500, 500), Image.ANTIALIAS)

    user_image_preview = ImageTk.PhotoImage(preview_image)
    canvas.config(width=preview_image.width, height=preview_image.height)
    canvas.itemconfig(image, image=user_image_preview)
    canvas.coords(image2, int(user_image_preview.width() / 2), int(user_image_preview.height() / 2))
    canvas.itemconfig(image2, image=water_mark_photo_tk)
    window.geometry(f"508x{user_image_preview.height() + 30}")


def place_watermark(event):
    global x
    global y
    x, y = event.x, event.y

    if (x > user_image_preview.width() - water_mark_photo_tk.width() / 2) \
            or (y > user_image_preview.height() - water_mark_photo_tk.height() / 2) \
            or (x < water_mark_photo_tk.width()/2) \
            or (y < water_mark_photo_tk.height()/2):
        print("Cannot place watermark here")
    else:
        canvas.coords(image2, event.x, event.y)


def save_photo():
    try:
        scale = user_image.width / (canvas.winfo_width() - 4)
        new_x_resize = int(scale * 200)
        new_y_resize = int(scale * 100)

        new_x_past_watermark = int(scale * (x - water_mark_photo_tk.width()/2))
        new_y_past_watermark = int(scale * (y - water_mark_photo_tk.height()/2))

        mark_photo = water_mark_photo.resize((new_x_resize, new_y_resize), Image.ANTIALIAS)
        user_image.paste(mark_photo, (new_x_past_watermark, new_y_past_watermark), mask=mark_photo)
        user_image.save(f"{photo_path.split('/')[-1]}")
    except ValueError:
        tkinter.messagebox.showinfo(message="Please select photo")
        clear_program()


def clear_program():
    user_image.close()
    canvas.config(width=500, height=500)
    canvas.itemconfig(image, image=preview_image_screen)
    canvas.itemconfig(image2, image=preview_image_screen)
    canvas.coords(image2, 250, 250)
    window.geometry(WINDOW_SIZE)


window = tk.Tk()

window.geometry(WINDOW_SIZE)
window.resizable(height=False, width=False)
window.title("WaterMarkApp")

user_image = Image.open(PREVIEW_PHOTO_PATH)
user_image_preview = ImageTk.PhotoImage(Image.open(PREVIEW_PHOTO_PATH))
preview_image_screen = ImageTk.PhotoImage(Image.open(PREVIEW_PHOTO_PATH))

water_mark_photo = Image.open(WATER_MARK_PHOTO_PATH)
water_mark_photo = water_mark_photo.resize((200, 100), Image.ANTIALIAS)
water_mark_photo_tk = ImageTk.PhotoImage(water_mark_photo)

search_file = tk.Button(text="Select photo", width=23, height=1, command=open_file)
search_file.grid(row=0, column=0)

save_photo_button = tk.Button(text="Save", width=23, height=1, command=save_photo)
save_photo_button.grid(row=0, column=1)

exit_button = tk.Button(text="Exit", width=23, height=1, command=window.destroy)
exit_button.grid(row=0, column=2)

canvas = tk.Canvas(width=500, height=500)
canvas.bind("<Button-1>", place_watermark)

image = canvas.create_image(0, 0, anchor="nw", image=preview_image_screen)
image2 = canvas.create_image(250, 250, anchor="center", image=preview_image_screen)

canvas.grid(row=1, column=0, columnspan=3)

window.mainloop()
