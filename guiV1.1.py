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

# This code writen by Ori Maimon from Ariel University 2022 Orimaimon2000@gmail.com

write1 = False
Selected_port = False

e = 2.71828182846

TempInput = "1"

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
COM_root.iconbitmap('logo_EN-1024x307 (3).ico')

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
        global T
        global write1
        global file
        firstTime = True

        while True:

            packet = serialInst.readline()

            if write1:

                if firstTime:
                    firstTime = False
                    startTime = time.time()
                    fileName = time.strftime("%Y%m%d-%H%M%S") + "data.csv"
                    file = open(fileName, "a")

                now = time.time()
                Counter = now - startTime
                Vin = float(packet.decode('utf'))
                R_t = Vin / 0.496997091
                if 0.0 < Vin:

                    if 0 < R_t and R_t < 681.6:
                        a = 3.35E-03
                        b = 2.54E-04
                        c = 8.54E-07
                        d = -8.79E-08
                    elif 681.6 < R_t and R_t < 3599:
                        a = 3.35E-03
                        b = 2.54E-04
                        c = 1.14E-06
                        d = -6.94E-08
                    elif 3599 < R_t and R_t < 32770:
                        a = 3.35E-03
                        b = 2.56E-04
                        c = 2.14E-06
                        d = -7.24E-08
                    elif 32770 < R_t and R_t < 692600:

                        a = 3.36E-03
                        b = 2.52E-04
                        c = 3.37E-06
                        d = -6.50E-08

                    R_25c = 10.00004098E3
                    lnR = ln(R_t / R_25c)
                    T = 1 / (a + b * lnR + c * lnR ** 2 + d * lnR ** 3) - 273.15

                    # data = Counter+","+T
                elif Vin < 0.0:
                    packet = serialInst.readline()
                    now = time.time()
                    Counter = now - startTime
                    Vin = float(packet.decode('utf'))
                    R_t = Vin / 0.496997091
                    print('Please connect Vin', ('\n'))

                print(Counter, ',', T, ',', packet.decode('utf'), ('\n'))  # ind
                TextBox.insert(tk.INSERT,round(Counter,3))
                TextBox.insert(tk.INSERT, ",")
                TextBox.insert(tk.INSERT, round(T,3)) #need check
                TextBox.insert(tk.INSERT, ",")

                if 'T_formUserStr' in globals():
                    TextBox.insert(tk.INSERT,T_formUserStr)
                else:
                    TEXT = 'User has not set T'
                    TextBox.insert(tk.INSERT,TEXT)

                TextBox.insert(tk.END, ('\n'))
                TextBox.see("end")
                if 'T_formUserStr' in globals():
                    file.write(str(Counter) + ',' + str(T) + ','+T_formUserStr+'\n')
                else:
                    file.write(str(Counter) + ',' + str(T) + '\n')
                time.sleep(1)

    def GButton_47_command():  # set temp
        global e
        global TempInput
        global T_formUserStr
        T_formUserStr = GLineEdit_473.get()
        T_formUser = float(T_formUserStr)
        T_Setting = T_formUser + 273.15
        if 0 < T_Setting and T_Setting < 272:
            A = -1.64E+01
            B = 6.11E+03
            C = -4.41E+05
            D = 2.42E+07
        elif 273 < T_Setting and T_Setting < 322:
            A = -1.55E+01
            B = 5.60E+03
            C = -3.79E+05
            D = 2.50E+07
        elif 323 < T_Setting and T_Setting < 372:
            A = -1.48E+01
            B = 5.16E+03
            C = -2.97E+05
            D = 2.29E+07
        elif 373 < T_Setting and T_Setting < 423:
            A = -1.49E+01
            B = 5.27E+03
            C = -3.54E+05
            D = 3.12E+07
        else:
            pass

        R_25c1 = 10.00004098E3
        S = A + B / T_Setting + C / (pow(T_Setting, 2)) + D / (pow(T_Setting, 3))
        R_tSet = R_25c1 * pow(e, S)
        Vout = 0.5 * R_tSet

        # covers to DigValue

        VoltageValuesArray = [0, 0, 0, 0, 0, 0, 51.7, 118.7, 173.8, 212.8,
                              252.7, 292.2, 330.7, 371.4, 409.8, 449.8,
                              488.5, 527.2, 567.6, 607.3, 647.4, 686.7,
                              727.1, 766.3, 803.5, 843.4, 884.5, 923.2,
                              962.8, 1003.1, 1041, 1081, 1119.6, 1160.7,
                              1199.9, 1240.5, 1278.6, 1319.6, 1358.3,
                              1395.8, 1434, 1474.8, 1512.2, 1551, 1591.6,
                              1630.8, 1670.5, 1710, 1748.7, 1789.3, 1827.9,
                              1865.7, 1910.3, 1945.9, 1991.8, 2027.5, 2066.4,
                              2104.9, 2145.3, 2182.8, 2225.5, 2262.7, 2299.9,
                              2338.8, 2378.8, 2416.4, 2459.2, 2496.1, 2533.1,
                              2576, 2613.9, 2652.2, 2693, 2730.1, 2769.1, 2813.1,
                              2853, 2888.6, 2925.4, 2969.5, 3006.6, 3048, 3085,
                              3118.8, 3165.6, 3202.8, 3239.2, 3283.9, 3321.8, 3359.8,
                              3399.8, 3439.4, 3473, 3514.7, 3552.5, 3595, 3633.4, 3672.7,
                              3715, 3753, 3791.8, 3830.8, 3869.3, 3905.5, 3941.4, 3982.3,
                              4025.9, 4066.2, 4106.6, 4145.2, 4184.6, 4222.6, 4264.8,
                              4298.7, 4335.7, 4375.8, 4417.5, 4455.7, 4495.3, 4534.1,
                              4569.6, 4618.8, 4654.2, 4685.7, 4732, 4772.7, 4805.8, 4849.9,
                              4884.6, 4928.5, 4966.1, 5004, 5047.6, 5081.8, 5122.8, 5156,
                              5197.9, 5235.9, 5275.8, 5315.6, 5355, 5393.6, 5426, 5470.1,
                              5510.2, 5545.3, 5588.8, 5626.9, 5663.9, 5706, 5744.6, 5781.9,
                              5822.7, 5857.1, 5900.4, 5939, 5979.3, 6016.9, 6060.2, 6098.3,
                              6140.5, 6176, 6214.2, 6257.6, 6293.3, 6330.4, 6371.7, 6409.7,
                              6442.5, 6483.5, 6531.3, 6564.1, 6601.8, 6647.4, 6680, 6724.4,
                              6765.3, 6802, 6840.7, 6883.8, 6919.1, 6959.9, 6999.5, 7038.2,
                              7075.1, 7111.3, 7151.7, 7188.4, 7233.6, 7272.1, 7308.2, 7350.6,
                              7390.5, 7422.7, 7464.8, 7507.5, 7545.3, 7584, 7618.2, 7661, 7703.9,
                              7742.1, 7779.7, 7818.1, 7860.5, 7894.9, 7936.9, 7975.5, 8015.1,
                              8055.6, 8090.1, 8131.8, 8170.4, 8208.8, 8251.2, 8287.8, 8327.7,
                              8364.3, 8400.9, 8439.3, 8478.5, 8524.3, 8564, 8603.9, 8641.9,
                              8676.2, 8716.3, 8759.6, 8802, 8842.5, 8875.8, 8917.3, 8953.2,
                              8994.7, 9035.1, 9074.9, 9106.9, 9153.6, 9191.9, 9232.7, 9270.3,
                              9305, 9346.7, 9389.9, 9422.4, 9468, 9501.8, 9546.8, 9595.5,
                              9659.7, 9721.5, 9772.2, 9859, 9883.8, 9905.1, 9911.6]

        def find_nearest(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()
            return idx

        value = Vout
        DigValToUno = find_nearest(VoltageValuesArray, value)

        # if serialInst.in_waiting:
        input_value = str(DigValToUno)
        serialInst.write(input_value.encode())


    def GButton_527_command():  # start log
        global write1

        write1 = True


    def GButton_871_command():  # saver
        global file
        global write1
        global TempInput
        write1 = False
        serialInst.write(TempInput.encode())
        file.close()
        root.destroy()


    if __name__ == "__main__":
        # *****************************************#
        # GUI setting

        root = tk.Tk()
        # setting title
        root.title("Data Logger For TED200C")
        root.iconbitmap('logo_EN-1024x307 (3).ico')


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
        # Ariel Logo
        image_ariel_logo = Image.open("Ariel_U_logo2.jpg")
        Ariel_Logo =  image_ariel_logo.resize((217, 82), Image.ANTIALIAS)
        Ariel_Logo = ImageTk.PhotoImage(Ariel_Logo)

        panel = tk.Label(root, image=Ariel_Logo)
        panel.place(x=40,y=450,width=216, height=82)
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

        # t = np.arange(0, 3, .01)
        # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        #
        # canvas = FigureCanvasTkAgg(T)  # A tk.DrawingArea.
        # canvas.draw()
        # canvas.get_tk_widget().grid(row=5, column=5, pady=50, padx=300, sticky='nsew')

        t1 = threading.Thread(target=T_read)
        t1.start()

        root.mainloop()

