from components.titlebar import TitleBar
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
import customtkinter as ctk
import threading
import pytube
import theme

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.__title = "Youtube Downloader"
        self.geometry("400x450")
        self.resizable(False, False)
        self.attributes('-topmost', True)
        self.attributes('-alpha', 1)
        self.overrideredirect(True)
        self.title(self.__title)

        self.init_widgets()
        self.add_widgets()

    def init_widgets(self) -> None:
        self.titlebar = TitleBar(master=self, title=self.__title)
        self.label_title = ctk.CTkLabel(master=self, text="Youtube Downloader", font=theme.font_title)
        self.text_area = ctk.CTkTextbox(master=self, font=theme.font_small)
        self.text_area.bind("<<Paste>>", self.on_paste) 
        self.combo_download_option = ctk.CTkComboBox(master=self, font=theme.font, values=["Video", "Audio"])
        self.button_convert = ctk.CTkButton(master=self, text="Convert", font=theme.font, fg_color=theme.accent, hover_color=theme.accent_hover, command=self.start_download_thread)
        self.label_progress = ctk.CTkLabel(master=self, text="", font=theme.font)
        self.progress_bar = ctk.CTkProgressBar(master=self, progress_color=theme.accent)
        self.progress_bar.set(0)

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
        threading.Thread(target=self.download, args=(dir, links)).start()

    def download(self, dir, links) -> None:

        for idx, link in enumerate(links, start=1):
            try:
                ytw_url = pytube.YouTube(link, on_progress_callback=self.on_progress)

                if self.combo_download_option.get() == "Audio": stream = ytw_url.streams.filter(only_audio=True).first()
                else: stream = ytw_url.streams.get_highest_resolution()

                self.label_progress.configure(text=f"Downloading {idx}/{len(links)}")
                stream.download(dir)

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

    def get_geometry(self) -> str:
        width, height = map(int, self.geometry().split('x'))
        return f"{width}x{height}"

if __name__ == "__main__":
    ctk.set_default_color_theme("green")
    app = App()
    app.mainloop()