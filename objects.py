from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image
import sqlite3 as sql
from pprint import pprint
from datetime import datetime, timedelta
from tkinter import messagebox

import events
import transit


month = {
	'Январь': 1,
	'Февраль': 2,
	'Март': 3,
	'Апрель':4,
	'Май': 5,
	'Июнь': 6,
	'Июль': 7,
	'Август': 8,
	'Сентябрь': 9,
	'Октябрь': 10,
	'Ноябрь': 11,
	'Декабрь': 12
}

window = Tk()
window.title('Моделирование движения космического буксира')
window.iconbitmap('images/s.ico')
window.config(bg="white")

img_sheep = PhotoImage(file = 'images/2.png')
img_eng = PhotoImage(file = 'images/3.png') 
img_travel = PhotoImage(file = 'images/4.png')
img_normal_max = PhotoImage(file = 'images/Max.png')
img_normal_min = PhotoImage(file = 'images/Min.png')

mainmenu = Menu(window)
window.config(menu=mainmenu)

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Создать", command = events.b_create_new_calcul)
filemenu.add_command(label="Открыть", command = events.open_file)
filemenu.add_command(label="Сохранить как...", command = events.save_to_file)

filegraph = Menu(mainmenu, tearoff=0)
filegraph.add_command(label="Графики параметров невозмущенного перелта", command = events.b_plot_nonpert)
filegraph.add_command(label="Графики орбитальных компанент ускорений TSW",command = events.b_plot_TSW)
filegraph.add_command(label="Графики орбитальных компанент возмущаюших ускорений TSW",command = events.b_plot_TSW_accel)
filegraph.add_command(label="Графики параметров невозмущенного и возмущенного перёлта",command = events.b_plot_pert)

filesimul = Menu(mainmenu, tearoff=0)
filesimul.add_command(label="Построение перелёта в плоскости экватора", command = events.b_sum_2d_eq)
filesimul.add_command(label="Построение перелёта в плоскости мередиана", command = events.b_sum_2d_mer)
filesimul.add_separator()
filesimul.add_command(label="3D", command = events.b_sum_3d)

mainmenu.add_cascade(label='Файл',menu=filemenu)
mainmenu.add_cascade(label='Графики',menu=filegraph,state = 'disabled')
mainmenu.add_cascade(label='Симуляция',menu=filesimul,state = 'disabled')
mainmenu.add_command(label='О программе', command = events.about)

area_main = Notebook(window)
area_main.bind("<<NotebookTabChanged>>", lambda e, note = area_main: events.current(e, note))
area_main.pack(expand = 1,anchor=NW, fill = BOTH)

window.geometry('700x480+0+0')
window.resizable(width=False, height=False)


class Calcul():

	def __init__(self, name):

		self.name = name
		
		frame_calcul = Frame(area_main)
		area_main.add(frame_calcul, text = self.name)
		area = Notebook(frame_calcul)

		area.pack(expand = 1, anchor = NW, fill =BOTH)
		compute = Frame(area)
		chk_state_atm = BooleanVar()
		chk_state_slw = BooleanVar()
		chk_state_gre = BooleanVar()
		chk_state_mis = BooleanVar()
		chk_state_atm.set(False)
		chk_state_slw.set(False)
		chk_state_gre.set(False)
		chk_state_mis.set(True)
		var = IntVar()
		var.set(1)
		#Запрет на буквы
		def validate(new_value):
			return (new_value == "" or new_value.isnumeric()) and (len(new_value) < 3)
		vcmd = (window.register(validate),'%P') 

		def max_img():
			sheep_max.configure(image=img_normal_max)
		def min_img():
			sheep_max.configure(image=img_normal_min)

		def new_engine():
			window_NE = Toplevel()
			label_Name_NE = Label(window_NE, text="Название")
			label_SpeedU_NE = Label(window_NE, text="Удельный импульс")
			label_Thrust_NE = Label(window_NE, text="Тяга")
			label_Power_NE = Label(window_NE, text="Потреблемая мощность")
			label_SpeedU_in_NE = Label(window_NE, text="J=")
			label_Thrust_in_NE = Label(window_NE, text="P=")
			label_Power_in_NE = Label(window_NE, text="N=")
			label_SpeedU_um_NE = Label(window_NE, text="м/с")
			label_Thrust_um_NE = Label(window_NE, text="Н")
			label_Power_um_NE = Label(window_NE, text="кВт")
			txt_Name_NE = Entry(window_NE, width=20)
			txt_SpeedU_NE = Entry(window_NE, width=20)
			txt_Thrust_NE = Entry(window_NE, width=20)
			txt_Power_NE = Entry(window_NE, width=20)
			label_Name_NE.grid(column=0, row=0, sticky=N+W)
			label_SpeedU_NE.grid(column=0, row=1, sticky=N+W)
			label_Thrust_NE.grid(column=0, row=2, sticky=N+W)
			label_Power_NE.grid(column=0, row=3, sticky=N+W)
			label_SpeedU_in_NE.grid(column=1, row=1)
			label_Thrust_in_NE.grid(column=1, row=2)
			label_Power_in_NE.grid(column=1, row=3)
			txt_Name_NE.grid(column=2, row=0)
			txt_SpeedU_NE.grid(column=2, row=1)
			txt_Thrust_NE.grid(column=2, row=2)
			txt_Power_NE.grid(column=2, row=3)
			label_SpeedU_um_NE.grid(column=3, row=1)
			label_Thrust_um_NE.grid(column=3, row=2)
			label_Power_um_NE.grid(column=3, row=3)
			window_NE.geometry('320x150+200+200')
			window_NE.title('Добавить новый двигатель')
			window_NE.iconbitmap('images/p.ico')

			def add_eng():
				name_eng = str(txt_Name_NE.get())
				speedU = float(txt_SpeedU_NE.get())
				thrust = float(txt_Thrust_NE.get())
				power = float(txt_Power_NE.get())
				try:
					#Обращаемся к БД
					conn = sql.connect('Engine.db')
					#Создаем курсор для обращению к инфе БД
					cursor = conn.cursor()
					cursor.execute("INSERT INTO Engine (Name, SpeedU, Thrust, Power) VALUES ('{}', {}, {}, {})".format(name_eng,speedU,thrust,power))
					#Cохранить имзенения
					conn.commit()
					cursor.execute("SELECT * FROM Engine")
					mass_of_eng = cursor.fetchall()
					mass_of_name_eng = []
					for engine in mass_of_eng:
						mass_of_name_eng.append(engine[1])
					combo_ENG['values'] = mass_of_name_eng
					#Закрываем базу данных
					conn.close()
					messagebox.showinfo('Уведомление', 'Двигатель добавлен!')
				except Exception as e:
					messagebox.showerror('Ошибка', e)
				window_NE.destroy()

			btn_NE = Button(window_NE, text="Готово",width=44, command = add_eng)
			btn_NE.place(relx=0.0025, rely=0.6)
			window_NE.mainloop()

		result_note = Frame(area, borderwidth= 10)
		area.add(compute, text ='Ввод даных')
		area.add(result_note, text ='Результат')
		area_main.pack(expand = 1,anchor=NW, fill = BOTH)
		area.pack(expand = 1,anchor=NW, fill = BOTH)

		frame_start = LabelFrame(compute,text="Введите время начала перелёта")

		label_bar = Label(compute, text="Нажмите 'Расчёт'")
		label_time_cur = Label(compute, text="Время расчёта: 0:00:00.000000")

		label_data = Label(frame_start, text="Дата")
		label_start_time = Label(frame_start, text="Время")

		txt_start_day = Entry(frame_start, width=2,validate='key', validatecommand=vcmd)
		txt_start_hours = Entry(frame_start, width=2,validate='key', validatecommand=vcmd)
		label_twopoint = Label(frame_start, text=":")
		txt_start_min = Entry(frame_start, width=2,validate='key', validatecommand=vcmd)
		txt_start_year = Entry(frame_start, width=4)
		label_point = Label(frame_start, text=".")
		txt_start_sec = Entry(frame_start, width=2,validate='key', validatecommand=vcmd)
		combo_month = Combobox(frame_start, values=['Январь', 'Февраль', 'Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'],width=10, state="readonly")
		combo_month.current(0)
		# combo_month.bind("<<ComboboxSelected>>",  change_month)
		txt_start_year.insert(0,"2021")
		txt_start_day.insert(0,"1")
		txt_start_hours.insert(0,"12")
		txt_start_min.insert(0,"59")	
		txt_start_sec.insert(0,"59")

		frame_title = LabelFrame(compute, text="Введите данные")

		label_r0 = Label(frame_title, text="Начальный радиус орбиты")
		label_i0 = Label(frame_title, text="Начальное наклонение обиты")
		label_rk = Label(frame_title, text="Конечный радиус орбиты") 	
		label_ik = Label(frame_title, text="Конечное наклонение обиты")
		label_r0_in = Label(frame_title, text="r0=")
		label_i0_in = Label(frame_title, text="i0=")
		label_rk_in = Label(frame_title, text="rk=")
		label_ik_in = Label(frame_title, text="ik=")
		label_r0_um = Label(frame_title, text="км")
		label_i0_um = Label(frame_title, text="град")
		label_rk_um = Label(frame_title, text="км")
		label_ik_um = Label(frame_title, text="град")

		txt_r0 = Entry(frame_title, width=10)	
		txt_i0 = Entry(frame_title, width=10)
		txt_rk = Entry(frame_title, width=10)	
		txt_ik = Entry(frame_title, width=10)

		txt_r0.insert(0,"6771")
		txt_i0.insert(0,"51.6")
		txt_rk.insert(0,"42157")
		txt_ik.insert(0,"0")

		label_SP = Label(frame_title, text="Параметры солнечной панели", relief=RIDGE)
		label_SP_PowerU = Label(frame_title, text="Удельная мощность")
		Label_SP_MassU  = Label(frame_title, text="Удельная масса")
		Label_SP_NesPower =  Label(frame_title, text="Требуемая мощность") 
		label_SP_PowerU_in = Label(frame_title, text="Ns=")
		label_SP_MassU_in  = Label(frame_title, text="ms=")
		Label_SP_NesPower_in = Label(frame_title, text="N0=")
		label_SP_PowerU_um = Label(frame_title, text="Вт/м2")
		label_SP_MassU_um  = Label(frame_title, text="кг/м2")
		label_SP_NesPower_um = Label(frame_title, text="кВт")

		txt_SP_PowerU = Entry(frame_title, width=10)
		txt_SP_MassU = Entry(frame_title, width=10,validate='key')
		txt_SP_NesPower = Entry(frame_title, width=10)

		txt_SP_PowerU.insert(0,"310")
		txt_SP_MassU.insert(0,"1.6")
		txt_SP_NesPower.insert(0,"400")

		label_ENG = Label(frame_title, text="Выберите двигатель", relief=RIDGE)
		btn_ENG = Button(frame_title, text="Добавить \nдвигатель", command = new_engine)
		combo_ENG = Combobox(frame_title, width=24)

		#Обращаемся к БД
		conn = sql.connect('Engine.db')
		#Создаем курсор для обращению к инфе БД
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM Engine")
		mass_of_eng  = cursor.fetchall()
		mass_of_name_eng = []
		mass_of_properties_ENG = []
		for engine in mass_of_eng:
			mass_of_name_eng.append(engine[1])
			mass_of_properties_ENG.append(engine[2])
			mass_of_properties_ENG.append(engine[3])
			mass_of_properties_ENG.append(engine[4])
		combo_ENG['values'] = mass_of_name_eng
		#Cохранить имзенения
		conn.commit()
		#Закрываем базу данных
		conn.close()

		combo_ENG.bind("<<ComboboxSelected>>",lambda event, obj = self: events.engine_prpoerty(event, obj))

		label_SpeedU = Label(frame_title, text="Удельный импульс")
		label_Thrust = Label(frame_title, text="Тяга")
		label_Power  = Label(frame_title, text="Потреблемая мощность")
		label_SpeedU_in = Label(frame_title, text="J=")
		label_Thrust_in = Label(frame_title, text="P=")
		label_Power_in  = Label(frame_title, text="N=")
		label_SpeedU_um = Label(frame_title, text="м/с")
		label_Thrust_um = Label(frame_title, text="Н")
		label_Power_um  = Label(frame_title, text="кВт")

		txt_SpeedU = Entry(frame_title, width=10)
		txt_Thrust = Entry(frame_title, width=10)	
		txt_Power  = Entry(frame_title, width=10)

		spd140 = 3

		combo_ENG.current(spd140)
		txt_SpeedU.insert(0,mass_of_properties_ENG[0+3 * spd140])
		txt_Thrust.insert(0,mass_of_properties_ENG[1+3 * spd140])	
		txt_Power.insert(0,mass_of_properties_ENG[2+3 * spd140])

		label_step = Label(frame_title, text="Шаг интегрирования")	
		label_step_in = Label(frame_title, text="h=")
		txt_step = Entry(frame_title, width=10)
		txt_step.insert(0,"10000")

		frame_perturbations = LabelFrame(compute,text="Выберите действующие возмущения")
		chk_atm = Checkbutton(frame_perturbations, text='Возмущения вызваные атмосферой', var=chk_state_atm)
		chk_slw = Checkbutton(frame_perturbations, text='Возмущения вызваные солнечным ветром', var=chk_state_slw)
		chk_gre = Checkbutton(frame_perturbations, text='Возмущения вызваные нецентральностью \nгравитациионого поля Земли', var=chk_state_gre)
		chk_mis = Checkbutton(frame_perturbations, text='Учёт ошибки в определении вектора тяги', var=chk_state_mis)

		frame_params = LabelFrame(compute,text="Укажите параметры буксира",width=300, height=300)

		radio_btn_normal = Radiobutton(frame_params, text = 'Нормаль по потоку', variable = var, value = 0,command = max_img)
		radio_btn_edgr = Radiobutton(frame_params,text = 'Нормаль \nперпендикулярна потоку', variable = var, value = 1, command = min_img)
		canvas_max = Canvas(frame_params, height=8, width=8)
		global img_normal_min, img_normal_max
		sheep_max = Label(frame_params, image=img_normal_min)
		sheep_max.place(x=180, y=5)
		canvas_max.grid()
		label_mass = Label(frame_params, text="Масса буксира")
		label_alph_k = Label(frame_params, text="Контсруктивный \nкоэффициент",justify=LEFT)
		label_gamma = Label(frame_params, text="Удельная масса ДУ")
		label_Kspx = Label(frame_params, text="Баковый коэффициент")

		label_mass_in = Label(frame_params, text="M0=")
		label_alpha_k_in = Label(frame_params, text="alpha_k=")
		label_gamma_in = Label(frame_params, text="gamma=")
		label_Kspx_in = Label(frame_params, text="k=")
		label_mass_um = Label(frame_params, text="кг")
		label_gamma_um = Label(frame_params, text="кг/Н")
		txt_mass = Entry(frame_params,width=10)
		txt_alpha_k = Entry(frame_params,width=10)
		txt_gamma = Entry(frame_params, width=10)
		txt_Kspx = Entry(frame_params, width=10)
		txt_mass.insert(0,32500)
		txt_alpha_k.insert(0,0.1)
		txt_gamma.insert(0,40)
		txt_Kspx.insert(0,0.07)

		func = lambda name = self.name: events.calcul(name)
		btn_CALCUL = Button(compute, text="Расчёт", command = func)

		# ____________________________________________________________________

		frame_sheep = LabelFrame(result_note,text="Параметры буксира")

		label_SP_area = Label(frame_sheep, text="Общая площадь \nсолнечных батарей", justify=LEFT)
		label_SP_mass = Label(frame_sheep, text="Общая масса \nсолнечных батарей", justify=LEFT)
		label_BalKOf = Label(frame_sheep, text="Баллистический \nкоффициент", justify=LEFT)
		label_PN = Label(frame_sheep, text="Масса полезной \nнагрзки", justify=LEFT)

		label_SP_area_in = Label(frame_sheep, text="S=")
		label_SP_mass_in = Label(frame_sheep, text="Msp=")
		label_BalKOf_in = Label(frame_sheep, text="Ф=")
		label_PN_in = Label(frame_sheep, text="Mпн=")

		label_SP_area_um = Label(frame_sheep, text="м2")
		label_SP_mass_um = Label(frame_sheep, text="кг")
		label_BalKOf_um = Label(frame_sheep, text="м2/кг")
		label_PN_um = Label(frame_sheep, text="кг")

		txt_SP_area = Entry(frame_sheep, width=10)
		txt_SP_mass = Entry(frame_sheep, width=10)
		txt_BalKOf = Entry(frame_sheep, width=10)
		txt_PN = Entry(frame_sheep, width=10)
		global img_sheep
		canvas_sheep = Canvas(frame_sheep, height=10, width=10)
		sheep_label = Label(frame_sheep, image=img_sheep)
		sheep_label.place(relx=0, rely=0)
		canvas_sheep.grid()

		frame_powerplant = LabelFrame(result_note,text="Параметры двигательной установки")
		global img_eng
		canvas_eng = Canvas(frame_powerplant, height=16, width=150)
		eng_label = Label(frame_powerplant, image=img_eng)
		eng_label.place(relx=0.15, rely=0)
		canvas_eng.grid()

		label_numbeng = Label(frame_powerplant, text="Количество \nдвигталей")
		label_NumThrust = Label(frame_powerplant, text="Тяга")
		label_NumPower = Label(frame_powerplant, text="Потребляемая \nмощность")
		label_fuel = Label(frame_powerplant, text="Масса \nрабочего тела \nна перелёт", justify=LEFT)
		label_numbeng_in = Label(frame_powerplant, text="n=")
		label_NumThrust_in = Label(frame_powerplant, text="Pду=")
		label_NumPower_in  = Label(frame_powerplant, text="Nду=")
		label_fuel_in  = Label(frame_powerplant, text="Mт=")
		label_NumThrust_um = Label(frame_powerplant, text="Н")
		label_NumPower_um = Label(frame_powerplant, text="кВт")
		label_fuel_um =  Label(frame_powerplant, text="кг")

		txt_numbeng = Entry(frame_powerplant, width=10)
		txt_NumThrust = Entry(frame_powerplant, width=10)
		txt_NumPower = Entry(frame_powerplant, width=10)
		txt_fuel = Entry(frame_powerplant, width=10)

		frame_travel = LabelFrame(result_note,text="Параметры перелёта")

		label_time = Label(frame_travel, text="Время движение \nбуксира")
		label_Vch = Label(frame_travel, text="Характерестическая \nскорость на перелёт", justify=LEFT)
		label_num_cr = Label(frame_travel, text="Количество оборотов", justify=LEFT)
		label_time_in = Label(frame_travel, text="T=")
		label_Vch_in = Label(frame_travel, text="Vх=")
		label_time_s_um = Label(frame_travel, text="c")
		label_time_day_um = Label(frame_travel, text="сут")
		label_Vch_um = Label(frame_travel, text="м/с")

		txt_time_s = Entry(frame_travel, width=10)
		txt_time_day = Entry(frame_travel, width=10)
		txt_Vch = Entry(frame_travel, width=10)
		txt_num_cr = Entry(frame_travel, width=10)

		canvas_travel = Canvas(frame_travel, height=16, width=16)
		global img_travel
		travel_label = Label(frame_travel, image=img_travel)
		travel_label.place(relx=0.0, rely=0.05)
		canvas_eng.grid()


		frame_start.place(x=15, y=5, width=317, height = 40)
		
		label_bar.place(x=15, y=400)
		label_time_cur.place(x=169, y=400)

		label_data.grid(column=0, row=0, sticky=N+W)

		txt_start_day.grid(column=1, row=0, sticky=N+W)
		combo_month.grid(column=2, row=0, sticky=N+W)
		txt_start_year.grid(column=3, row=0, sticky=N+W)
		label_start_time.grid(column=4, row=0, sticky=N+W)	
		txt_start_hours.grid(column=5, row=0, sticky=N+W)
		label_twopoint.grid(column=6, row=0, sticky=N+W)
		txt_start_min.grid(column=7, row=0, sticky=N+W)	
		label_point.grid(column=8, row=0, sticky=N+W)
		txt_start_sec.grid(column=9, row=0, sticky=N+W)

		frame_title.place(x=15, y=65, width=317)

		label_r0.grid(column=0, row=0, sticky=N+W)
		label_i0.grid(column=0, row=1, sticky=N+W)
		label_rk.grid(column=0, row=2, sticky=N+W)
		label_ik.grid(column=0, row=3, sticky=N+W)
		label_r0_in.grid(column=1, row=0)
		label_i0_in.grid(column=1, row=1)
		label_rk_in.grid(column=1, row=2)
		label_ik_in.grid(column=1, row=3)
		txt_r0.grid(column=2, row=0)	
		txt_i0.grid(column=2, row=1)
		txt_rk.grid(column=2, row=2)	
		txt_ik.grid(column=2, row=3)
		label_r0_um.grid(column=3, row=0)
		label_i0_um.grid(column=3, row=1)
		label_rk_um.grid(column=3, row=2)
		label_ik_um.grid(column=3, row=3)

		label_SP.grid(column=0, row=4,sticky=N+W)
		label_SP_PowerU.grid(column=0, row=5,sticky=N+W)
		Label_SP_MassU.grid(column=0, row=6,sticky=N+W)
		Label_SP_NesPower.grid(column=0, row=7,sticky=N+W)
		label_SP_PowerU_in.grid(column=1, row=5)
		label_SP_MassU_in.grid(column=1, row=6)
		Label_SP_NesPower_in.grid(column=1,row=7)
		txt_SP_PowerU.grid(column=2, row=5)
		txt_SP_MassU.grid(column=2, row=6)
		txt_SP_NesPower.grid(column=2, row=7)
		label_SP_PowerU_um.grid(column=3, row=5)
		label_SP_MassU_um.grid(column=3, row=6)
		label_SP_NesPower_um.grid(column=3, row=7)

		label_ENG.grid(column=0, row=8,sticky=N+W)
		combo_ENG.grid(column=0, row=9,sticky=W)
		btn_ENG.grid(column=2, row=9, sticky=N+W)
		label_SpeedU.grid(column=0, row=10, sticky=N+W)
		label_Thrust.grid(column=0, row=11, sticky=N+W)
		label_Power.grid(column=0, row=12, sticky=N+W)
		label_SpeedU_in.grid(column=1, row=10)
		label_Thrust_in.grid(column=1, row=11)
		label_Power_in.grid(column=1, row=12)
		txt_SpeedU.grid(column=2, row=10)
		txt_Thrust.grid(column=2, row=11)	
		txt_Power.grid(column=2, row=12)	
		label_SpeedU_um.grid(column=3, row=10)
		label_Thrust_um.grid(column=3, row=11)
		label_Power_um.grid(column=3, row=12)

		label_step.grid(column=0, row=13,sticky=N+W)
		label_step_in.grid(column=1, row=13)
		txt_step.grid(column=2, row=13)

		frame_perturbations.place(x=360, y=250, width=317)

		chk_atm.pack(anchor=NW)
		chk_slw.pack(anchor=NW)
		chk_gre.pack(anchor=NW)
		chk_mis.pack(anchor=NW)

		frame_params.place(x=360, y=5, width=317, height = 240)

		radio_btn_normal.place(x=10, y=3)
		radio_btn_edgr.place(x=10, y=45)

		label_mass.place(x=5, y=100)
		label_alph_k.place(x=5, y=120)
		label_gamma.place(x=5, y=160)
		label_Kspx.place(x=5, y=190)
		label_mass_in.place(x=135, y=100)
		label_alpha_k_in.place(x=115, y=130)
		label_gamma_in.place(x=115, y=160)
		label_Kspx_in.place(x=145, y=190)
		label_mass_um.place(x=245, y=100)
		label_gamma_um.place(x=245, y=160)
		txt_mass.place(x=175, y=100)
		txt_alpha_k.place(x=175, y=130)
		txt_gamma.place(x=175, y=160)
		txt_Kspx.place(x=175, y=190)

		frame_sheep.place(x=5, y=5,width=440, height=200)


		label_SP_area.place(relx=0.4, rely=0)
		label_SP_mass.place(relx=0.4, rely=0.25)
		label_BalKOf.place(relx=0.4, rely=0.5)
		label_PN.place(relx=0.4, rely=0.75)

		label_SP_area_in.place(relx=0.705, rely=0.05)
		label_SP_mass_in.place(relx=0.67, rely=0.25)
		label_BalKOf_in.place(relx=0.70, rely=0.5)
		label_PN_in.place(relx=0.665, rely=0.75)

		label_SP_area_um.place(relx=0.92, rely=0.05)
		label_SP_mass_um.place(relx=0.92, rely=0.25)
		label_BalKOf_um.place(relx=0.92, rely=0.5)
		label_PN_um.place(relx=0.92, rely=0.75)

		txt_SP_area.place(relx=0.76, rely=0.05)
		txt_SP_mass.place(relx=0.76, rely=0.25)
		txt_BalKOf.place(relx=0.76, rely=0.5)
		txt_PN.place(relx=0.76, rely=0.75)


		frame_powerplant.place(x=450, y=30, width=230, height=360)

		label_numbeng.place(relx=0, rely=0.5)
		label_NumThrust.place(relx=0, rely=0.625)
		label_NumPower.place(relx=0, rely=0.725)
		label_fuel.place(relx=0, rely=0.85)
		label_numbeng_in.place(relx=0.5, rely=0.525)
		label_NumThrust_in.place(relx=0.45, rely=0.625)
		label_NumPower_in.place(relx=0.445, rely=0.75)
		label_fuel_in.place(relx=0.45, rely=0.89)
		label_NumThrust_um.place(relx=0.9, rely=0.625)
		label_NumPower_um.place(relx=0.9, rely=0.75)
		label_fuel_um .place(relx=0.9, rely=0.89)

		txt_numbeng.place(relx=0.6, rely=0.525)
		txt_NumThrust.place(relx=0.6, rely=0.625)
		txt_NumPower.place(relx=0.6, rely=0.75)
		txt_fuel.place(relx=0.6, rely=0.89)

		frame_travel.place(x=5, y=210,width=440, height=200)

		label_time.place(relx=0.4, rely=0.05)
		label_Vch.place(relx=0.4, rely=0.375)
		label_num_cr.place(relx=0.4, rely=0.725)
		label_time_in.place(relx=0.70, rely=0.1)
		label_Vch_in.place(relx=0.70, rely=0.425)
		label_time_s_um.place(relx=0.93, rely=0)
		label_time_day_um.place(relx=0.93, rely=0.175)
		label_Vch_um.place(relx=0.93, rely=0.425)

		txt_time_s.place(relx=0.76, rely=0)
		txt_time_day.place(relx=0.76, rely=0.175)
		txt_Vch.place(relx=0.76, rely=0.425)
		txt_num_cr.place(relx=0.76, rely=0.725)

		btn_CALCUL.place(x=360, y=380, width=317, height = 44)

		self.txt_start_day = txt_start_day
		self.combo_month = combo_month
		self.txt_start_year = txt_start_year
		self.txt_start_hours = txt_start_hours
		self.txt_start_min = txt_start_min
		self.txt_start_sec = txt_start_sec
		self.txt_r0 = txt_r0
		self.txt_i0 = txt_i0
		self.txt_rk = txt_rk
		self.txt_ik = txt_ik
		self.txt_SP_PowerU = txt_SP_PowerU
		self.txt_SP_MassU = txt_SP_MassU
		self.txt_SP_NesPower = txt_SP_NesPower
		self.combo_ENG = combo_ENG
		self.txt_SpeedU = txt_SpeedU
		self.txt_Thrust = txt_Thrust
		self.txt_Power = txt_Power
		self.txt_step = txt_step
		self.chk_state_atm = chk_state_atm
		self.chk_state_slw = chk_state_slw
		self.chk_state_gre = chk_state_gre
		self.chk_state_mis = chk_state_mis
		self.var = var
		self.txt_mass = txt_mass
		self.txt_alpha_k = txt_alpha_k
		self.txt_gamma = txt_gamma
		self.txt_Kspx = txt_Kspx
		self.txt_SP_area = txt_SP_area
		self.txt_SP_mass = txt_SP_mass
		self.txt_BalKOf = txt_BalKOf
		self.txt_PN = txt_PN
		self.txt_numbeng = txt_numbeng
		self.txt_NumThrust = txt_NumThrust
		self.txt_NumPower = txt_NumPower
		self.txt_fuel = txt_fuel
		self.txt_time_s = txt_time_s
		self.txt_time_day = txt_time_day
		self.txt_Vch = txt_Vch
		self.txt_num_cr = txt_num_cr
		self.sheep_max = sheep_max
		self.result_frame = result_note
		self.area = area
		self.check_rules()
		self.label_bar = label_bar
		self.label_time_cur = label_time_cur
		window.update()

	def calculate(self):
		self.label_bar.configure(text = "Расчёт...")
		window.update()
		self.txt_SP_area.delete(0, 'end')
		self.txt_SP_mass.delete(0, 'end')
		self.txt_BalKOf.delete(0, 'end')
		self.txt_PN.delete(0, 'end')
		self.txt_numbeng.delete(0, 'end')
		self.txt_NumThrust.delete(0, 'end')
		self.txt_NumPower.delete(0, 'end')
		self.txt_fuel.delete(0, 'end')
		self.txt_time_s.delete(0, 'end')
		self.txt_time_day.delete(0, 'end')
		self.txt_Vch.delete(0, 'end')
		self.txt_num_cr.delete(0, 'end')
		self.transit_data = transit.Transit(
			N_0 = float(self.txt_SP_NesPower.get()),
			N_eng = float(self.txt_Power.get()),
			P_eng = float(self.txt_Thrust.get()),
			r_0 = float(self.txt_r0.get()),
			i_0 = float(self.txt_i0.get()),
			r_k = float(self.txt_rk.get()),
			i_k = float(self.txt_ik.get()),
			M_0 = float(self.txt_mass.get()),
			c_d = float(self.txt_SpeedU.get()),
			N_su = float(self.txt_SP_PowerU.get()),
			M_su = float(self.txt_SP_MassU.get()),
			Alfa_k = float(self.txt_alpha_k.get()),
			Gamma = float(self.txt_gamma.get()),
			K_spx = float(self.txt_Kspx.get()),
			h_step = int(self.txt_step.get()),
			year = float(self.txt_start_year.get()),
			month = float(month[self.combo_month.get()]),
			day = float(self.txt_start_day.get()),
			hour = float(self.txt_start_hours.get()),
			minute = float(self.txt_start_min.get()),
			second = float(self.txt_start_sec.get()),
			ch_rotate = self.var.get(),
			add_atm = self.chk_state_atm.get(),
			add_grav = self.chk_state_gre.get(),
			add_sw = self.chk_state_slw.get(),
			statistic_misstake = self.chk_state_mis.get(),
			name_eng= self.combo_ENG.get()
			)
		self.transit_data.general_calculation()
		# pprint(self.transit_data.result)

		self.txt_SP_area.insert(0, round(self.transit_data.square_sp,2))
		self.txt_SP_mass.insert(0, round(self.transit_data.mass_sp,2))
		self.txt_BalKOf.insert(0, round(self.transit_data.balistik_koef,3))
		self.txt_PN.insert(0, round(self.transit_data.M_pn,2))
		self.txt_numbeng.insert(0, self.transit_data.number_of_engine)
		self.txt_NumThrust.insert(0, round(self.transit_data.P_du,2))
		self.txt_NumPower.insert(0, round(self.transit_data.N_du,2))
		self.txt_fuel.insert(0, round(self.transit_data.M_fuel,2))
		self.txt_time_s.insert(0, round(self.transit_data.t_sec,2))
		self.txt_time_day.insert(0, round(self.transit_data.t_day,2))
		self.txt_Vch.insert(0, round(self.transit_data.V_ch,2))
		self.txt_num_cr.insert(0, round(self.transit_data.num_round,2))
		self.check_rules()
		self.label_bar.configure(text = 'Готово!')
		self.label_time_cur.configure(text = 'Время расчёта: ' + self.transit_data.time_of_compute)
	
	def download_calculate(self, transit):
		self.transit_data = transit

		self.txt_start_day.delete(0, 'end')
		self.txt_start_day.insert(0, int(transit.day))
		self.txt_start_year.delete(0, 'end')
		self.txt_start_year.insert(0, int(transit.year))
		self.txt_start_hours.delete(0, 'end')
		self.txt_start_hours.insert(0, int(transit.hour))
		self.txt_start_min.delete(0, 'end')
		self.txt_start_min.insert(0, int(transit.minute))
		self.txt_start_sec.delete(0, 'end')
		self.txt_start_sec.insert(0, int(transit.second))
		self.txt_r0.delete(0, 'end')
		self.txt_r0.insert(0, transit.r_0/1000)
		self.txt_i0.delete(0, 'end')
		self.txt_i0.insert(0, transit.i_0)
		self.txt_rk.delete(0, 'end')
		self.txt_rk.insert(0, transit.r_k/1000)
		self.txt_ik.delete(0, 'end')
		self.txt_ik.insert(0, transit.i_k)
		self.txt_SP_PowerU.delete(0, 'end')
		self.txt_SP_PowerU.insert(0, transit.N_su)
		self.txt_SP_MassU.delete(0, 'end')
		self.txt_SP_MassU.insert(0, transit.M_su)
		self.txt_SP_NesPower.delete(0, 'end')
		self.txt_SP_NesPower.insert(0, transit.N_0)
		self.txt_SpeedU.delete(0, 'end')
		self.txt_SpeedU.insert(0, transit.c_d)
		self.txt_Thrust.delete(0, 'end')
		self.txt_Thrust.insert(0, transit.P_eng)
		self.txt_Power.delete(0, 'end')
		self.txt_Power.insert(0, transit.N_eng)
		self.txt_step.delete(0, 'end')
		self.txt_step.insert(0, transit.h_step)
		self.txt_mass.delete(0, 'end')
		self.txt_mass.insert(0, transit.M_0)
		self.txt_alpha_k.delete(0, 'end')
		self.txt_alpha_k.insert(0, transit.Alfa_k)
		self.txt_gamma.delete(0, 'end')
		self.txt_gamma.insert(0, transit.Gamma)
		self.txt_Kspx.delete(0, 'end')
		self.txt_Kspx.insert(0, transit.K_spx)
		self.txt_SP_area.delete(0, 'end')
		self.txt_SP_area.insert(0, round(transit.square_sp,2))
		self.txt_SP_mass.delete(0, 'end')
		self.txt_SP_mass.insert(0, round(transit.mass_sp,2))
		self.txt_BalKOf.delete(0, 'end')
		self.txt_BalKOf.insert(0, round(transit.balistik_koef,3))
		self.txt_PN.delete(0, 'end')
		self.txt_PN.insert(0, round(transit.M_pn,2))
		self.txt_numbeng.delete(0, 'end')
		self.txt_numbeng.insert(0, round(transit.number_of_engine,2))
		self.txt_NumThrust.delete(0, 'end')
		self.txt_NumThrust.insert(0, round(transit.P_du,2))
		self.txt_NumPower.delete(0, 'end')
		self.txt_NumPower.insert(0, round(transit.N_du,2))
		self.txt_fuel.delete(0, 'end')
		self.txt_fuel.insert(0, round(transit.M_fuel,2))
		self.txt_time_s.delete(0, 'end')
		self.txt_time_s.insert(0, round(transit.t_sec,2))
		self.txt_time_day.delete(0, 'end')
		self.txt_time_day.insert(0, round(transit.t_day,2))
		self.txt_Vch.delete(0, 'end')
		self.txt_Vch.insert(0, round(transit.V_ch,2))
		self.txt_num_cr.delete(0, 'end')
		self.txt_num_cr.insert(0, round(transit.num_round,2))

		self.combo_ENG.set(transit.name_eng)
		self.combo_month.current(int(transit.month)-1)
		self.chk_state_atm.set(transit.add_atm)
		self.chk_state_slw.set(transit.add_sw)
		self.chk_state_gre.set(transit.add_grav)
		self.chk_state_mis.set(transit.statistic_misstake)

		self.label_bar.configure(text = 'Готово!')
		self.label_time_cur.configure(text = 'Время расчёта: ' + self.transit_data.time_of_compute)

		self.var.set(int(transit.ch_rotate))
		if int(transit.ch_rotate) == 0:
			self.sheep_max.configure(image=img_normal_max)
		else:
			self.sheep_max.configure(image=img_normal_min)


	def check_rules(self):
		if hasattr(self, 'transit_data'):
			self.area.add(self.result_frame)
			mainmenu.entryconfig('Графики',state = 'normal')
			mainmenu.entryconfig('Симуляция',state = 'normal')
		else:
			self.area.hide(1)
			mainmenu.entryconfig('Графики',state = 'disabled')
			mainmenu.entryconfig('Симуляция',state = 'disabled')