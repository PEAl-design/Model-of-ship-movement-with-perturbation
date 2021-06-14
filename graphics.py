import matplotlib.animation as animation
from matplotlib.animation import ArtistAnimation
import numpy as np
import matplotlib.pyplot as plt
import pylab


def graph(mass_of_Vxk, mass_of_nonpetr_i, mass_of_r, mass_of_t, mass_of_nonpetr_u, mass_of_psi, mass_of_psi_m):
	'''
	Графики параметров невозмущенного перелёта
	'''
	plt.figure(figsize=(16,9))
	fig = pylab.gcf()
	fig.canvas.set_window_title('Графики')

	pylab.subplot (2,3,1)
	pylab.title("Зависимость наклонения орбиты от \n текущей характеристической скорости")
	pylab.plot(mass_of_Vxk,mass_of_nonpetr_i, "b")
	plt.grid()
	plt.xlabel("Характеристическая скорость Vxk,м/c")            
	plt.ylabel("Наклонение i,рад")  
	

	pylab.subplot (2,3,2)
	pylab.title("Зависимость радиуса орбиты от \n текущей характеристической скорости")
	pylab.plot(mass_of_Vxk,mass_of_r, "r")
	plt.grid()
	plt.xlabel("Характеристическая скорость Vxk,м/c")            
	plt.ylabel("Радиус r,км")  

	pylab.subplot (2,3,3)
	pylab.title("Измениние радиуса орбиты во времени")            
	pylab.plot(mass_of_t,mass_of_r)
	plt.grid() 
	plt.xlabel("Время t,c")            
	plt.ylabel("Радиус r,км") 

	pylab.subplot (2,3,4)
	pylab.title("Изменения программного угла \nот аргумента широты ")
	pylab.plot(mass_of_nonpetr_u,mass_of_psi, "r")
	plt.grid()
	plt.xlabel("Широта u,рад")            
	plt.ylabel("Програмный угол psi,рад")  
	
	pylab.subplot (2,3,5)
	pylab.title("Изменения амплитуды программного угла \nот времени ")
	pylab.plot(mass_of_t,mass_of_psi_m, "r")
	plt.grid()
	plt.xlabel("Время t,c")            
	plt.ylabel("Програмный угол psi,рад")  
	
	pylab.subplot (2,3,6)
	pylab.title("Изменения аргумента широты от \n текущей характеристической скорости")
	pylab.plot(mass_of_Vxk,mass_of_nonpetr_u, "r")
	plt.grid()
	plt.xlabel("Характеристическая скорость Vxk,м/c")            
	plt.ylabel("Широта u,рад")  

	plt.subplots_adjust(wspace=0.4, hspace=0.4)
	pylab.show()                          # Включаю отображение

def Pgraph(mass_of_r, mass_of_rP, mass_of_t, mass_of_nonpetr_i, mass_of_petr_i):
	'''
	Графики параметров невозмущенного и возмущенного перелёта
	'''
	plt.figure(figsize=(16,9))
	fig = pylab.gcf()
	fig.canvas.set_window_title('Графики')

	pylab.subplot (1,2,1)
	pylab.title("Изменение радиуса орбиты во времени")
	pylab.plot(mass_of_t,mass_of_r, "b", label = 'Невозмущенное движение')
	pylab.plot(mass_of_t,mass_of_rP, "r", label = 'Возмущенное движение')
	pylab.legend()
	plt.grid()
	plt.xlabel("Время,c")            
	plt.ylabel("Радиус r,км")  
	

	pylab.subplot (1,2,2)
	pylab.title("Изменение наклонения орбиты во времени")
	pylab.plot(mass_of_t,mass_of_nonpetr_i, "b", label = 'Невозмущенное движение')
	pylab.plot(mass_of_t,mass_of_petr_i, "r", label = 'Возмущенное движение')
	pylab.legend()
	plt.grid()
	plt.xlabel("Время t, c")            
	plt.ylabel("Наклонение i, рад")  

	plt.subplots_adjust(wspace=0.4, hspace=0.4)
	pylab.show() 

def TSWgraph(mass_of_t, mass_of_TP, mass_of_T, mass_of_SP, mass_of_S, mass_of_WP, mass_of_W):
	'''
	Графики орбитальых компанент ускорений
	'''
	plt.figure(figsize=(16,9))
	fig = pylab.gcf()
	fig.canvas.set_window_title('Графики')

	pylab.subplot (1,3,1)
	pylab.title("Изменение T состовляющей")
	pylab.plot(mass_of_t,mass_of_TP, "r", label = 'Возмущенное движение')
	pylab.plot(mass_of_t,mass_of_T, "b--", label = 'Невозмущенное движение')
	pylab.legend()
	plt.grid()
	plt.xlabel("Время,c")            
	plt.ylabel("T,м/с^2")  
	
	pylab.subplot (1,3,2)
	pylab.title("Изменение S состовляющей")
	pylab.plot(mass_of_t,mass_of_SP, "r", label = 'Возмущенное движение')
	pylab.plot(mass_of_t,mass_of_S, "b--", label = 'Невозмущенное движение')
	pylab.legend()
	plt.grid()
	plt.xlabel("Время,c")            
	plt.ylabel("S,м/с^2")  
	
	pylab.subplot (1,3,3)
	pylab.title("Изменение W состовляющей")
	pylab.plot(mass_of_t,mass_of_WP, "r", label = 'Возмущенное движение')
	pylab.plot(mass_of_t,mass_of_W, "b--", label = 'Невозмущенное движение')
	pylab.legend()
	plt.grid()
	plt.xlabel("Время,c")            
	plt.ylabel("W,м/с^2")  
	
	plt.subplots_adjust(wspace=0.4, hspace=0.4)
	pylab.show() 

def accel_graph(mass_of_t, mass_of_T_accel, mass_of_S_accel, mass_of_W_accel, mass_of_TSW_accel):
	'''
	Графики орбитальных компанент возмущаюших ускорений
	'''
	plt.figure(figsize=(16,9))
	fig = pylab.gcf()
	fig.canvas.set_window_title('Графики')

	pylab.subplot (2,3,1)
	pylab.title("Изменение T состовляющей")
	pylab.plot(mass_of_t,mass_of_T_accel, "r", label = 'Возмущенное движение')
	plt.grid()
	plt.xlabel("Время,c")            
	plt.ylabel("T,м/с^2")  
	
	pylab.subplot (2,3,2)
	pylab.title("Изменение S состовляющей")
	pylab.plot(mass_of_t,mass_of_S_accel, "r", label = 'Возмущенное движение')
	pylab.legend()
	plt.grid()
	plt.xlabel("Время,c")            
	plt.ylabel("S,м/с^2")  
	
	pylab.subplot (2,3,3)
	pylab.title("Изменение W состовляющей")
	pylab.plot(mass_of_t,mass_of_W_accel, "r", label = 'Возмущенное движение')
	pylab.legend()
	plt.grid()
	plt.xlabel("Время,c")            
	plt.ylabel("W,м/с^2") 

	pylab.subplot (2,1,2)
	pylab.title("Изменение полного ускорения")
	pylab.plot(mass_of_t,mass_of_TSW_accel, "r", label = 'Возмущенное движение')
	pylab.legend()
	plt.grid()
	plt.xlabel("Время,c")            
	plt.ylabel("W,м/с^2") 

	plt.subplots_adjust(wspace=0.4, hspace=0.4)
	pylab.show() 

def orbit_a(mass_of_x_ka, mass_of_y_ka, mass_of_h, mass_of_t):
	'''
	Построение перлёта в плоскости экваотра
	'''
	def moment_plot(event):
		ax.plot(mass_of_x_ka, mass_of_y_ka,lw=0.2, color = "black")
	fig, ax = plt.subplots(figsize = (8, 8))
	ax.set(xlim = (-45157000, 45157000), ylim = (-45157000, 45157000), title = 'Построение перелёта',  xlabel= 'Координата x_ka, м', ylabel = 'Координата y_ka, м')
	ax.grid(True, which='both')
	img = plt.imread('images/pol.png')
	ax.imshow(img, extent=[-6371000,6371000,-6371000,6371000])
	line, = ax.plot([], [], color = "black", lw=0.2)
	sc_3 = ax.scatter([], [], color = "crimson", s = 20, edgecolor = "w")
	height_1 = ax.text(39157000, 42157000, "", bbox={'facecolor':'w', 'alpha':0.5, 'pad':5}, ha="center")
	time_1 = ax.text(39157000, 38157000, "", bbox={'facecolor':'w', 'alpha':0.5, 'pad':5}, ha="center")
	def animate(i):
		if i >= 0:
			line.set_data(mass_of_x_ka[:i + 1], mass_of_y_ka[:i + 1])
			sc_3.set_offsets([mass_of_x_ka[i], mass_of_y_ka[i]])
			height_1.set_text(round(mass_of_h[i],1))
			time_1.set_text(round(mass_of_t[i] / 86400,1))
		return time_1,height_1, line, sc_3,
	ani = animation.FuncAnimation(fig = fig, func = animate, frames = len(mass_of_x_ka)-1, interval = 0.1,  blit = True, repeat = False)
	axes_button_add = pylab.axes([0.7, 0.035, 0.25, 0.04])
	button_add = pylab.Button(axes_button_add, 'Показать перелёт')
	button_add.on_clicked(moment_plot)
	plt.show()
	


def orbit_m(mass_of_y_ka, mass_of_z_ka, mass_of_h, mass_of_t):
	'''
	Построение перлёта в плоскости мередиана  
	'''
	def moment_plot_1(event):
		ax.plot(mass_of_y_ka, mass_of_z_ka,lw=0.2, color = "black")
	fig, ax = plt.subplots(figsize = (8, 8))
	ax.set(xlim = (-45157000, 45157000), ylim = (-45157000, 45157000), title = 'Построение перелёта', xlabel= 'Координата y_ka, м', ylabel = 'Координата z_ka, м')
	ax.grid(True, which='both')
	img = plt.imread('images/ear.png')
	ax.imshow(img, extent=[-6371000,6371000,-6371000,6371000])
	line, = ax.plot([], [], color = "black", zorder = 4, lw=0.2)
	sc_3 = ax.scatter([], [], color = "crimson", zorder = 4, s = 20, edgecolor = "w")
	height_1 = ax.text(39157000, 42157000, "", bbox={'facecolor':'w', 'alpha':0.5, 'pad':5}, ha="center")
	time_1 = ax.text(39157000, 38157000, "", bbox={'facecolor':'w', 'alpha':0.5, 'pad':5}, ha="center")
	def animate(i):
		if i >= 0:
			line.set_data(mass_of_y_ka[:i + 1], mass_of_z_ka[:i + 1])
			sc_3.set_offsets([mass_of_y_ka[i], mass_of_z_ka[i]])
			height_1.set_text(round(mass_of_h[i],1))
			time_1.set_text(round(mass_of_t[i] / 86400,1))
		return time_1,height_1,line, sc_3,
	ani = animation.FuncAnimation(fig = fig, func = animate, frames = len(mass_of_y_ka)-1, interval = 0.01,  blit = True, repeat = False)
	axes_button_add_1 = pylab.axes([0.7, 0.035, 0.25, 0.04])
	button_add_1 = pylab.Button(axes_button_add_1, 'Показать перелёт')
	button_add_1.on_clicked(moment_plot_1)
	plt.show()

def orbit_3d(mass_of_x_ka, mass_of_y_ka,mass_of_z_ka):
	'''
	Построение перлёта в 3D  
	'''
	def moment_plot_3d(event):
		ax_3d.plot(mass_of_x_ka, mass_of_y_ka,mass_of_z_ka, lw=0.2, color = "black")
	fig = plt.figure(figsize=(8,8))
	ax_3d = fig.add_subplot(projection='3d')
	ax_3d.set(xlim = (-45157000, 45157000), ylim = (-45157000, 45157000), zlim = (-45157000, 45157000), title = 'Построение перелёта', xlabel= 'Координата x_ka, м', ylabel = 'Координата y_ka, м',  zlabel = 'Координата z_ka, м', )
	frames = []
	u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:25j]
	rxe = 6371000 * np.cos(u)*np.sin(v)
	rye = 6371000 * np.sin(u)*np.sin(v)
	rze = 6371000 * np.cos(v)
	ax_3d.plot_surface(rxe, rye, rze, cmap='winter')
	for i in range(0,(len(mass_of_x_ka)-1) // 10):
		line = ax_3d.plot(mass_of_x_ka[:(i+1)*10],mass_of_y_ka[:(i+1)*10],mass_of_z_ka[:(i+1)*10],color= "black",lw=0.2)
		frames.append(line)
	ani = ArtistAnimation(fig,frames, interval = 0.1, blit = True, repeat = False)
	axes_button_add_3d = pylab.axes([0.7, 0.035, 0.25, 0.04])
	button_add_3d = pylab.Button(axes_button_add_3d, 'Показать перелёт')
	button_add_3d.on_clicked(moment_plot_3d)
	plt.show()