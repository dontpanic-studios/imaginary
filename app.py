import customtkinter, os, qemutool, json
customtkinter.set_default_color_theme('.\\src\\themes\\color.json')

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.title('Imaginary')
        self.geometry('1600x900')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.vmFrame = customtkinter.CTkFrame(self)
        self.vmFrame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")

        self.vmShow = customtkinter.CTkFrame(self)

        vmList = [name for name in os.listdir('.\\src\\vm\\') if os.path.isdir(os.path.join('.\\src\\vm\\', name))]
        num = 0

        for i in vmList:
            num = num + 1
            with open("./src/vm/" + i + "/metadata.json") as jsonData:
                    d = json.load(jsonData)
                    jsonData.close()
                    print(f"reading vm metadata: {d}")
                    self.vmBtn = customtkinter.CTkButton(self.vmFrame, text=i, command=self.button_callback(d))
                    self.vmBtn.grid(row=num, column=0, padx=10, pady=(10, 0), sticky="w")
        
    def button_callback(self, d):
        qemutool.runQemu(d["iso_loc"], d["disk_loc"], d["mem_size"], d["sys_core"]) 

app = App()
app.mainloop()        