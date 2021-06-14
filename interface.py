from tkinter import *
from tkinter.ttk import *
import sqlite3 as sql

window = Tk()

mainmenu = Menu(window)
window.config(menu=mainmenu)

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

filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть...")
filemenu.add_command(label="Сохранить...")

filegraph = Menu(mainmenu, tearoff=0)
filegraph.add_command(label="Графики параметров невозмущенного перелта")
filegraph.add_command(label="Графики орбитальных компанент ускорений TSW")
filegraph.add_command(label="Графики орбитальных компанент возмущаюших ускорений TSW")
filegraph.add_command(label="Графики параметров невозмущенного и возмущенного перёлта")

filesimul = Menu(mainmenu, tearoff=0)
filesimul.add_command(label="Построение перелёта в плоскости экватора")
filesimul.add_command(label="Построение перелёта в плоскости мередиана")
filesimul.add_separator()
filesimul.add_command(label="3D")

mainmenu.add_cascade(label='Файл',menu=filemenu)
mainmenu.add_cascade(label='Графики',menu=filegraph)
mainmenu.add_cascade(label='Симуляция',menu=filesimul)
mainmenu.add_command(label='О программе')

area_main = Notebook(window)
calcul_1 = Frame(area_main)
calcul_2 = Frame(area_main)
calcul_3 = Frame(area_main)
area_main.add(calcul_1, text ='Расчёт 1')
area_main.add(calcul_2, text ='Расчёт 2')
area_main.add(calcul_3, text ='Расчёт 3')
area_1 = Notebook(calcul_1)
compute = Frame(area_1)
result_note = Frame(area_1)
area_1.add(compute, text ='Ввод даных')
area_1.add(result_note, text ='Результат')
area_main.pack(expand = 1,anchor=NW, fill = BOTH)
area_1.pack(expand = 1,anchor=NW, fill = BOTH)

frame_start = LabelFrame(compute,text="Введите время начала перелёта")

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
btn_ENG = Button(frame_title, text="Добавить \nдвигатель")
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

# combo_ENG.bind("<<ComboboxSelected>>",  engine_prpoerty)

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
img_normal_max = PhotoImage(file = 'images/Max.png')
img_normal_min = PhotoImage(file = 'images/Min.png') 
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

btn_CALCUL = Button(compute, text="Расчёт")

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


canvas_sheep = Canvas(frame_sheep, height=10, width=10)
img_sheep = PhotoImage(file = 'images/2.png') 
sheep_label = Label(frame_sheep, image=img_sheep)
sheep_label.place(relx=0, rely=0)
canvas_sheep.grid()

frame_powerplant = LabelFrame(result_note,text="Параметры двигательной установки")

canvas_eng = Canvas(frame_powerplant, height=16, width=150)
img_eng = PhotoImage(file = 'images/3.png') 
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
img_travel = PhotoImage(file = 'images/4.png') 
travel_label = Label(frame_travel, image=img_travel)
travel_label.place(relx=0.0, rely=0.05)
canvas_eng.grid()

window.title('Моделирование движения космического буксира')
window.iconbitmap('images/s.ico')
window.config(bg="white")

frame_start.place(x=15, y=5, width=317, height = 40)

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

window.geometry('700x480+0+0')
window.resizable(width=False, height=False)
window.mainloop()