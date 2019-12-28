import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter.ttk import *

from xml_viewer import XML_Viwer
import xml.etree.ElementTree as ET
import numpy as np

DEBUG  = True
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.xml_string = ""


    def create_widgets(self):
        self.winfo_toplevel().title("URDF Generator")

        self.b_0 = tk.Button(self)
        self.b_0["text"] = "Select extent URDF"
        self.b_0["command"] = self.get_urdf_extent_file
        self.b_0.pack(side="top")

        self.b_1 = tk.Button(self)
        self.b_1["text"] = "Select URDF"
        self.b_1["command"] = self.get_urdf_file
        self.b_1.pack(side="top")

        self.l_1_v = tk.StringVar()
        self.l_1 = tk.Label(self.master, textvariable=self.l_1_v)
        self.l_1.pack(side="top")

        self.b_2 = tk.Button(self)
        self.b_2["text"] = "Select generation directory"
        self.b_2["command"] = self.get_save_directory
        self.b_2.pack(side="top")

        self.l_2_v = tk.StringVar()
        self.l_2 = tk.Label(self.master, textvariable=self.l_2_v)
        self.l_2.pack(side="top")

        self.b_3 = tk.Button(self)
        self.b_3["text"] = "Set generation #"
        self.b_3["command"] = self.set_num_gens
        self.b_3.pack(side="top")

        self.l_3_v = tk.StringVar()
        self.l_3 = tk.Label(self.master, textvariable=self.l_3_v)
        self.l_3.pack(side="top")

        self.i_3 = tk.Entry(self)
        self.i_3.insert(10, "15")
        self.i_3.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

        self.b_4 = tk.Button(self, fg="green")
        self.b_4["text"] = "Generate"
        self.b_4["command"] = self.generate
        self.b_4.pack(side="top")

        self.progress = Progressbar(root, orient = tk.HORIZONTAL, 
              length = 100, mode = 'determinate') 
        self.progress.pack(side="bottom")

    def get_urdf_file(self):
        if DEBUG:
            root.filename = "example.xml"
        else:
            root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("URDF files","*.xml"),("all files","*.*")))
        self.urdf_master = root.filename
        self.l_1_v.set("Using base URDF:\n" + self.urdf_master + "\n")
        print("Using base URDF:\n" + self.urdf_master + "\n")

        # load xml into string
        self.xml_string = open(self.urdf_master).read()
        # display
        self.urdf_tree = XML_Viwer(root, self.xml_string, heading_text="Original").pack(side="left")
    
    def get_urdf_extent_file(self):
        if DEBUG:
            root.filename = "example_extent.xml"
        else:
            root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("URDF files","*.xml"),("all files","*.*")))
        self.urdf_extent_master = root.filename
        self.l_1_v.set("Using extent URDF:\n" + self.urdf_extent_master + "\n")
        print("Using extent URDF:\n" + self.urdf_extent_master + "\n")

        # load xml into string
        self.xml_extent_string = open(self.urdf_extent_master).read()
        # display
        self.urdf_extent_tree = XML_Viwer(root, self.xml_extent_string, heading_text="Extent").pack(side="right")

    def get_save_directory(self):
        if DEBUG:
            root.filename = "generated"
        else:
            root.filename =  filedialog.askdirectory()
        self.save_directory = root.filename
        self.l_2_v.set("Will save generated URDFs to:\n" + self.save_directory + "\n")
        print("Will save generated URDFs to:\n" + self.save_directory + "\n")
    
    def set_num_gens(self):
        self.num_generations = self.i_3.get()
        self.l_3_v.set("# of Generations: " + str(self.num_generations))

    def generate(self):
        # print(self.urdf_tree._element_tree)
        tree = ET.parse(self.urdf_master)
        root = tree.getroot()
        print(root.tag)
        print(root.attrib)
        for child in root:
            print(child.tag)
            print(child.attrib)
            print(len(child))
        mean = 5
        std = 1
        print(np.random.normal(mean,std,int(self.num_generations)))

        for i in range(int(self.num_generations)):
            self.progress['value'] = (int(i)+1)/int(self.num_generations)*100

            new_tree = ET.parse(self.urdf_master)
            new_root = new_tree.getroot()

            mean_tree = ET.parse(self.urdf_master)
            mean_root = mean_tree.getroot()

            std_tree = ET.parse(self.urdf_extent_master)
            std_root = std_tree.getroot()

            new_tree.write(self.save_directory + "/generated_" + str(i) + ".xml")
        

root = tk.Tk()
app = Application(master=root)

# xml = """
# <messages>
#     <note id="501">
#     <to>Tove</to>
#     <from>Jani</from>
#     <heading>Reminder</heading>
#     <body>Don't forget me this weekend!</body>
#     </note>
#     <note id="502">
#     <to>Jani</to>
#     <from>Tove</from>
#     <heading>Re: Reminder</heading>
#     <body>I will not</body>
#     </note>
# </messages>"""
# XML_Viwer(root, xml, heading_text="Original").pack(side="left")
# XML_Viwer(root, xml, heading_text="Extent").pack(side="right")

app.mainloop()