from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
import customtkinter as ctk
import threading
import pytube

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.resizable(False, False)
        self.title("Youtube Downloader")

        self.init_widgets()
        self.add_widgets()

    def init_widgets(self) -> None:
        self.label_title = ctk.CTkLabel(master=self, text="Youtube Downloader", font=("Roboto", 30))
        self.text_area = ctk.CTkTextbox(master=self, font=("Roboto", 14))
        self.text_area.bind("<<Paste>>", self.on_paste) 
        self.combo_download_option = ctk.CTkComboBox(master=self, font=("Roboto", 16), values=["Video", "Audio"])
        self.button_convert = ctk.CTkButton(master=self, text="Convert", font=("Roboto", 16), command=self.start_download_thread)
        self.label_progress = ctk.CTkLabel(master=self, text="", font=("Roboto", 16))
        self.progress_bar = ctk.CTkProgressBar(master=self)
        self.progress_bar.set(-1)

    def add_widgets(self) -> None:
        self.label_title.pack(padx=15, pady=5)
        self.text_area.pack(fill="both", expand=True, padx=15, pady=5)
        self.combo_download_option.pack(padx=15, pady=5)
        self.button_convert.pack(padx=15, pady=(5,15))
        self.label_progress.pack(padx=15, pady=(5,0))
        self.progress_bar.pack(padx=15, pady=5)

    def start_download_thread(self) -> None:
        dir = filedialog.askdirectory(title="Select a directory")
        links = [line for line in self.text_area.get("1.0", "end-1c").split('\n') if line.strip()]
        self.label_progress.configure(text="Starting...")
        self.combo_download_option.configure(state="disabled")
        self.progress_bar.set(0)
        threading.Thread(target=self.download, args=(dir, links)).start()

    def download(self, dir, links) -> None:
        self.history = open("download_history.txt", "a")

        for idx, link in enumerate(links, start=1):
            try:
                ytw_url = pytube.YouTube(link, on_progress_callback=self.on_progress)

                if self.combo_download_option.get() == "Audio": stream = ytw_url.streams.filter(only_audio=True).first()
                else: stream = ytw_url.streams.get_highest_resolution()

                self.label_progress.configure(text=f"Downloading {idx}/{len(links)}")
                stream.download(dir)
                self.download_history_file.write(f"{link}\n")

            except Exception as e: 
                print(f"Error downloading {link}: {e}")
                CTkMessagebox(title="Error", message=e, option_1="Ok")

        self.on_complete()

    def on_paste(self, event) -> None:
        self.text_area.after(1, lambda: self.text_area.insert("insert", "\n"))

    def on_progress(self, stream, chunk, remaining) -> None:
        size = stream.filesize
        downloaded = size - remaining
        chunk_size = len(chunk)
        completion = (downloaded + chunk_size) / size
        self.progress_bar.set(completion)

    def on_complete(self) -> None:
        self.label_progress.configure(text="Finished")
        self.combo_download_option.configure(state="normal")
        self.text_area.delete("1.0", "end-1c") 
        self.history.close()

if __name__ == "__main__":
    app = App()
    app.mainloop()