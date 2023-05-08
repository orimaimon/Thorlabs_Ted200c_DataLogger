import tkinter as tk
import serial.tools.list_ports
import serial
import time
import tkinter.font as tkFont
import numpy as np
from numpy import log as ln
import threading
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk, Image
import sys
# This code writen by Ori Maimon from Ariel University 2023 Orimaimon2000@gmail.com

write1 = False
Selected_port = False
input_value = 0
Rroom = 10000

# ports = serial.tools.list_ports.comports()
# com = input("Input COM num:")
# COM = "COM"+str(com)
# serialInst = serial.Serial(COM, '9600')
data = ""
T = " "
def COM_Button_command():
    global ports
    global serialInst
    global COM
    global Selected_port
    ports = serial.tools.list_ports.comports()
    COM = "COM" + COM_Entry.get()
    serialInst = serial.Serial(COM, '9600')
    Selected_port= True
    COM_root.destroy()

COM_root = tk.Tk()
# setting title
COM_root.title("Data Logger For TED200C")

# setting window size
width = 250
height = 75
screenwidth = COM_root.winfo_screenwidth()
screenheight = COM_root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
COM_root.geometry(alignstr)
COM_root.resizable(width=False, height=False)

# SET COM

COM_text = tk.Label(COM_root)
ft = tkFont.Font(family='Times', size=10)
COM_text["font"] = ft
COM_text["fg"] = "#333333"
COM_text["justify"] = "center"
COM_text["text"] = "Before you start please select COM PORT:"
COM_text.pack()


COM_Entry = tk.Entry(COM_root)
COM_Entry["bg"] = "#ffffff"
COM_Entry["borderwidth"] = "1px"
ft = tkFont.Font(family='Times', size=10)
COM_Entry["font"] = ft
COM_Entry["fg"] = "#333333"
COM_Entry["justify"] = "center"
COM_Entry["text"] = "Entry"
COM_Entry.pack()

COM_Button = tk.Button(COM_root)
COM_Button["bg"] = "#fad400"
ft = tkFont.Font(family='Times', size=10)
COM_Button["font"] = ft
COM_Button["fg"] = "#000000"
COM_Button["justify"] = "center"
COM_Button["text"] = "Select"
COM_Button["relief"] = "ridge"
COM_Button.pack()
COM_Button["command"] = COM_Button_command





while Selected_port == False:
    COM_root.mainloop()


if Selected_port==True:
    def T_read():
        # ***********************************************#
        # T Read
        global T_formUserStr
        global fileName
        global data
        global T_Thermistor
        global write1
        global file
        firstTime = True

        while True:

            packet = serialInst.readline()

            if write1:

                if firstTime:
                    TextBox.insert(tk.INSERT,"Time[s]" + ',' + "T Thermistor[C]" + ','+"T form User[C]"+'\n')
                    firstTime = False
                    startTime = time.time()
                    fileName = time.strftime("%Y%m%d-%H%M%S") + "data.csv"
                    file = open(fileName, "a")
                    file.write("Time[s]" + ',' + "T Thermistor[C]" + ','+"T form User[C]"+'\n')
                now = time.time()
                Counter = now - startTime
                Vin = float(packet.decode('utf'))
                R_Thermistor = 2.0175*Vin
                if 0.0 < Vin:

                    if 0 < R_Thermistor and R_Thermistor < 681.6:
                        a = 0.0033536166
                        b = 0.000253772
                        c = 0.00000085433271
                        d = -0.000000087912262
                    if 681.6 < R_Thermistor and R_Thermistor < 3599:
                        a = 0.0033530481
                        b = 0.0002542023
                        c = 0.0000011431163
                        d = -0.000000069383563

                    if 3599 < R_Thermistor and R_Thermistor < 32770:
                        a = 0.003354017
                        b = 0.00025617244
                        c = 0.0000021400943
                        d = -0.000000072405219
                    if 32770 < R_Thermistor and R_Thermistor < 692600:
                        a = 0.003357042
                        b = 0.00025214848
                        c = 0.0000033743283
                        d = -0.000000064957311


                    lnR=ln(R_Thermistor/Rroom)
                    T_Thermistor = 1/(a+b*lnR+c*lnR**2+d*lnR**3)-273.15

                    if 'T_formUserStr' in globals():
                        file.write(str(round(Counter,3)) + ',' + str(T_Thermistor) + ','+T_formUserStr+'\n')
                        TextBox.insert(tk.INSERT,str(round(Counter,2)) + ',' + str(round(T_Thermistor,3)) + ','+T_formUserStr+'\n')
                        TextBox.see("end")
                    else:
                        file.write(str(round(Counter,3)) + ',' + str(T_Thermistor) + ','+"Set T"+'\n')
                        TextBox.insert(tk.INSERT,str(round(Counter,3)) + ',' + str(round(T_Thermistor,3))  +",Set T"+'\n')
                        TextBox.see("end")
                elif Vin < 0.0:
                    packet = serialInst.readline()
                    now = time.time()
                    Counter = now - startTime
                    Vin = float(packet.decode('utf'))
                    R_t = Vin / 0.496997091
                    if 'T_formUserStr' in globals():
                        TextBox.insert(tk.INSERT,"T set is:"+T_formUserStr+","+"Connect Vin"+'\n')
                        TextBox.see("end")
                    else:
                        TextBox.insert(tk.INSERT,"Set T"+","+"Connect Vin"+'\n')
                        TextBox.see("end")
                time.sleep(1)

    def GButton_47_command():  # set temp
        
        global T_formUserStr
        global T_set
        global V_out
        T_formUserStr = GLineEdit_473.get()
        T_formUser = float(T_formUserStr)
        T_set = T_formUser + 273.15
        CSV = np.genfromtxt('M.csv', delimiter=',')

        def closest(lst, K):
    	    idx = np.abs(lst - K).argmin()
    	    return idx
        input_value = str(closest(CSV[:,2],T_formUser))
        serialInst.write(input_value.encode())

    
    def GButton_527_command():  # start log
        global write1

        write1 = True


    def GButton_871_command():  # saver
        global file
        global write1
        global input_value
        write1 = False
        serialInst.write(str(input_value).encode())
        file.close()
        root.destroy()
        sys.exit()


    if __name__ == "__main__":
        # *****************************************#
        # GUI setting

        root = tk.Tk()
        # setting title
        root.title("Data Logger For TED200C")
 


        # setting window size
        width = 850
        height = 600
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)


        # **************************************#
        # SET TEMP Button

        GButton_47 = tk.Button(root)
        GButton_47["bg"] = "#fad400"
        ft = tkFont.Font(family='Times', size=10)
        GButton_47["font"] = ft
        GButton_47["fg"] = "#000000"
        GButton_47["justify"] = "center"
        GButton_47["text"] = "SET TEMP"
        GButton_47["relief"] = "ridge"
        GButton_47.place(x=40, y=120, width=150, height=25)
        GButton_47["command"] = GButton_47_command

        # **************************************#
        # Start Logging Button

        GButton_527 = tk.Button(root)
        GButton_527["bg"] = "#31e60d"
        ft = tkFont.Font(family='Times', size=10)
        GButton_527["font"] = ft
        GButton_527["fg"] = "#000000"
        GButton_527["justify"] = "center"
        GButton_527["text"] = "Start Logging"
        GButton_527.place(x=40, y=150, width=150, height=25)
        GButton_527["command"] = GButton_527_command

        # **************************************#
        # **************************************#
        # Temp entry

        GLineEdit_473 = tk.Entry(root)
        GLineEdit_473["bg"] = "#ffffff"
        GLineEdit_473["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        GLineEdit_473["font"] = ft
        GLineEdit_473["fg"] = "#333333"
        GLineEdit_473["justify"] = "center"
        GLineEdit_473["text"] = "Entry"
        GLineEdit_473.place(x=40, y=90, width=150, height=25)
        #GLineEdit_473.place(x=40, y=90, width=150, height=25)
        # **************************************#

        GLabel_390 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_390["font"] = ft
        GLabel_390["fg"] = "#333333"
        GLabel_390["justify"] = "center"
        GLabel_390["text"] = "Form:"
        GLabel_390.place(x=10, y=20, width=70, height=25)

        # **************************************#

        GLabel_420 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_420["font"] = ft
        GLabel_420["fg"] = "#333333"
        GLabel_420["justify"] = "center"
        GLabel_420["text"] = "Consule:"
        GLabel_420.place(x=300, y=20, width=70, height=25)

        # **************************************#

        GLabel_880 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=10)
        GLabel_880["font"] = ft
        GLabel_880["fg"] = "#333333"
        GLabel_880["justify"] = "center"
        GLabel_880["text"] = "Enter temperature [C]:"
        GLabel_880.place(x=30, y=60, width=150, height=25)

        # **************************************#
        # Stop and Save Button

        GButton_871 = tk.Button(root)
        GButton_871["bg"] = "#ff0202"
        ft = tkFont.Font(family='Times', size=10)
        GButton_871["font"] = ft
        GButton_871["fg"] = "#000000"
        GButton_871["justify"] = "center"
        GButton_871["text"] = "Stop and save"
        GButton_871["relief"] = "ridge"
        GButton_871.place(x=40, y=180, width=150, height=25)
        GButton_871["command"] = GButton_871_command

        # **************************************#
        # Data figuer and logger

        TextBox = ScrolledText(root,font=("consolas", "15", "normal"),fg="#49be25")
        TextBox.place(x=280, y=50, width=500, height=500)
        



        t1 = threading.Thread(target=T_read)
        t1.start()

        root.mainloop()

