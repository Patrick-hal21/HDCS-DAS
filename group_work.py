import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, ttk
# import CTkGradient as ctkg
from single_linked_list import LinkedList

# for background gradient
class GradientFrame(tk.Canvas):
    def __init__(self, parent, color1, color2, **kwargs):
        super().__init__(parent, **kwargs)
        self.color1 = color1
        self.color2 = color2
        self.bind("<Configure>", self._draw_gradient)

    def _draw_gradient(self, event=None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        (r1, g1, b1) = self.winfo_rgb(self.color1)
        (r2, g2, b2) = self.winfo_rgb(self.color2)
        r_ratio = (r2 - r1) / height
        g_ratio = (g2 - g1) / height
        b_ratio = (b2 - b1) / height

        for i in range(height):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = f"#{nr>>8:02x}{ng>>8:02x}{nb>>8:02x}"
            self.create_line(0, i, width, i, tags=("gradient",), fill=color)
            # self.create_line(i, 0, i, height, tags=("gradient",), fill=color) # for horizontal , change above 'height' to 'width'

    def add_widget(self, widget, x, y, anchor="center"):
        self.update_idletasks()
        self.create_window(x, y, window=widget, anchor=anchor)

def interpolate_color(color1, color2, position, height):
    # Convert hex to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb_color):
        return "#{:02x}{:02x}{:02x}".format(*rgb_color)

    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    ratio = position / height

    interpolated = tuple(
        int(rgb1[i] + (rgb2[i] - rgb1[i]) * ratio)
        for i in range(3)
    )
    return rgb_to_hex(interpolated)

class MyApp():
    def __init__(self, root):
        # ctk.set_appearance_mode("dark")
        self.root = root
        # self.root = tk.Tk()
        self.root.title("Student Name List Manager")

        # To center TKinter window
        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate position
        x = (screen_width // 2) - (609// 2)
        y = (screen_height // 2) - (400 // 2)

        self.root.geometry(f"609x400+{x}+{y}")
        self.root.wm_minsize(609, 400)
    
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Sinlge Linked List
        self.myll = LinkedList()
        self.myll.add("Michael", "Yangon")

        # needed custom lists
        self.tasks = ["Display All Data", "Add Data", "Search and Remove", "Exit"]
        self.tasks_btns = []
        self.pages = []
        self.back_btns = [] # from each page to Home

        # custom style
        style = ttk.Style()
        style.theme_use("clam")  # Enables full header customization

        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))

        style.configure("Treeview.Heading",
                        background="#CE6520",  # Static background
                        foreground="white",   # Optional: clearer text
                        font=("Segoe UI", 12))

        style.map("Treeview.Heading",
                background=[("active", "#CE6520")])  # Prevent hover change

        # Binding ecents (currently dont work as expected)
        root.bind("<Configure>", self.adjust_row_weights)

        # Cretae Main Page
        self.main()
        # self.root.update()

    def main(self):
        # Main Page
        self.gradient_frame = GradientFrame(self.root, "#0d87c0", "#1bd4cb")
        # gradient_frame.grid(row=0, column=0, sticky="nsew")
        self.gradient_frame.place(x=0, y=0, relheight=1, relwidth=1)
        self.gradient_frame.grid_columnconfigure([0,2], weight=1)

        self.title = ctk.CTkLabel(self.gradient_frame, text="Student Name List Manager", font=ctk.CTkFont('Mono', 26, "bold"))
        self.title.grid(row=1, column=1, padx=10, pady=20)


        for n, task in enumerate(self.tasks, 2):
            btn = ctk.CTkButton(self.gradient_frame, text=task, fg_color="#03425E", corner_radius=6, hover_color="#CE1515" if task == "Exit" else "#042D3F", command=self.root.destroy if task == "Exit" else None)
            btn.grid(row=n, column=1, padx=10, pady=30 if task == "Exit" else 10)
            self.tasks_btns.append(btn)

        # btn1.bind("<Button-1>", lambda e: print("Hello"))

        # pages
        for task in self.tasks[:-1]:
            pg = GradientFrame(self.root, "#0d87c0", "#1bd4cb")
            self.pages.append(pg)
            # label = tk.Label(pg, text=f"{task} Page", font=("Mono", "20"))
            # label.grid(row=0, column=0, padx=10, pady=10)

            back_btn = ctk.CTkButton(pg, text="Back to Home", fg_color="green", bg_color="#0d87c0", corner_radius=5, hover_color="#17a71f")
            back_btn.grid(row=1, column=0, padx=3, pady=10, sticky="w")
            self.back_btns.append(back_btn)

        # Bind Buttons and Commands
        for task in self.tasks[:-1]:
            pg_index = self.tasks.index(task) 
            self.tasks_btns[pg_index].bind("<Button-1>", lambda e, pg = self.pages[pg_index]: self.switch_pages(self.gradient_frame, pg))

            # initial set, later I will change this
            self.back_btns[pg_index].bind("<Button-1>", lambda e, pg = self.pages[pg_index]: self.switch_pages(pg, self.gradient_frame))

        self.root.after(100, lambda : self.set_color())

        # Display All Data Page
        # add_treeview()
        self.tasks_btns[0].bind("<Button-1>", lambda e :  (self.display_all_data(), self.set_color()))

        # Add Data Page
        self.tasks_btns[1].bind("<Button-1>", lambda e :  (self.add_data_pg(), self.set_color()))
        # Search Data Page
        self.tasks_btns[2].bind("<Button-1>", lambda e :  (self.search_page(), self.set_color()))
        # self.root.update()
        # self.set_color()

    # secondary functions 
    def adjust_row_weights(self, event):
        try:
            # root.update_idletasks()
            if self.gradient_frame.winfo_height() < 700:
                
                self.title.configure(font=ctk.CTkFont('Mono', 24, "bold"))

                self.gradient_frame.grid_rowconfigure(0, weight=1)
                self.gradient_frame.grid_rowconfigure(len(self.tasks)+2, weight=3)

                self.title.grid(row=1, column=1, padx=10, pady=20)
                for btn in self.tasks_btns:
                    btn.configure(height=28)

            elif self.gradient_frame.winfo_height() > 700:
                for btn in self.tasks_btns:
                    btn.configure(height=32)

                self.title.grid(row=1, column=1, padx=10, pady=40)
                self.title.configure(font=ctk.CTkFont('Mono', 26, "bold"))
                self.gradient_frame.grid_rowconfigure(0, weight=0)

            # self.set_color()
            self.root.update_idletasks()
            self.root.update()

        except tk.TclError:
            pass


    def switch_pages(self, old, new): # I can use current and new parameter to toggle
        # for frames' visibilty testing 
        '''
        if gradient_frame.winfo_ismapped():
            print("Page-1 can be seen")
            if not pg2.winfo_ismapped():
                print("But not page-2")

        elif pg2.winfo_ismapped():
            print("Page-1 can be seen")
            if not gradient_frame.winfo_ismapped():
                print("But not page-2")
        '''
        # if gradient_frame.winfo_ismapped():
        #     gradient_frame.place_forget()

        #     pg2.place(x=0, y=0, relheight=1, relwidth=1)

        # elif pg2.winfo_ismapped():
        #     pg2.place_forget()

        #     gradient_frame.place(x=0, y=0, relheight=1, relwidth=1)

        # with parameters
        # print(old, new)
        old.place_forget()
        self.root.after(100)
        new.place(x=0, y=0, relheight=1, relwidth=1)
        new.update_idletasks()
        self.root.update()

    ## visibility happens after a brief delay or an event.
    ## root.after(100, lambda: switch_pages())


    # optional
    def set_color(self):
        self.root.update_idletasks()

        title_y = self.title.winfo_y()
        
        try:
            try:
                # self.addPage.update_idletasks()
                flabel_y = self.fname_label.winfo_y()
                address_label_y = self.address_label.winfo_y()
                addPage_height= self.addPage.winfo_height()
                add_btn_y = self.add_btn.winfo_y()

                label_bg_color = interpolate_color("#0d87c0", "#1bd4cb", flabel_y, addPage_height)
                address_label_bg_color = interpolate_color("#0d87c0", "#1bd4cb", address_label_y, addPage_height)
                add_btn_color = interpolate_color("#0d87c0", "#1bd4cb", add_btn_y, addPage_height)

                self.fname_label.configure(bg_color=label_bg_color)
                self.address_label.configure(bg_color=address_label_bg_color)
                self.add_btn.configure(bg_color=add_btn_color)
                # self.addPage.update_idletasks()
            except Exception as e:
                # print(f"Error in setting color for Add Page: {e}")
                pass
                try:
                    # for search and remove pages
                    self.bg_color_for_widget(self.searchPage, self.search_name, self.search_address, self.search_btn, self.remove_btn, self.searchResult)
                except Exception as e:
                    # print(f"Error in setting color for Search Page: {e}")
                    pass
        except:
            pass # may be add page' widgets are not built yet
        # name_entry.configure(bg_color=label_bg_color)

        
        gradient_height = self.gradient_frame.winfo_height()

        for btn in self.tasks_btns:
            btn_y = btn.winfo_y() # Get y position of button
            color = interpolate_color("#0d87c0", "#1bd4cb", btn_y, gradient_height)
            btn.configure(bg_color = color)
    
        for btn in self.back_btns:
            btn_y = btn.winfo_y() # Get y position of button
            color = interpolate_color("#0d87c0", "#1bd4cb", btn_y, gradient_height)
            btn.configure(bg_color = color)
        
        color_at_title = interpolate_color("#0d87c0", "#1bd4cb", title_y, gradient_height)
        self.title.configure(fg_color = color_at_title)
        # self.root.update_idletasks()

    def bg_color_for_widget(self, main_pg, fwidget, swidget, fbtn, sbtn, msg):
   
        flabel_y = fwidget.winfo_y()
        address_label_y = swidget.winfo_y()
        Page_height= main_pg.winfo_height()
        btn_y = fbtn.winfo_y()
        msg_y = msg.winfo_y() if msg else btn_y+30

        name_bg_color = interpolate_color("#0d87c0", "#1bd4cb", flabel_y, Page_height)
        address_bg_color = interpolate_color("#0d87c0", "#1bd4cb", address_label_y, Page_height)
        btn_color = interpolate_color("#0d87c0", "#1bd4cb", btn_y, Page_height)
        msg_bg_color = interpolate_color("#0d87c0", "#1bd4cb", msg_y, Page_height)

        fwidget.configure(bg_color=name_bg_color)
        swidget.configure(bg_color=address_bg_color)

        fbtn.configure(bg_color=btn_color)
        sbtn.configure(bg_color=btn_color)

        msg.configure(bg_color=msg_bg_color)

# def adjust_bg_color(master, widget):
#     master_height = master.winfo_height()
#     widget_height = widget.winfo_y()

#     color = interpolate_color("#0d87c0", "#1bd4cb", widget_height, master_height)
#     widget.configure(bg_color=color)

#     master.update_idletasks()

    # Add Treeview to Display, Search
    def add_treeview(self, master, row_n, column_n, colspan_val=1, display_all=False):

        holder = tk.Frame(master)
        holder.grid(row = row_n, column=column_n, columnspan=colspan_val, padx=3, pady=10, sticky="nsew")
        holder.grid_rowconfigure(0, weight=1)
        holder.grid_columnconfigure(0, weight=1)


        display_box = ttk.Treeview(holder, columns=("Serial", "Name", "Address"), show="headings", style="Treeview")
        display_box.heading("Serial", text = "No.")
        display_box.heading("Name", text="Student Name")
        display_box.heading("Address", text="Student Address")

        display_box.column("Serial", anchor="w", width=50)
        display_box.column("Name", anchor="w")
        display_box.column("Address", anchor="w")

        self.back_btns[0].bind("<Button-1>", lambda e :  display_box.destroy())

        # for i in range(1,100):
        #     display_box.insert("", "end", values=(i, "John Doe", "123 Elm St"))
        if display_all:
            if self.myll:
                if self.myll.head is None:
                    noti = "Empty Data!"
                    self.no_data_or_not.configure(text=noti)
                   
                else:
                    self.no_data_or_not.grid_forget()  # Hide the label if data is available
                    node = self.myll.head
                    i = 1
                    while node:
                        name = node.data
                        address = node.metadata
                        display_box.insert("", "end", values=(i, name, address))
                        node = node.next  # Advance to next node
                        i += 1

        x_scroll = ctk.CTkScrollbar(holder, orientation="horizontal", corner_radius=10, height=18, button_hover_color="#4195cc")
        v_scroll = ctk.CTkScrollbar(holder, orientation="vertical", corner_radius=10, width=18, button_hover_color="#4195cc")

        display_box.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1,column=0, sticky="ew")

        display_box.configure(yscrollcommand=v_scroll.set)
        v_scroll.configure(command=display_box.yview)

        display_box.configure(xscrollcommand=x_scroll.set)
        x_scroll.configure(command=display_box.xview)

        # display_box.pack(fill="x", expand=True, side="top", padx=10, pady=10, anchor="n")
        self.root.update_idletasks()
        return display_box


    ## Display All Data page
    def display_all_data(self):
        display_all_data_pg = self.pages[0]
        display_all_data_pg.grid_columnconfigure(0, weight=1)
        display_all_data_pg.grid_rowconfigure(3, weight=1)

        self.no_data_or_not = ctk.CTkLabel(display_all_data_pg, text="No Data Available", font=ctk.CTkFont('Mono', 16), bg_color="#118dc7")
        self.no_data_or_not.grid(row=2, column=0, padx=10, sticky="nsew")

        self.root.update_idletasks()
        self.root.update()

        display_box = self.add_treeview(display_all_data_pg, 3, 0, 1, True)
    

    # Add Data page
    def add_data_pg(self):
        
        self.addPage = self.pages[1]
        self.addPage.grid_columnconfigure([0,1], weight=1)

        # First Name
        self.fname_label = ctk.CTkLabel(self.addPage, text="Student Name:", font=ctk.CTkFont('Mono', 16), bg_color="#118dc7")
        self.fname_label.grid(row=2, column=0, pady=10, padx=10)
        # ctk.CTkLabel(addPage, text="*", text_color="red", bg_color="#118dc7").grid(row=2, column=0, padx=50, pady=10, sticky="e") # to add asterick 

        name_entry = ctk.CTkEntry(self.addPage, placeholder_text="Enter student name", font=ctk.CTkFont('Mono', 14), bg_color="#0d87c0", width=150)
        name_entry.grid(row=2, column=1, pady=10, sticky="w")

        name_entry.bind("<FocusIn>", lambda e : self.chg_color_on_focus(name_entry))
        name_entry.bind("<FocusOut>", lambda e : self.chg_color_on_focus(name_entry, True))

        # Address
        self.address_label = ctk.CTkLabel(self.addPage, text="Address:", font=ctk.CTkFont('Mono', 16), bg_color="#118dc7")
        self.address_label.grid(row=3, column=0, pady=10, padx=10)

        address_entry = ctk.CTkEntry(self.addPage, placeholder_text="Enter Address", font=ctk.CTkFont('Mono', 14), bg_color="#0d87c0", width=150)
        address_entry.grid(row=3, column=1, pady=10, sticky="w")

        address_entry.bind("<FocusIn>", lambda e : self.chg_color_on_focus(address_entry))
        address_entry.bind("<FocusOut>", lambda e : self.chg_color_on_focus(address_entry, True))

        #  add button
        self.add_btn = ctk.CTkButton(self.addPage, text="Add Data", fg_color="#03425E", bg_color="#10b9b1", corner_radius=6, hover_color="#042D3F")
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=20)

        # self.root.update()

        self.add_btn.bind("<Button-1>", lambda e: self.add_save_data(name_entry, address_entry))

        # self.addPage.update_idletasks()              

        self.back_btns[1].bind("<Button-1>", lambda e: self.clear_children(self.addPage))

        # self.tasks_btns[1].bind("<Button-1>", lambda e: self.add_data_pg())

    # to clear children widgets when back to main page
    def clear_children(self, parent):
        for widget in parent.winfo_children()[1:]:
            widget.destroy()

    def chg_color_on_focus(event, entry, out=False):
        if out:
            entry.configure(border_color="#7f7f7f")
        else:
            entry.configure(border_color="#0C0A99")

    def add_save_data(self, name_entry, address_entry):
        name = name_entry.get().strip()
        address = address_entry.get().strip()

        if not name:
            messagebox.showwarning("Required Field", "Please fill in the Student Name Field.")
            return
        # if not address:
        #     messagebox.showwarning("Required Field", "Please fill in the Address Field.")
        #     return
        
        address = address if address else "No Address Provided"  # Default value if address is empty
        
        # Check if there is same data
        if self.myll:
            if self.myll.head is None:
                self.myll.add(name, address)
                messagebox.showinfo("Success", f"Data added: {name}, {address}")
            else:
                node = self.myll.head
                i = 1
                while node:
                    name_data = node.data
                    address_data = node.metadata
                    if name_data == name and address_data == address:
                        messagebox.showwarning("Duplicate Entry", "Data already exists!")
                        break
                    node = node.next  # Advance to next node
                    i += 1
                else:
                    self.myll.add(name, address)
                    messagebox.showinfo("Success", f"Data added: {name}, {address}")
        # self.myll.add(name, address)
        # messagebox.showinfo("Success", f"Data added: {name}, {address}")
        
        # Clear entries after adding
        name_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END) if address_entry.get() else None
        
        print(self.myll.display())
        self.addPage.focus_set()
        # return
        # self.root.update_idletasks()
        # return

    # Search Page
    def search_page(self):
        self.searchPage = self.pages[2]
        self.searchPage.grid_columnconfigure([0,1], weight=1)
        self.searchPage.grid_rowconfigure(6, weight=1)
        # Name
        self.search_name = ctk.CTkLabel(self.searchPage, text="Student Name:", font=ctk.CTkFont('Mono', 16), bg_color="#118dc7")
        self.search_name.grid(row=2, column=0, pady=5, padx=10)

        self.search_name_entry = ctk.CTkEntry(self.searchPage, placeholder_text="Enter Student Name", font=ctk.CTkFont('Mono', 14), bg_color="#0d87c0")
        self.search_name_entry.grid(row=2, column=1, pady=5, padx=10, sticky="w")
        # Address
        self.search_address = ctk.CTkLabel(self.searchPage, text="Address:", font=ctk.CTkFont('Mono', 16), bg_color="#118dc7")
        self.search_address.grid(row=3, column=0, pady=5, padx=10)

        self.search_address_entry = ctk.CTkEntry(self.searchPage, placeholder_text="Enter Address", font=ctk.CTkFont('Mono', 14), bg_color="#0d87c0")
        self.search_address_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")
        
        # Bind events 
        for entry in [self.search_name_entry, self.search_address_entry]:
            entry.bind("<FocusIn>", lambda e , ent = entry: self.chg_color_on_focus(ent))
            entry.bind("<FocusOut>", lambda e, ent = entry: self.chg_color_on_focus(ent, True))

        # Search Button
        self.search_btn = ctk.CTkButton(self.searchPage, text="Search Data", fg_color="#03425E", bg_color="#10b9b1", corner_radius=6, hover_color="#042D3F")
        self.search_btn.grid(row=4, column=0, pady=10, padx=10, sticky="e")

        # Remove Button
        self.remove_btn = ctk.CTkButton(self.searchPage, text="Remove Data", fg_color="grey", bg_color="#10b9b1", corner_radius=6, hover_color="#042D3F", state="disabled")
        self.remove_btn.grid(row=4, column=1, pady=10, padx=10, sticky="w")

        # TO show number of searched data or not / No Data Found!
        self.searchResult = ctk.CTkLabel(self.searchPage, text="", font=ctk.CTkFont('Mono', 16), bg_color="#24a9d1")
        self.searchResult.grid(row=5, column=0,  columnspan=2, padx=10, sticky="nsew")

        search_box = self.add_treeview(self.searchPage, 6, 0, 2)
        
        self.selected_data = [] # for removing data
        self.current_selection = ""

        # Bind treeview selection event
        search_box.bind("<<TreeviewSelect>>", lambda e : self.select_data(search_box))

        # Bind clear childern actions to back
        self.back_btns[2].bind("<Button-1>", lambda e: self.clear_children(self.searchPage))
        # Search btn
        self.search_btn.bind("<Button-1>", lambda e: self.search_data(search_box, self.searchResult))
        # Remove btn
        self.remove_btn.bind("<Button-1>", lambda e: self.remove_data_metadata(search_box))

    # search data
    def search_data(self, treeview, msg):
        name = self.search_name_entry.get().strip()
        address = self.search_address_entry.get().strip()

        if not name:
            messagebox.showwarning("Required Field", "Please fill in the Student Name Field.")
            return
        
        # if not address:
        #     messagebox.showwarning("Required Field", "Please fill in the Address Field.")
        #     return

        # Search in linked list
        searched_data = self.myll.search(name) # return list of node(s) if found, else None
        if searched_data:
            for item in treeview.get_children():
                treeview.delete(item)
            
            lng = len(searched_data)

            msg.configure(text=f"Found {lng} data(s) with name '{searched_data[0].data}'.")
            # Insert found data into treeview (now this will be only 1 data cuz search(0 returns only first found data)
            treeview.insert("", "end", values=(1, searched_data[0].data, searched_data[0].metadata))
        else:
            msg.configure(text="No Data Found!")
            for item in treeview.get_children():
                treeview.delete(item)


    def select_data(self, treeview=ttk.Treeview):
        try:
            # if user select data , enablesremove button
            self.selected_data.clear() # clear data for each selection 

            selected_item = treeview.selection()[0] # row text

            if self.current_selection != selected_item: # check this is currently in selection
                self.remove_btn.configure(fg_color="#03425E", state="normal") # enable remove btn

                item_value = treeview.item(selected_item, "values") # I used values to add data
                name_address = item_value[1:]
                self.selected_data.append(name_address)

                self.current_selection = selected_item

                print(self.selected_data[0])
            else:
                self.remove_btn.configure(fg_color="grey", state="disabled") # disable remove btn
                self.current_selection = "" # clear to be able to select again
                treeview.selection_set(())

        except Exception:
            treeview.selection_set(())

    def remove_data_metadata(self, treeview):
        if self.remove_btn._state == "normal":
            data = self.selected_data[0] # contains Name and Address
            if data:
                name, address = data
                confirm = messagebox.askokcancel("Confirmation", f"You are going to delete Student data with \n Name : '{name}\n Address : '{address}")

                if confirm:
                    result_msg, status = self.myll.remove(name, address)

                    if status:
                        # remove data and clear treeview
                        self.search_name_entry.delete(0, tk.END)
                        self.search_name_entry.delete(0, tk.END)
                        treeview.delete(*treeview.get_children())
                        self.searchResult.configure(text="")

                        self.remove_btn.configure(fg_color="grey", state="disabled") # disable remove btn
                        self.current_selection = "" # clear to be able to select again
                        treeview.selection_set(())

                        # SHow msg
                        messagebox.showinfo("Success!", result_msg)
                    
                    else:
                        messagebox.showerror("Failure!", result_msg)
                else:
                    pass


    def set_to_default_style(self, parent, entries:list, treeview = None):
        for entry in entries:
            entry.delete(0, tk.END) if entry.get() else None # Clear the entry
        
        parent.focus_set()

        if treeview:
            for item in treeview.get_children():
                treeview.delete(item)


    '''
    info = frame.grid_info()
    frame.grid_forget()
    # Restore with info
    frame.grid(**info)
    '''


# Main function to run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()