import customtkinter as ctk
import theme
 
class TitleBar(ctk.CTkFrame):
    def __init__(self, master, title: str):
        super().__init__(master, corner_radius=0)

        self.title_label = ctk.CTkLabel(master=self, text=title, font=theme.font)
        self.title_label.pack(anchor="n", side="left", padx=(10, 0))

        self.close_button = ctk.CTkButton(master=self, text="X", font=theme.font, width=50, corner_radius=0,fg_color=theme.accent, hover_color=theme.accent_hover, command=lambda: exit(0))
        
        self.close_button.pack(anchor="ne", side="right")
        self.pack(fill="x", anchor="n")

        def get_pos(event):
            xwin = master.winfo_x()
            ywin = master.winfo_y()
            startx = event.x_root
            starty = event.y_root

            ywin = ywin - starty
            xwin = xwin - startx

            def move_window(event):
                master.geometry("400x450" + '+{0}+{1}'.format(event.x_root + xwin, event.y_root + ywin))
                startx = event.x_root
                starty = event.y_root

            self.bind('<B1-Motion>', move_window)
            self.title_label.bind('<B1-Motion>', move_window)

        self.bind('<Button-1>', get_pos)
        self.title_label.bind('<Button-1>', get_pos)
