# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import tkinter as tk
# from tkinter import colorchooser, filedialog
# from mpl_toolkits.mplot3d import Axes3D
# import csv
# import matplotlib.colors as mcolors

# def calculate_intersection(x1, angle1, x2, angle2):
#     """Calculate intersection of two lines in 2D space."""
#     m1 = np.tan(np.radians(angle1))
#     m2 = np.tan(np.radians(angle2))
#     if m1 == m2:
#         return None  # Parallel lines or identical slopes
#     z_intersect = (x2 - x1) / (m1 - m2)
#     if 0 <= z_intersect <= 2.0:
#         x_intersect = x1 + z_intersect * m1
#         return x_intersect, z_intersect
#     else:
#         return None

# def update_2d_plot(event=None):
#     x1 = x1_slider.get()
#     x2 = x2_slider.get()
#     x3 = x3_slider.get()
#     angle1 = angle1_slider.get()
#     angle2 = angle2_slider.get()
#     angle3 = angle3_slider.get()
#     num_petals = num_petals_slider.get()
#     wave_angle = wave_angle_slider.get()
    
#     length = 2.0
    
#     x1_coords = np.array([x1, x1 + length * np.sin(np.radians(angle1))])
#     z1_coords = np.array([0, length * np.cos(np.radians(angle1))])
    
#     x2_coords = np.array([x2, x2 + length * np.sin(np.radians(angle2))])
#     z2_coords = np.array([0, length * np.cos(np.radians(angle2))])
    
#     # Calculate x and z coordinates for line 3
#     theta = np.linspace(0, 2 * np.pi, 300)
#     x3_min = x3 + length * np.sin(np.radians(angle3) - np.radians(wave_angle))
#     x3_max = x3 + length * np.sin(np.radians(angle3) + np.radians(wave_angle))
#     z3_min = length * np.cos(np.radians(angle3) - np.radians(wave_angle))
#     z3_max = length * np.cos(np.radians(angle3) + np.radians(wave_angle))
    
#     x3_coords = np.array([x3, x3 + length * np.sin(np.radians(angle3))])
#     z3_coords = np.array([0, length * np.cos(np.radians(angle3))])
    
#     # Calculate intersections
#     intersection_1_2 = calculate_intersection(x1, angle1, x2, angle2)
#     intersection_2_3 = calculate_intersection(x2, angle2, x3, angle3)
    
#     ax2d.clear()
#     ax2d.plot(x1_coords, z1_coords, label='Line 1')
#     ax2d.plot(x2_coords, z2_coords, label='Line 2')
#     ax2d.plot(x3_coords, z3_coords, label='Line 3')
#     ax2d.fill_between([x3, x3_min, x3_max], [0, z3_min, z3_max], alpha=0.2, label='Range of Line 3')
    
#     # Plot intersection points and endpoints
#     p1 = (x1, 0)
#     if intersection_1_2 is not None:
#         p2 = intersection_1_2
#         ax2d.plot(*p2, 'ro')  # Line 1 and Line 2 intersection
#     else:
#         p2 = (x1_coords[1], z1_coords[1])  # Fallback to the end of line 1

#     if intersection_2_3 is not None:
#         p3 = intersection_2_3
#         ax2d.plot(*p3, 'ro')  # Line 2 and Line 3 intersection
#     else:
#         p3 = (x2_coords[1], z2_coords[1])  # Fallback to the end of line 2

#     p4 = (x3_coords[1], z3_coords[1])  # Line 3 top
    
#     ax2d.plot(*p1, 'ro')  # Line 1 bottom
#     ax2d.plot(*p4, 'ro')  # Line 3 top
    
#     ax2d.set_xlim([-5, 5])
#     ax2d.set_ylim([0, 2])
#     ax2d.set_aspect('equal', 'box')
#     ax2d.set_xlabel('X')
#     ax2d.set_ylabel('Z')
#     ax2d.legend()
#     canvas2d.draw_idle()

#     return p1, p2, p3, p4, x3_coords, z3_coords

# def show_3d_plot():
#     p1, p2, p3, p4, x3_coords, z3_coords = update_2d_plot()
    
#     num_petals = num_petals_slider.get()
#     wave_angle = wave_angle_slider.get()
#     petal_color = petal_color_var.get()
    
#     theta = np.linspace(0, 2 * np.pi, 300)
    
#     def rotate_and_plot(ax, start, end, num_petals, wave_angle):
#         x_start, z_start = start
#         x_end, z_end = end
#         x_line = np.linspace(x_start, x_end, 300)
#         z_line = np.linspace(z_start, z_end, 300)
#         for t in theta:
#             angle_offset = np.sin(num_petals * t) * np.radians(wave_angle)
#             X = x_line * np.cos(t)
#             Y = x_line * np.sin(t)
#             Z = z_line * np.cos(angle_offset) - z_line * np.sin(angle_offset)
#             ax.plot(X, Y, Z, color=petal_color, alpha=0.5)
    
#     for ax in ax3d:
#         ax.clear()
#         rotate_and_plot(ax, p1, p2, num_petals, wave_angle)
#         rotate_and_plot(ax, p2, p3, num_petals, wave_angle)
#         rotate_and_plot(ax, p3, p4, num_petals, wave_angle)
#         ax.set_xlabel('X')
#         ax.set_ylabel('Y')
#         ax.set_zlabel('Z')
#         ax.set_xlim([-1, 1])
#         ax.set_ylim([-1, 1])
#         ax.set_zlim([0, 2])
#         ax.set_box_aspect([1, 1, 1])  # Aspect ratio 1:1:1
    
#     # Set different views
#     ax3d[0].view_init(elev=0, azim=90)  # Side view
#     ax3d[1].view_init(elev=30, azim=45)  # Diagonal top view
#     ax3d[2].view_init(elev=90, azim=0)  # Top view
    
#     canvas3d.draw_idle()
    
#     # CSV用のデータ保存
#     save_csv_data(p1, p2, p3, p4, x3_coords, z3_coords, num_petals, wave_angle, petal_color)

# def save_csv_data(p1, p2, p3, p4, x3_coords, z3_coords, num_petals, wave_angle, petal_color):
#     global data
#     data = []
#     r_color, g_color, b_color = mcolors.to_rgb(petal_color)
    
#     def add_line_data(start, end, radius, phi, num_petals, wave_angle,x):
#         x_start, z_start = start
#         x_end, z_end = end
#         diff_yaw_values = np.linspace(0, 2 * np.pi, 300)
#         for t in diff_yaw_values:
#             angle_offset = np.sin(num_petals * t) * np.radians(wave_angle)
#             l_max = np.sqrt((x_end - x)**2 + (z_end - 0)**2)
#             l_min = np.sqrt((x_start - x)**2 + (z_start - 0)**2)
#             data.append([
#                 '', '', t, phi+angle_offset, l_max, l_min, 0.8, 0.4, r_color, g_color, b_color
#             ])
    
#     # メタデータ
#     data.append([x1_slider.get(), 1, '', '', '', '', '', '', '', '', ''])
#     add_line_data(p1, p2, np.linalg.norm(p1), np.arctan2(p2[0]-p1[0], p2[1]-p1[1]), num_petals, 0,x1_slider.get())
#     data.append([x2_slider.get(), 1, '', '', '', '', '', '', '', '', ''])
#     add_line_data(p2, p3, np.linalg.norm(p2), np.arctan2(p3[0]-p2[0], p3[1]-p2[1]), num_petals, 0,x2_slider.get())
#     data.append([x3_slider.get(), 1, '', '', '', '', '', '', '', '', ''])
#     add_line_data(p3, p4, np.linalg.norm(p3), np.arctan2(p4[0]-p3[0], p4[1]-p3[1]), num_petals, wave_angle,x3_slider.get())

# def save_csv():
#     file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
#     if file_path:
#         with open(file_path, 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(['r', 'n', 'diff_yaw', 'phi', 'l_max', 'l_min', 'c_max', 'c_min', 'r', 'g', 'b'])
#             writer.writerows(data)

# def choose_color():
#     color_code = colorchooser.askcolor(title="Choose color")[1]
#     if color_code:
#         petal_color_var.set(color_code)
#         update_2d_plot()

# root = tk.Tk()
# root.title("Conjugate Petal Mode Designer")

# # 2D plot for the cross-section
# fig2d, ax2d = plt.subplots(figsize=(6, 4))
# canvas2d = FigureCanvasTkAgg(fig2d, master=root)
# canvas2d.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# # 3D plot for the trajectory with 3 different views
# fig3d, ax3d = plt.subplots(1, 3, subplot_kw={'projection': '3d'}, figsize=(18, 6))
# canvas3d = FigureCanvasTkAgg(fig3d, master=root)
# canvas3d.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# control_frame = tk.Frame(root)
# control_frame.pack(side=tk.BOTTOM, fill=tk.X)

# x1_slider = tk.Scale(control_frame, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="X1", command=update_2d_plot)
# x1_slider.set(0)
# x1_slider.pack(side=tk.LEFT)

# x2_slider = tk.Scale(control_frame, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="X2", command=update_2d_plot)
# x2_slider.set(-0.3)
# x2_slider.pack(side=tk.LEFT)

# x3_slider = tk.Scale(control_frame, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="X3", command=update_2d_plot)
# x3_slider.set(-0.7)
# x3_slider.pack(side=tk.LEFT)

# angle1_slider = tk.Scale(control_frame, from_=-90, to=90, resolution=1, orient=tk.HORIZONTAL, label="Angle 1", command=update_2d_plot)
# angle1_slider.set(19)
# angle1_slider.pack(side=tk.LEFT)

# angle2_slider = tk.Scale(control_frame, from_=-90, to=90, resolution=1, orient=tk.HORIZONTAL, label="Angle 2", command=update_2d_plot)
# angle2_slider.set(48)
# angle2_slider.pack(side=tk.LEFT)

# angle3_slider = tk.Scale(control_frame, from_=-90, to=90, resolution=1, orient=tk.HORIZONTAL, label="Angle 3", command=update_2d_plot)
# angle3_slider.set(60)
# angle3_slider.pack(side=tk.LEFT)

# num_petals_slider = tk.Scale(control_frame, from_=1, to=10, resolution=1, orient=tk.HORIZONTAL, label="Num Petals", command=update_2d_plot)
# num_petals_slider.set(7)
# num_petals_slider.pack(side=tk.LEFT)

# wave_angle_slider = tk.Scale(control_frame, from_=0, to=30, resolution=1, orient=tk.HORIZONTAL, label="Wave Angle", command=update_2d_plot)
# wave_angle_slider.set(4)
# wave_angle_slider.pack(side=tk.LEFT)

# color_button = tk.Button(control_frame, text="Choose Petal Color", command=choose_color)
# color_button.pack(side=tk.LEFT)

# petal_color_var = tk.StringVar(value='blue')

# show_button = tk.Button(control_frame, text="Show 3D Plot", command=show_3d_plot)
# show_button.pack(side=tk.LEFT)

# save_button = tk.Button(control_frame, text="Save CSV", command=save_csv)
# save_button.pack(side=tk.LEFT)

# update_2d_plot()
# root.mainloop()


#================================


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import colorchooser, filedialog
from mpl_toolkits.mplot3d import Axes3D
import csv
import matplotlib.colors as mcolors

def calculate_intersection(x1, angle1, x2, angle2):
    """Calculate intersection of two lines in 2D space."""
    m1 = np.tan(np.radians(angle1))
    m2 = np.tan(np.radians(angle2))
    if m1 == m2:
        return None  # Parallel lines or identical slopes
    z_intersect = (x2 - x1) / (m1 - m2)
    if 0 <= z_intersect <= 2.0:
        x_intersect = x1 + z_intersect * m1
        return x_intersect, z_intersect
    else:
        return None

def update_2d_plot(event=None):
    x1 = x1_slider.get()
    x2 = x2_slider.get()
    x3 = x3_slider.get()
    angle1 = angle1_slider.get()
    angle2 = angle2_slider.get()
    angle3 = angle3_slider.get()
    num_petals = num_petals_slider.get()
    wave_angle = wave_angle_slider.get()
    
    length = 2.0
    
    x1_coords = np.array([x1, x1 + length * np.sin(np.radians(angle1))])
    z1_coords = np.array([0, length * np.cos(np.radians(angle1))])
    
    x2_coords = np.array([x2, x2 + length * np.sin(np.radians(angle2))])
    z2_coords = np.array([0, length * np.cos(np.radians(angle2))])
    
    # Calculate x and z coordinates for line 3
    theta = np.linspace(0, 2 * np.pi, 300)
    x3_min = x3 + length * np.sin(np.radians(angle3) - np.radians(wave_angle))
    x3_max = x3 + length * np.sin(np.radians(angle3) + np.radians(wave_angle))
    z3_min = length * np.cos(np.radians(angle3) - np.radians(wave_angle))
    z3_max = length * np.cos(np.radians(angle3) + np.radians(wave_angle))
    
    x3_coords = np.array([x3, x3 + length * np.sin(np.radians(angle3))])
    z3_coords = np.array([0, length * np.cos(np.radians(angle3))])
    
    # Calculate intersections
    intersection_1_2 = calculate_intersection(x1, angle1, x2, angle2)
    intersection_2_3 = calculate_intersection(x2, angle2, x3, angle3)
    
    ax2d.clear()
    ax2d.plot(x1_coords, z1_coords, label='Line 1')
    ax2d.plot(x2_coords, z2_coords, label='Line 2')
    ax2d.plot(x3_coords, z3_coords, label='Line 3')
    ax2d.fill_between([x3, x3_min, x3_max], [0, z3_min, z3_max], alpha=0.2, label='Range of Line 3')
    
    # Plot intersection points and endpoints
    p1 = (x1, 0)
    if intersection_1_2 is not None:
        p2 = intersection_1_2
        ax2d.plot(*p2, 'ro')  # Line 1 and Line 2 intersection
    else:
        p2 = (x1_coords[1], z1_coords[1])  # Fallback to the end of line 1

    if intersection_2_3 is not None:
        p3 = intersection_2_3
        ax2d.plot(*p3, 'ro')  # Line 2 and Line 3 intersection
    else:
        p3 = (x2_coords[1], z2_coords[1])  # Fallback to the end of line 2

    p4 = (x3_coords[1], z3_coords[1])  # Line 3 top
    
    ax2d.plot(*p1, 'ro')  # Line 1 bottom
    ax2d.plot(*p4, 'ro')  # Line 3 top
    
    ax2d.set_xlim([-5, 5])
    ax2d.set_ylim([0, 2])
    ax2d.set_aspect('equal', 'box')
    ax2d.set_xlabel('X')
    ax2d.set_ylabel('Z')
    ax2d.legend()
    canvas2d.draw_idle()

    return p1, p2, p3, p4, x3_coords, z3_coords

def show_3d_plot():
    p1, p2, p3, p4, x3_coords, z3_coords = update_2d_plot()
    
    num_petals = num_petals_slider.get()
    wave_angle = wave_angle_slider.get()
    petal_color = petal_color_var.get()
    
    theta = np.linspace(0, 2 * np.pi, 300)
    
    def rotate_and_plot(ax, start, end, num_petals, wave_angle):
        x_start, z_start = start
        x_end, z_end = end
        x_line = np.linspace(x_start, x_end, 300)
        z_line = np.linspace(z_start, z_end, 300)
        for t in theta:
            angle_offset = np.sin(num_petals * t) * np.radians(wave_angle)
            X = x_line * np.cos(t)
            Y = x_line * np.sin(t)
            Z = z_line * np.cos(angle_offset) - z_line * np.sin(angle_offset)
            ax.plot(X, Y, Z, color=petal_color, alpha=0.5)
    
    for ax in ax3d:
        ax.clear()
        rotate_and_plot(ax, p1, p2, num_petals, wave_angle)
        rotate_and_plot(ax, p2, p3, num_petals, wave_angle)
        rotate_and_plot(ax, p3, p4, num_petals, wave_angle)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])
        ax.set_zlim([0, 2])
        ax.set_aspect('auto')  # Adjust the aspect ratio manually
    
    # Set different views
    ax3d[0].view_init(elev=0, azim=90)  # Side view
    ax3d[1].view_init(elev=30, azim=45)  # Diagonal top view
    ax3d[2].view_init(elev=90, azim=0)  # Top view
    
    canvas3d.draw_idle()
    
    # CSV用のデータ保存
    save_csv_data(p1, p2, p3, p4, x3_coords, z3_coords, num_petals, wave_angle, petal_color)

def save_csv_data(p1, p2, p3, p4, x3_coords, z3_coords, num_petals, wave_angle, petal_color):
    global data
    data = []
    r_color, g_color, b_color = mcolors.to_rgb(petal_color)
    
    def add_line_data(start, end, radius, phi, num_petals, wave_angle,x):
        x_start, z_start = start
        x_end, z_end = end
        diff_yaw_values = np.linspace(0, 2 * np.pi, 300)
        for t in diff_yaw_values:
            angle_offset = np.sin(num_petals * t) * np.radians(wave_angle)
            l_max = np.sqrt((x_end - x)**2 + (z_end - 0)**2)
            l_min = np.sqrt((x_start - x)**2 + (z_start - 0)**2)
            data.append([
                '', '', t, phi+angle_offset, l_max, l_min, 0.8, 0.4, r_color, g_color, b_color
            ])
    
    # メタデータ
    data.append([x1_slider.get(), 1, '', '', '', '', '', '', '', '', ''])
    add_line_data(p1, p2, np.linalg.norm(p1), np.pi/2.0-np.arctan2(p2[0]-p1[0], p2[1]-p1[1]), num_petals, 0,x1_slider.get())
    data.append([x2_slider.get(), 1, '', '', '', '', '', '', '', '', ''])
    add_line_data(p2, p3, np.linalg.norm(p2), np.pi/2.0-np.arctan2(p3[0]-p2[0], p3[1]-p2[1]), num_petals, 0,x2_slider.get())
    data.append([x3_slider.get(), 1, '', '', '', '', '', '', '', '', ''])
    add_line_data(p3, p4, np.linalg.norm(p3), np.pi/2.0-np.arctan2(p4[0]-p3[0], p4[1]-p3[1]), num_petals, wave_angle,x3_slider.get())

def save_csv():
    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
    if file_path:
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['r', 'n', 'diff_yaw', 'phi', 'l_max', 'l_min', 'c_max', 'c_min', 'r', 'g', 'b'])
            writer.writerows(data)

def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")[1]
    if color_code:
        petal_color_var.set(color_code)
        update_2d_plot()

root = tk.Tk()
root.title("Conjugate Petal Mode Designer")

# 2D plot for the cross-section
fig2d, ax2d = plt.subplots(figsize=(6, 4))
canvas2d = FigureCanvasTkAgg(fig2d, master=root)
canvas2d.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# 3D plot for the trajectory with 3 different views
fig3d, ax3d = plt.subplots(1, 3, subplot_kw={'projection': '3d'}, figsize=(18, 6))
canvas3d = FigureCanvasTkAgg(fig3d, master=root)
canvas3d.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

control_frame = tk.Frame(root)
control_frame.pack(side=tk.BOTTOM, fill=tk.X)

x1_slider = tk.Scale(control_frame, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="X1", command=update_2d_plot)
x1_slider.set(0)
x1_slider.pack(side=tk.LEFT)

x2_slider = tk.Scale(control_frame, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="X2", command=update_2d_plot)
x2_slider.set(-0.3)
x2_slider.pack(side=tk.LEFT)

x3_slider = tk.Scale(control_frame, from_=-5, to=5, resolution=0.1, orient=tk.HORIZONTAL, label="X3", command=update_2d_plot)
x3_slider.set(-0.7)
x3_slider.pack(side=tk.LEFT)

angle1_slider = tk.Scale(control_frame, from_=-90, to=90, resolution=1, orient=tk.HORIZONTAL, label="Angle 1", command=update_2d_plot)
angle1_slider.set(19)
angle1_slider.pack(side=tk.LEFT)

angle2_slider = tk.Scale(control_frame, from_=-90, to=90, resolution=1, orient=tk.HORIZONTAL, label="Angle 2", command=update_2d_plot)
angle2_slider.set(48)
angle2_slider.pack(side=tk.LEFT)

angle3_slider = tk.Scale(control_frame, from_=-90, to=90, resolution=1, orient=tk.HORIZONTAL, label="Angle 3", command=update_2d_plot)
angle3_slider.set(60)
angle3_slider.pack(side=tk.LEFT)

num_petals_slider = tk.Scale(control_frame, from_=1, to=10, resolution=1, orient=tk.HORIZONTAL, label="Num Petals", command=update_2d_plot)
num_petals_slider.set(7)
num_petals_slider.pack(side=tk.LEFT)

wave_angle_slider = tk.Scale(control_frame, from_=0, to=30, resolution=1, orient=tk.HORIZONTAL, label="Wave Angle", command=update_2d_plot)
wave_angle_slider.set(4)
wave_angle_slider.pack(side=tk.LEFT)

color_button = tk.Button(control_frame, text="Choose Petal Color", command=choose_color)
color_button.pack(side=tk.LEFT)

petal_color_var = tk.StringVar(value='blue')

show_button = tk.Button(control_frame, text="Show 3D Plot", command=show_3d_plot)
show_button.pack(side=tk.LEFT)

save_button = tk.Button(control_frame, text="Save CSV", command=save_csv)
save_button.pack(side=tk.LEFT)

update_2d_plot()
root.mainloop()

