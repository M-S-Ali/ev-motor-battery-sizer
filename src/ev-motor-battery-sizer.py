# Import custom tkinter 
import customtkinter
import math
import matplotlib.pyplot as plt
import numpy as np


# Global UI configuration
customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")

# Main GUI class creation
class App(customtkinter.CTk):
    # class constructor
    def __init__(self):
        # call constructor of inherited class
        super().__init__()

        # Main UI setup
        self.title("EV-Motor-Battery-Sizer")
        self.iconbitmap("assets/motor_icon.ico")
        self.geometry("800x600")

        # setup 4 columns
        for column in range(4):
            self.grid_columnconfigure(column, weight = 1)

        # setup 10 rows
        for row in range(11):
            self.grid_rowconfigure(row, weight = 1)

        label = customtkinter.CTkLabel(self, text = "ELECTRIC VEHICLE MOTOR BATTERY CALCULATOR",font=("",20)) 
        label.grid(row=0, column=0, sticky="nsew", columnspan=4)


        # Make all the labels
        label_array = []
        for column in [0,2]:
            for row in range(1,9):
                label = customtkinter.CTkLabel(self, text=f"({column},{row})")
                label.grid(column=column,row=row,sticky="w",padx=10, pady=10)
                label_array.append(label)

        for column in [0,2]:
            for row in [10,11]:
                label = customtkinter.CTkLabel(self, text=f"({column},{row})")
                label.grid(column=column,row=row,sticky="w",padx=10, pady=10)
                label_array.append(label)

        # Make the Label texts
        label_text_array = [
            "Total Weight with Driver (kg)", "Maximum Speed (km/hr)", "Top speed with Max Accelaration (km/hr)",  "Time for Max Speed Accelaration (s)",
            "Total Range (km)", "Wheel Diameter (inch)", "Battery Voltage", "Frontal Area (m2)", "Mass Coefficent", "Rolling Resistance",
            "Air Density (kg/m2)", "Aerodynamic Coefficent", "Average Speed (km/hr)", "Air Velocity (km/hr)", "Inverter Efficency",
            "Motor Efficency", "Total Motor Power", "Battery Capacity (Ah)", "Wheel RPM","Battery Energy (kWh)"
        ]

        # Configure the Label text to labels
        for i in range(20):
            label_array[i].configure(text=f"{label_text_array[i]}: ")

        # Create all the entry
        self.entry_array = []
        for column in [1,3]:
            for row in range(1,9):
                entry = customtkinter.CTkEntry(self, placeholder_text=f"({column},{row})")
                entry.grid(column=column,row=row,sticky="w",padx=10, pady=10)
                self.entry_array.append(entry)

        for column in [1,3]:
            for row in [10,11]:
                entry = customtkinter.CTkEntry(self, placeholder_text=f"({column},{row})")
                entry.grid(column=column,row=row,sticky="w",padx=10, pady=10)
                self.entry_array.append(entry)

        # Make the entry texts
        entry_text_array = [
            "1645", "144", "100",  "11.5",
            "160", "25", "72", "2", "1.1", "0.0083",
            "1.2", "0.28", "40", "12", "0.95",
            "0.95", "Total Motor Power", "Battery Capacity", "Wheel RPM","Battery Energy (kWh)"
        ]

        # Configure the Label text to labels
        for i in range(20):
            self.entry_array[i].insert(0,f"{entry_text_array[i]}")

        # Configure Buttons
        customtkinter.CTkButton(self, text="PLOT",command = self.plot).grid(column=0,row=9,padx=10, pady=10,columnspan = 2)
        customtkinter.CTkButton(self, text="CALCULATE",command= self.calculate).grid(column=2,row=9,padx=10, pady=10,columnspan = 2)

    def update_input_data(self):
        self.weight = float(self.entry_array[0].get())
        self.max_speed = float(self.entry_array[1].get())*5/18
        self.acc_speed = float(self.entry_array[2].get())*5/18
        self.acc_time = float(self.entry_array[3].get())
        self.range = float(self.entry_array[4].get())
        self.w_diameter = float(self.entry_array[5].get())*0.0254
        self.bat_voltage = float(self.entry_array[6].get())
        self.f_area = float(self.entry_array[7].get())
        self.cm = float(self.entry_array[8].get())
        self.cr = float(self.entry_array[9].get())
        self.a_density = float(self.entry_array[10].get())
        self.cd = float(self.entry_array[11].get())
        self.avg_speed = float(self.entry_array[12].get())*5/18
        self.a_speed = float(self.entry_array[13].get())*5/18
        self.i_efficency = float(self.entry_array[14].get())
        self.m_efficency = float(self.entry_array[15].get())

    def calculate(self):
        self.update_input_data()
        self.power  =   ( ( 0.5 * self.a_density * self.cd * self.f_area * (self.a_speed+self.max_speed)**2) + \
                          ( self.weight * 9.81 * self.cr ) ) * self.max_speed / self.m_efficency
        self.entry_array[16].delete(0,"end")
        self.entry_array[16].insert(0,f"{round((self.power/1000),1)}")

        wheel_rpm = (self.max_speed * 60) / (np.pi * self.w_diameter)
        self.entry_array[18].delete(0,"end")
        self.entry_array[18].insert(0,f"{round(wheel_rpm)}")

        avg_power = ( ( 0.5 * self.a_density * self.cd * self.f_area * (self.a_speed+self.avg_speed)**2) + \
                          ( self.weight * 9.81 * self.cr ) ) * self.avg_speed / self.m_efficency
        
        run_time = self.range / (self.avg_speed*18/5)
        self.entry_array[19].delete(0,"end")
        self.entry_array[19].insert(0,f"{round(avg_power*run_time/1000)}")

        self.entry_array[17].delete(0,"end")
        self.entry_array[17].insert(0,f"{round((avg_power*run_time/self.bat_voltage),1)}")


    def plot(self):

        self.update_input_data()

        # --- Plot 1: Power vs Speed at Different Grades ---
        max_speeds = list(range(0, 201, 20))  # km/h
        max_speeds_mps = [v * 1000 / 3600 for v in max_speeds]  # m/s
        gradeabilities = [0, 2, 4, 9, 15]

        plt.figure(1)  # Open new figure window
        for grade in gradeabilities:
            power_kw = []
            for v in max_speeds_mps:
                aero_force = 0.5 * self.a_density * self.cd * self.f_area * v**2
                rolling_force = self.weight * 9.81 * self.cr * math.cos(math.radians(grade))
                grade_force = self.weight * 9.81 * math.sin(math.radians(grade))
                total_force = aero_force + rolling_force + grade_force

                if self.m_efficency == 0:
                    raise ValueError("Motor efficiency must not be zero.")

                power_required = total_force * v / self.m_efficency
                power_kw.append(power_required / 1000)  # kW

            plt.plot(max_speeds, power_kw, label=f'Grade = {grade}%')

        plt.xlabel("Speed (km/h)")
        plt.ylabel("Power (kW)")
        plt.title("Power vs Speed at Different Grades")
        plt.legend()
        plt.grid(True)

        # --- Plot 2: Tractive Force vs Speed at Different Speed Ratios ---
        plt.figure(2)  # Open another new figure window

        speeds = list(range(180))  # km/h
        speeds_mps = [v * 1000 / 3600 for v in speeds]
        speed_ratios = [2.5, 3.3, 4]

        acc_speed = self.acc_speed
        max_speed = self.max_speed

        for ratio in speed_ratios:
            total_power = ((self.weight * self.cm) / (2 * self.acc_time)) * (acc_speed**2 + (max_speed / ratio)**2)+ \
                            (0.2 * self.a_density * self.cd * self.f_area * acc_speed**3) + \
                           ((2 / 3) * self.weight * 9.81 * self.cr * acc_speed)

            force_kn = []
            for v in speeds_mps:
                v = max(v, 1e-5)  # Avoid divide-by-zero
                limit_speed = max_speed / ratio
                if v < limit_speed:
                    f = total_power / limit_speed
                else:
                    f = total_power / v
                force_kn.append(f/1000)  # N to kN

            plt.plot(speeds, force_kn, label=f'Ratio = {ratio}')

        plt.xlabel("Speed (km/h)")
        plt.ylabel("Force (kN)")
        plt.title("Tractive Force vs Speed at Different Speed Ratios")
        plt.legend()
        plt.grid(True)


# --- Plot 3: Speed vs Time at Different Speed Ratios ---
        plt.figure(3)  # Open another new figure window

        time = list(np.arange(0, 25.2, 0.1))  # secconds
        speed_ratios = [2.5, 3.3, 4]

        acc_speed = self.acc_speed
        max_speed = self.max_speed

        for ratio in speed_ratios:
            total_power = ((self.weight *self.cm) / (2 * self.acc_time)) * (acc_speed**2 + (max_speed / ratio)**2)+ \
                            (0.2 * self.a_density * self.cd * self.f_area * acc_speed**3) + \
                           ((2 / 3) * self.weight * 9.81 * self.cr * acc_speed)

            speed = []
            time_plot = []
            for t in time:
                t = max([0.1,t])
                A = self.a_density * self.cd * self.f_area / 5
                B = self.cm * self.weight /  (2 * t)
                C = 2/3 * self.weight * 9.81 * self.cr
                D = ((self.cm * self.weight /  (2 * t)) * (self.max_speed / ratio)**2) - total_power
                
                roots = np.roots([A,B,C,D])
                s = [r.real for r in roots if np.isreal(r) and r.real > 0]
                if s:
                    s = max(s)
                    speed.append(s*18/5)  # speed in km/hr
                    time_plot.append(t)


            plt.plot(time_plot, speed, label=f'Ratio = {ratio}')

        plt.xlabel("Time (s)")
        plt.ylabel("Speed (km/hr)")
        plt.title("Speed vs Time")
        plt.legend()
        plt.grid(True)

        plt.show()

app = App()
app.mainloop()