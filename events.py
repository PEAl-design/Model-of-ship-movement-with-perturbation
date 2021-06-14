# Сторонние импорты
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, filedialog
import objects
import graphics
import pickle
import sqlite3 as sql
# Локальные импорты

dict_of_calcul = {}
current_frame = ''


def b_create_new_calcul():

	dialog = Toplevel()
	dialog.title('Создать')
	dialog.geometry('215x80')
	dialog.resizable(False, False)
	lable = Label(dialog, text="Название: ").grid(row=0, column=0,pady=10, padx=5)
	entry = Entry(dialog, text='Создать')
	entry.delete(0, 'end')
	entry.insert(0, 'Расчёт')
	entry.grid(row=0, column=1,pady=10,padx=5)
	func = lambda entry = entry, dialog = dialog: create_new_calcul(entry, dialog)
	Button(dialog, text='Ок', command = func).grid(row=1, column=0, columnspan=2, sticky= W+E,pady=5, padx=10)

def create_new_calcul(entry, dialog):
	name = entry.get()
	if name not in dict_of_calcul:
		cal = objects.Calcul(name)
		dict_of_calcul[name] = cal
	else:
		messagebox.showerror( title="Ошибка", message="Такое имя уже существует")
	dialog.destroy()

def engine_prpoerty(event, obj):
	obj.txt_SpeedU.delete(0, 'end')
	obj.txt_Thrust.delete(0, 'end')	
	obj.txt_Power.delete(0, 'end')
	Name = event.widget.get()
	conn = sql.connect('Engine.db')
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM Engine")
	mass_of_eng = cursor.fetchall()
	conn.commit()
	conn.close()
	for num in mass_of_eng:
		if Name in num:
			obj.txt_SpeedU.insert(0,num[2])
			obj.txt_Thrust.insert(0,num[3])
			obj.txt_Power.insert(0,num[4])

def calcul(name):
	obj = dict_of_calcul[name]
	obj.calculate()

def current(event, note):
	# Меняем текущий фрейм
	tab_id = note.select()
	tab_name = note.tab(tab_id, "text")
	global current_frame
	current_frame = tab_name

	try:
		# Получаем новый объект калкул
		obj = dict_of_calcul[current_frame]
		obj.check_rules()
	except Exception as e:
		print(e)

def b_plot_nonpert():
	result = dict_of_calcul[current_frame].transit_data.result
	graphics.graph(result['V_xk'], result['i'], result['r'], result['t'], result['u'], result['psi'], result['psi_m'])

def b_plot_pert():
	result = dict_of_calcul[current_frame].transit_data.result
	graphics.Pgraph(result['r'], result['r_pert'], result['t'], result['i'], result['i_pert'])

def b_plot_TSW():
	result = dict_of_calcul[current_frame].transit_data.result
	graphics.TSWgraph(result['t'], result['TP'], result['T'], result['SP'], result['S'], result['WP'], result['W'])

def b_plot_TSW_accel():
	result = dict_of_calcul[current_frame].transit_data.result
	graphics.accel_graph(result['t'], result['T_accel'], result['S_accel'], result['W_accel'], result['TSW_accel'])

def b_sum_2d_eq():
	result = dict_of_calcul[current_frame].transit_data.result
	graphics.orbit_a(result['x_ka'], result['y_ka'], result['h_orbit'], result['t'])

def b_sum_2d_mer():
	result = dict_of_calcul[current_frame].transit_data.result
	graphics.orbit_m(result['y_ka'], result['z_ka'], result['h_orbit'], result['t'])

def b_sum_3d():
	result = dict_of_calcul[current_frame].transit_data.result
	graphics.orbit_3d(result['x_ka'], result['y_ka'], result['z_ka'])

def save_to_file():
	try:
		obj = dict_of_calcul[current_frame].transit_data
		name = filedialog.asksaveasfilename(filetypes = [('Расчёт межорбитального перелёта','*.transit')],initialfile = current_frame)
		with open((name + '.transit'), 'wb') as f:
			pickle.dump(obj, f)
	except Exception as e:
		print(e)

def open_file():
	try:
		file_name = filedialog.askopenfilename(filetypes = [('Расчёт межорбитального перелёта','*.transit')])
		with open(file_name, 'rb') as f:
			transit = pickle.load(f)
		file_name = file_name.split('/')[-1]
		obj = objects.Calcul(file_name)
		obj.download_calculate(transit)
		obj.check_rules()
		dict_of_calcul[file_name] = obj
	except Exception as e:
		print(e)

def about():
	messagebox.showinfo("О программе",'''
Эта программа создана в рамках выпускной квалификационной работы
по напаравлению
'Ракетные комплексы и космонавтика'
студентом
Пашковским Евгением Александровичем (gek123456789@yandex.ru)
Под руководством 
Четверикова Алексея Сергеевича
Консультант
Мазуренко Александр Артёмович
		''')