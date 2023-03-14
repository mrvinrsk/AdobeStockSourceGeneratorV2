import datetime
import tkinter as tk
from tkinter import filedialog

from scrape_link import adobestock, fallback, flaticon


def create_popup(file):
    """
    Creates the progress popup window
    """
    popup = tk.Toplevel(root)
    popup.geometry("600x400")
    popup.title("Progress: " + str(file))
    text = tk.Text(popup, height=400, width=600)
    text.pack()
    return text


def update_text(new_text, text):
    """
    Updates the text of the progress popup
    """
    text.insert(tk.END, new_text + "\n")
    text.see(tk.END)
    text.update()


def open_folder(path):
    """
    Opens the parent folder of a file/directory in the default file manager
    """
    import os
    import platform
    import subprocess

    if platform.system() == "Windows":
        os.startfile(os.path.abspath(os.path.join(path, os.pardir)))
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", "-R", path])
    else:
        subprocess.Popen(["xdg-open", os.path.abspath(os.path.join(path, os.pardir))])


def run_program():
    """
    Runs the main program and updates the progress popup
    """

    file_path = input_file.get().strip()
    if not file_path:
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        input_file.delete(0, tk.END)
        input_file.insert(0, file_path)

    text = create_popup(file_path)

    now = datetime.datetime.now()
    date_string = now.strftime("%d.%m.%Y %H:%M")

    with open(file_path[:file_path.rfind(".")] + ".html", "a") as output:
        output.write("<div class='sources' data-last-updated='" + str(date_string) + '\'>\n')
        output.write("\t<!-- StockSourceGenerator by Marvin Roßkothen -->\n")

    with open(file_path, "r") as f:
        for line in f:
            url = line.strip().split("?")[0]

            if "stock.adobe.com" in url:
                link = adobestock(url)
            elif "flaticon.com" in url:
                link = flaticon(url)
            else:
                link = fallback(url)

            with open(file_path[:file_path.rfind(".")] + ".html", "a") as output:
                output.write("\t" + link)
                output.write("\n")

            update_text("Finished parsing & saved href for: " + url, text)

    result_file = file_path[:file_path.rfind(".")] + ".html"
    with open(result_file, "a") as output:
        output.write("</div>")

    update_text("\n\nFinished, saved sources to: " + str(result_file), text)

    if open_folder_var.get():
        update_text("\nOpening folder...", text)
        open_folder(result_file)


# create the main window
root = tk.Tk()

# create the input field and file selection button
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

input_label = tk.Label(input_frame, text="Input file:")
input_label.pack(side=tk.LEFT)

input_file = tk.Entry(input_frame)
input_file.pack(side=tk.LEFT, padx=10)

input_button = tk.Button(input_frame, text="Choose file", command=run_program)
input_button.pack(side=tk.LEFT)

# create the "Run" button
run_button = tk.Button(root, text="Run", command=lambda: run_program())
run_button.pack(pady=10)

# create the checkbox to open folder
open_folder_var = tk.IntVar()
open_folder_checkbutton = tk.Checkbutton(root, text="Open folder after finishing", variable=open_folder_var)
open_folder_checkbutton.pack()

root.mainloop()
