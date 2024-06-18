import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from mpl_toolkits.mplot3d import Axes3D
import csv
import matplotlib.colors as mcolors

def triangle_wave(x, period=2*np.pi):
    """ Generate a triangle wave with a given period. """
    return 2 * np.abs(2 * (x / period - np.floor(x / period + 0.5))) - 1

def update_plot(event=None):
    global inner_lines
    num_turns = num_turns_slider.get()
    start_phi = start_phi_slider.get()
    end_phi = end_phi_slider.get()
    radius = radius_slider.get()
    petal_color = petal_color_var.get()
    wave_type = wave_type_var.get()

    try:
        num_petals = float(num_petals_entry.get())
    except ValueError:
        num_petals = 5.0  # デフォルト値

    # スライダーの値を調整
    if start_phi > end_phi:
        start_phi_slider.set(end_phi)
        start_phi = start_phi_slider.get()
    
    theta = np.linspace(0, num_turns * 2 * np.pi, 1000)
    phi = np.linspace(start_phi, end_phi, 1000)  # 開始立体角と終了立体角を指定

    if wave_type == "sin":
        r = radius * ((1.0/1.3) + (0.3/1.3) * np.sin(num_petals * theta))
    elif wave_type == "square":
        r = radius * ((1.0/1.3) + (0.3/1.3) * np.sign(np.sin(num_petals * theta)))
    elif wave_type == "triangle":
        r = radius * ((1.0/1.3) + (0.3/1.3) * triangle_wave(num_petals * theta))
    
    r2d = r * np.sin(phi)
    x = r2d * np.cos(theta)
    y = r2d * np.sin(theta)
    z = r * np.cos(phi)

    for ax, elev, azim in zip(axes, elevations, azimuths):
        ax.clear()
        ax.plot(x, y, z, color=petal_color, alpha=0.5)  # 軌道を半透明に設定
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim([-radius-0.2, radius+0.2])
        ax.set_ylim([-radius-0.2, radius+0.2])
        ax.set_zlim([-radius-0.2, radius+0.2])
        ax.set_box_aspect([1, 1, 1])  # 等しいスケーリングを設定
        ax.view_init(elev=elev, azim=azim)
    inner_lines = None
    canvas.draw_idle()
    
    global data
    data = []
    r_val = 0  # 離弁花モードでは旋回半径は0
    r_color, g_color, b_color = mcolors.to_rgb(petal_color)
    
    data.append([r_val, num_turns, '', '', '', '', '', '', '', ''])
    
    for i in range(len(theta)):
        diff_yaw = theta[i]
        l_max = r[i]
        phi_val = phi[i]
        data.append([
            '', '', diff_yaw, phi_val, l_max, 0, 0.3, 0, r_color, g_color, b_color
        ])

def show_inner_lines():
    global inner_lines
    if inner_lines is not None:
        return  # すでに表示されている場合は何もしない

    num_turns = num_turns_slider.get()
    start_phi = start_phi_slider.get()
    end_phi = end_phi_slider.get()
    radius = radius_slider.get()
    petal_color = petal_color_var.get()
    wave_type = wave_type_var.get()

    try:
        num_petals = float(num_petals_entry.get())
    except ValueError:
        num_petals = 5.0  # デフォルト値

    theta = np.linspace(0, num_turns * 2 * np.pi, 1000)
    phi = np.linspace(start_phi, end_phi, 1000)  # 開始立体角と終了立体角を指定

    if wave_type == "sin":
        r = radius * ((1.0/1.3) + (0.3/1.3) * np.sin(num_petals * theta))
    elif wave_type == "square":
        r = radius * ((1.0/1.3) + (0.3/1.3) * np.sign(np.sin(num_petals * theta)))
    elif wave_type == "triangle":
        r = radius * ((1.0/1.3) + (0.3/1.3) * triangle_wave(num_petals * theta))
    
    r2d = r * np.sin(phi)
    x = r2d * np.cos(theta)
    y = r2d * np.sin(theta)
    z = r * np.cos(phi)

    inner_lines = []
    for ax in axes:
        for i in range(len(x)):
            line, = ax.plot([x[i], 0], [y[i], 0], [z[i], 0], color=petal_color, alpha=0.5)
            inner_lines.append(line)
    canvas.draw_idle()

def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")[1]
    if color_code:
        petal_color_var.set(color_code)
        update_plot()

def save_csv():
    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
    if file_path:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['r', 'n', 'diff_yaw', 'phi', 'l_max', 'l_min', 'c_max', 'c_min', 'r', 'g', 'b'])
            writer.writerows(data)

def on_start_phi_change(event=None):
    update_plot()

def on_end_phi_change(event=None):
    update_plot()

root = tk.Tk()
root.title("3D Flower Petal Spiral Designer")

fig, axes = plt.subplots(1, 3, subplot_kw={'projection': '3d'}, figsize=(15, 5))

elevations = [0, 30, 90]  # 正面、斜め上、真上
azimuths = [0, 45, 0]     # 正面、斜め上、真上

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

control_frame = tk.Frame(root)
control_frame.pack(side=tk.BOTTOM, fill=tk.X)

num_turns_slider = tk.Scale(control_frame, from_=1, to=20, orient=tk.HORIZONTAL, label="Number of Turns", command=update_plot)
num_turns_slider.set(15)
num_turns_slider.pack(side=tk.LEFT)

start_phi_slider = tk.Scale(control_frame, from_=0, to=np.pi/2, resolution=0.01, orient=tk.HORIZONTAL, label="Start Phi", command=on_start_phi_change)
start_phi_slider.set(0)
start_phi_slider.pack(side=tk.LEFT)

end_phi_slider = tk.Scale(control_frame, from_=0, to=np.pi/2, resolution=0.01, orient=tk.HORIZONTAL, label="End Phi", command=on_end_phi_change)
end_phi_slider.set(np.pi/2)
end_phi_slider.pack(side=tk.LEFT)

radius_slider = tk.Scale(control_frame, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL, label="Radius", command=update_plot)
radius_slider.set(2.0)
radius_slider.pack(side=tk.LEFT)

num_petals_label = tk.Label(control_frame, text="Number of Petals")
num_petals_label.pack(side=tk.LEFT)
num_petals_entry = tk.Entry(control_frame)
num_petals_entry.insert(0, "2.3")
num_petals_entry.pack(side=tk.LEFT)

color_button = tk.Button(control_frame, text="Choose Petal Color", command=choose_color)
color_button.pack(side=tk.LEFT)

petal_color_var = tk.StringVar(value='blue')

wave_type_var = tk.StringVar(value='sin')
wave_type_menu = tk.OptionMenu(control_frame, wave_type_var, "sin", "square","triangle", command=update_plot)
wave_type_menu.pack(side=tk.LEFT)

show_button = tk.Button(control_frame, text="Show Inner Lines", command=show_inner_lines)
show_button.pack(side=tk.LEFT)

save_button = tk.Button(control_frame, text="Save CSV", command=save_csv)
save_button.pack(side=tk.LEFT)

update_plot()
root.mainloop()
