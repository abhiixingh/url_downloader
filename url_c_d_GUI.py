import requests
import os
import tkinter as tk
from tkinter import messagebox
from threading import Thread

class UrlDownloader:
    """ Class to download a file from a given URL. """

    def _extract_filename(self, text_url):
        """ Extracts the file name from the URL. """
        return text_url.split('?')[0].rsplit('/', 1)[1]

    def download(self, text_url, save_folder):
        """ Perform the download and save the content to a file. """
        try:
            response = requests.get(text_url, stream=True)
            response.raise_for_status()  

            filename = self._extract_filename(text_url)

            os.makedirs(save_folder, exist_ok=True)

            file_path = os.path.join(save_folder, filename)
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)

            return f"Downloaded: {filename} to {save_folder}"

        except requests.exceptions.RequestException as e:
            return f"Error occurred: {e}"

def download_file(url, folder, result_var):
    downloader = UrlDownloader()
    result = downloader.download(url, folder)
    result_var.set(result)

def on_download_button_click():
    """ Triggered when the download button is clicked. """
    url = url_entry.get()
    folder = folder_entry.get()

    if not url or not folder:
        messagebox.showwarning("Input Error", "Please enter both a URL and a folder to save the file.")
        return

    result_var.set("Downloading...")
    download_thread = Thread(target=download_file, args=(url, folder, result_var))
    download_thread.start()


root = tk.Tk()
root.title("URL Content Downloader")


url_label = tk.Label(root, text="Enter URL to download:")
url_label.pack(pady=10)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

folder_label = tk.Label(root, text="Enter folder to save file:")
folder_label.pack(pady=10)
folder_entry = tk.Entry(root, width=60)
folder_entry.pack(pady=5)


result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, width=60, height=2, relief="sunken")
result_label.pack(pady=10)

# Download button
download_button = tk.Button(root, text="Start Download", command=on_download_button_click)
download_button.pack(pady=20)

root.mainloop()
