import numpy as np
from pprint import pprint
from datetime import datetime


# Гравитационная постоянная
G = 6.67430*10**(-11)
# Угловая скорость вращения Земли
OO = 0.000072921
# Масса планеты
M_planet = 5.97*10**(24)
# Гравитационная постоянная планеты
M_u = M_planet * G
# 
ee = M_u * 6378137 ** (2) * 0.000115519


def find_number_of_engine(N_eng, N_0):
	'''
	Расчёт количества двигателей от проектируемой мощности
	:param N_0: Проектируемая мощность буксира (КВт)
	:param N_eng: Мощность потребляемая одним двигателем (КВт)
	:return number_of_engine: Количество двигателей
	'''
	number_of_engine = int(N_0//N_eng)
	return number_of_engine

def find_general_thrust(number_of_engine, P_eng, statistic_misstake = True):
	'''
	Расчёт общей тяги
	:param number_of_engine: Количество двигателей
	:param P_eng: Тяга одного двигателя (Н)
	:param statistic_misstake: Учёт статистической ошибки
	:return P_du: Общая тяга
	'''
	if statistic_misstake:
		P_du = number_of_engine*P_eng*1.021
	else:
		P_du = number_of_engine*P_eng
	return P_du

def find_general_power(number_of_engine, N_eng):
	'''
	Расчёт общей потребляемой мощность аппарата
	:param number_of_engine: Количество двигателей
	:param N_eng: Мощность потребляемая одним двигателем (КВт)
	:return N_du: Общая мощность
	'''
	N_du = number_of_engine*N_eng*1.05
	return N_du

def find_characteristic_velocity(M_planet, r_0, i_0, r_k, i_k):
	'''
	Расчёт необходимой характерестической скорости для перелёта
	:param M_planet: Масса планеты (кг)
	:param r_0: Начальный радиус орбиты (км)
	:param i_0: Начальное наклонение орбиты (град)
	:param r_k: Конечный радиус орбиты (км)
	:param i_k: Конечное наклонение орбиты (град)
	:return V_ch: Характеристеческая скорость
	'''
	V_ch = (np.sqrt((G * M_planet)/(r_0)) * np.sqrt(1 - 2 * np.sqrt(r_0/r_k) * 
			np.cos(np.pi * ((i_k - i_0) * np.pi / 180)/ 2 ) + r_0/r_k))
	return V_ch

def find_mass_of_fuel(M_0, V_ch, c_d):
	'''Расчёт массы топлива
	:param M_0: Начальная масса аппарата на орбите (кг)
	:param V_ch: Характеристеческая скорость
	:param c_d: Удельный импульс (м/c)
	:return M_fuel: Масса топлива
	'''
	M_fuel = M_0*(1-np.exp(-V_ch/c_d))
	return M_fuel

def find_square_solar_panel(N_0, N_su):
	'''
	Расчёт площади солнечных батарей
	:param N_0: Проектируемая мощность буксира (КВт)
	:param N_su: Удельная мощность солнечных батарей (Вт/м2)
	:return square_sp: Площадь солнечных батарей
	'''
	square_sp = N_0 * 1000 / N_su
	return square_sp

def find_mass_solar_panel(square_sp, M_su):
	'''
	Расчёт массы солнечных панелей
	:param square_sp: Площадь солнечных батарей
	:param M_su: Удельная масса солнечных батарей (Кг/м2)
	:return mass_sp: Масса солнечных батарей
	'''
	mass_sp = Ms = square_sp * float(M_su)
	return mass_sp

def find_mass_pn(M_0, Alfa_k, M_fuel, K_spx, Gamma, P_du, mass_sp):
	'''Расчёт массы полезной нагрузки
	:param M_0: Начальная масса аппарата на орбите (кг)
	:param Alfa_k: Конструктивный коэффициент
	:param M_fuel: Масса топлива
	:param K_spx: Баковый коэффициент (Масса бака относительно массы топлива)
	:param Gamma: Удельная масса двигательной установки (кг/H)
	:param P_du: Общая тяга
	:param mass_sp: Масса солнечных батарей
	:return M_pn: Масса полезной нагрузки
	'''
	M_pn = M_0 * (1-Alfa_k)-M_fuel*(1+K_spx)-Gamma*P_du-mass_sp
	return M_pn

def find_time_transit(M_fuel, c_d, P_du):
	'''Расчёт времени перелёта
	:param M_fuel: Масса топлива
	:param c_d: Удельный импульс (м/c)
	:param P_du: Общая тяга
	:return t_sec: Время перелёта (секунды)
	:return t_day: Время перелёта (дни)
	'''
	t_sec = M_fuel * c_d / P_du
	t_day = t_sec/86400
	return t_sec, t_day

def find_balistik_koef(square_sp, M_0, ch_rotate):
	'''Расчёт балистического коэффициента
	:param square_sp: Площадь солнечных батарей
	:param M_0: Начальная масса аппарата на орбите (кг)
	:return balistik_koef: Балистический коэффициент
	'''
	if ch_rotate == True:
		balistik_koef = 2.15*60/(2*M_0)
	else:
		balistik_koef = 2.15*square_sp/(2*M_0)
	return balistik_koef

def find_beg_acceleration(P_du, M_0):
	'''Начальное ускорение
	:param P_du: Общая тяга
	:param M_0: Начальная масса аппарата на орбите (кг)
	:return a_0: Начальное ускорение
	'''
	a_0 = P_du / M_0
	return a_0

class Transit(object):
	"""Параметры перелёта космического аппарата с орбиты на орбиту и его характеристики"""
	
	def __init__(self, N_0 = None, N_eng = None, P_eng = None, r_0 = None, i_0 = None,
				r_k = None, i_k = None, M_0 = None, c_d = None, N_su = None, M_su = None, Alfa_k = None,
				Gamma = None, K_spx = None, h_step = None, year = None, month = None, day = None, hour = None,
				 minute = None, second = None, ch_rotate = False, add_atm = False, add_sw = False, add_grav = False, 
				 statistic_misstake = True, name_eng = None):
		'''Коструктор Transit
		:param N_0: Проектируемая мощность буксира (КВт)
		:param N_eng: Мощность потребляемая одним двигателем (КВт)
		:param P_eng: Тяга одного двигателя (Н)
		:param M_planet: Масса планеты (кг)
		:param r_0: Начальный радиус орбиты (км)
		:param i_0: Начальное наклонение орбиты (град)
		:param r_k: Конечный радиус орбиты (км)
		:param i_k: Конечное наклонение орбиты (град)
		:param M_0: Начальная масса аппарата на орбите (кг)
		:param c_d: Удельный импульс (м/c)
		:param N_su: Удельная мощность солнечных батарей (Вт/м2)
		:param M_su: Удельная масса солнечных батарей (Кг/м2)
		:param Alfa_k: Конструктивный коэффициент
		:param Gamma: Удельная масса двигательной установки (кг/H)
		:param K_spx: Баковый коэффициент (Масса бака относительно массы топлива)
		:param h_step: Шаг интегрирования
		:param year: Год (2000 - ...)
		:param month: Месяц (1-12)
		:param day: День
		:param hour: час (0-23)
		:param minute: минуты (0-59)
		:param second: секунды (0-59)
		:param ch_rotate: Положение буксира по потоку True - нормаль по потоку/False - перпендикулярно потоку
		:param add_atm: Учёт атмосферы True/False
		:param add_sw: Учёт солнечного ветра True/False
		:param add_grav: Учёт гравитации True/False
		'''
		self.N_0 = N_0
		self.N_eng = N_eng
		self.P_eng = P_eng
		self.M_planet = M_planet
		self.r_0 = r_0*1000
		self.i_0 = i_0
		self.r_k = r_k*1000
		self.i_k = i_k
		self.M_0 = M_0
		self.c_d = c_d
		self.N_su = N_su
		self.M_su = M_su
		self.Alfa_k = Alfa_k
		self.Gamma = Gamma
		self.K_spx = K_spx
		self.h_step = h_step
		self.year = year
		self.month = month
		self.day = day
		self.hour = hour
		self.minute = minute
		self.second = second
		self.ch_rotate = ch_rotate
		self.add_atm = add_atm
		self.add_sw = add_sw
		self.add_grav = add_grav
		self.statistic_misstake = statistic_misstake
		self.name_eng = name_eng


	def runge_kut(self, mass_f, n, h, mass_of_x, t1, T):
		result_massive = []
		result_massive.append([*mass_of_x])
		while t1 < T:
			K1 = []
			K2 = []
			K3 = []
			K4 = []
			S1 = []
			S2 = []
			S3 = []
			for i in range(0,n):
				K1.append(mass_f[i](t1,mass_of_x))
				S1.append(mass_of_x[i] + 0.5 * h * K1[i])
			for i in range(0,n):
				K2.append(mass_f[i](t1 + h/2, S1))
				S2.append(mass_of_x[i] + 0.5 * h * K2[i])
			for i in range(0,n):
				K3.append(mass_f[i](t1 + h/2, S2))
				S3.append(mass_of_x[i] + h * K3[i])
			for i in range(0,n):
				K4.append(mass_f[i](t1 + h, S3))
			for i in range(0,n):
				mass_of_x[i] += (h/6) *(K1[i] + 2*K2[i] + 2*K3[i] + K4[i])
			t1 += h
			rez = [*mass_of_x]
			result_massive.append(rez)
		transform_matrix = []
		i = 0
		while i <= len(result_massive[0])-1:
			column = []
			for line in result_massive:
				column.append(line[i])
			transform_matrix.append(column)
			i += 1

		return transform_matrix

	def general_calculation(self):
		'''Общий расчёт параметров выведения космического аппарата'''
		begining_time = datetime.now()
		# Основные параметры
		self.number_of_engine = find_number_of_engine(self.N_eng, self.N_0)
		self.P_du = find_general_thrust(self.number_of_engine, self.P_eng, self.statistic_misstake)
		self.N_du = find_general_power(self.number_of_engine, self.N_eng)
		self.V_ch = find_characteristic_velocity(self.M_planet, self.r_0, self.i_0, self.r_k, self.i_k)
		self.M_fuel = find_mass_of_fuel(self.M_0, self.V_ch, self.c_d)
		self.square_sp = find_square_solar_panel(self.N_0, self.N_su)
		self.mass_sp = find_mass_solar_panel(self.square_sp, self.M_su)
		self.M_pn = find_mass_pn(self.M_0, self.Alfa_k, self.M_fuel, self.K_spx, self.Gamma, self.P_du, self.mass_sp)
		self.t_sec, self.t_day = find_time_transit(self.M_fuel, self.c_d, self.P_du)
		self.balistik_koef = find_balistik_koef(self.square_sp, self.M_0, self.ch_rotate)
		self.a_0 = find_beg_acceleration(self.P_du, self.M_0)
		
		# Подготовка значений для дискретного расчёта
		self.result = {'t':[],'V_xk':[],'psi_m':[]}
		for t in range(0, (int(self.t_sec) + self.h_step), self.h_step):
			self.result['t'].append(t)
			self.result['V_xk'].append(self.Vxk(t))
			self.result['psi_m'].append(self.psi_m(t))
		
		# Решаем дифф уравнение методом Рунге-Кутта без возмущений
		# Массив функция правых частей
		mass_f = (self.dpdt, self.dlmb1dt, self.dlmb2dt, self.domgdt, self.didt, self.dudt)
		# Массив начальных значений
		mass_beg = [self.r_0, 0, 0, 0, np.radians(self.i_0), 0]
		self.result['p'], self.result['lmb1'], self.result['lmb2'], self.result['Omg'], self.result['i'], self.result['u'] = self.runge_kut(mass_f, len(mass_f) , self.h_step, mass_beg, 0, self.t_sec)

		# Решаем дифф уравнение методом Рунге-Кутта с возмущениями
		# Массив функция правых частей
		mass_f = (self.Pdpdt, self.Pdlmb1dt, self.Pdlmb2dt, self.Pdomgdt, self.Pdidt, self.Pdudt)
		# Массив начальных значений
		mass_beg = [self.r_0, 0, 0, 0, np.radians(self.i_0), 0]
		self.result['p_pert'], self.result['lmb1_pert'], self.result['lmb2_pert'], self.result['Omg_pert'], self.result['i_pert'], self.result['u_pert'] = self.runge_kut(mass_f, len(mass_f) , self.h_step, mass_beg, 0, self.t_sec)

		# Массивы для графиков
		v = [self.result['p'],self.result['lmb1'],self.result['lmb2'],self.result['Omg'],self.result['i'],self.result['u']]
		v_pert = [self.result['p_pert'],self.result['lmb1_pert'],self.result['lmb2_pert'],self.result['Omg_pert'],self.result['i_pert'],self.result['u_pert']]
		a_tsw = list(np.array(v).transpose())
		b_tsw = list(np.array(v_pert).transpose())
		self.result['T'] = []
		self.result['S'] = []
		self.result['W'] = []
		self.result['TP'] = []
		self.result['SP'] = []
		self.result['WP'] = []
		self.result['T_accel'] = []
		self.result['S_accel'] = []
		self.result['W_accel'] = []
		self.result['x_ka'] = []
		self.result['y_ka'] = []
		self.result['z_ka'] = []
		self.result['h_orbit'] = []
		self.result['psi'] = []
		self.result['r'] = []
		self.result['r_pert'] = []
		self.result['TSW_accel'] = []

		for i in range(0,len(self.result['t'])):
			self.result['T'].append(self.T(self.result['t'][i],a_tsw[i]))
			self.result['S'].append(self.S(self.result['t'][i],a_tsw[i]))
			self.result['W'].append(self.w(self.result['t'][i],a_tsw[i]))
			self.result['psi'].append(self.psi(self.result['t'][i], a_tsw[i]))
			self.result['r'].append(self.r(a_tsw[i]))
			self.result['r_pert'].append(self.r(b_tsw[i]))
			self.result['TP'].append(self.TT(self.result['t'][i],b_tsw[i]))
			self.result['SP'].append(self.SS(self.result['t'][i],b_tsw[i]))
			self.result['WP'].append(self.ww(self.result['t'][i],b_tsw[i]))
			self.result['T_accel'].append(self.T_accel(self.result['t'][i],b_tsw[i]))
			self.result['S_accel'].append(self.S_accel(self.result['t'][i],b_tsw[i]))
			self.result['W_accel'].append(self.w_accel(self.result['t'][i],b_tsw[i]))
			self.result['TSW_accel'].append((self.result['T_accel'][i] ** (2) + self.result['S_accel'][i]  ** (2) + self.result['W_accel'][i] ** (2)) ** (0.5))
			self.result['x_ka'].append(self.x_ka(a_tsw[i]))
			self.result['y_ka'].append(self.y_ka(a_tsw[i]))
			self.result['z_ka'].append(self.z_ka(a_tsw[i]))
			self.result['h_orbit'].append((self.r(b_tsw[i])- 6371000) / 1000 )

		self.num_round = self.result['u'][-1]/(2*np.pi)

		# Время выполнения
		ending_time = datetime.now()
		self.time_of_compute = str(ending_time-begining_time)


		# pprint(self.result)

	# Вспомогательные функции для дискретного расчёта
	def psi_m(self,t):
		r0 = self.r_0
		i0 = self.i_0
		rk = self.r_k
		ik = self.i_k
		M = self.M_planet
		VHO = (G * M / (r0)) ** 0.5
		psi_m = np.arctan((np.sin(np.pi / 2 * ((ik - i0) * np.pi / 180))) / ((rk / r0) ** (0.5)) * ((1 - (np.cos(np.pi / 2 * ((ik - i0) * np.pi / 180))) / ((rk / r0) ** (0.5)) - (self.Vxk(t) / VHO) * (1 - (2 * np.cos(np.pi / 2 * ((ik - i0) * np.pi / 180))) / ((rk / r0) ** (0.5)) + (r0 / rk)) ** (0.5)) ** (-1)))
		if psi_m > 0 and i0 > ik:
			psi_m += -np.pi
		if psi_m < 0 and i0 < ik:
			psi_m += np.pi
		return psi_m

	def Vxk(self, t):
		M0 = self.M_0
		n = self.number_of_engine
		P = self.P_du
		a0 = self.a_0
		cd = self.c_d
		Vxk = cd * np.log(1 / (1 - a0 * t / cd))
		return Vxk

	def psi(self, t, v):
		psi = self.psi_m(t) * np.sign(np.cos(v[5]))
		return psi

	def T(self, t, v):
		T = self.a_0 * np.exp(self.Vxk(t) / self.c_d) * np.cos(self.psi(t,v))
		return T

	def S(self, t, v):
		return 0

	def w(self, t, v):
		W = self.a_0 * np.exp(self.Vxk(t) / self.c_d) * np.sin(self.psi(t,v))
		return W

	def r(self, v):
		return v[0] / (1 + v[1] * np.cos(v[5]) + v[2] * np.sin(v[5]))

		#функции без возмущений----------------------------------------------------------------------

	def dpdt (self, t, v):
		return 2 * self.r(v) * ((v[0] / M_u) ** (0.5)) * self.T(t, v)

	def dlmb1dt (self, t, v):
		if v[4] < 0.01:
			v[4] = 0.01
		return  ((v[0] / M_u) ** (0.5)) * (self.T(t,v) * (1 + self.r(v) / v[0]) * np.cos(v[5]) + self.S(t,v) * np.sin(v[5]) + (self.r(v) / v[0]) * (self.T(t,v) * v[2] - self.w(t,v) * v[1] * np.sin(v[5]) * (1 / np.tan(v[4]))))

	def dlmb2dt (self, t, v):
		if v[4] < 0.01:
			v[4] = 0.01
		return  ((v[0] / M_u) ** (0.5)) * (self.T(t,v) * (1 + self.r(v) / v[0]) * np.sin(v[5]) - self.S(t,v) * np.cos(v[5]) + (self.r(v) / v[0]) * (self.T(t,v) * v[1] + self.w(t,v) * v[2] * np.sin(v[5]) * (1 / np.tan(v[4]))))

	def domgdt (self, t, v):
		if v[4] < 0.01:
			v[4] = 0.01
		return (self.r(v) / ((M_u * v[0]) ** (0.5))) * np.sin(v[5]) * self.w(t,v) / np.sin(v[4]) 

	def didt (self, t, v):
		return (self.r(v) / ((M_u * v[0]) ** (0.5))) * np.cos(v[5]) * self.w(t,v)

	def dudt (self, t, v):
		if v[4] < 0.01:
			v[4] = 0.01
		return ((M_u * v[0]) ** (0.5)) / ((self.r(v)) ** 2) - self.r(v) * np.sin(v[5]) * (1 / np.tan(v[4])) * self.w(t,v) / ((M_u * v[0]) ** (0.5))


	#Функции с возмущениями----------------------------------------------------------------
	#Атмосфера-----------------------------------------------------------------------------
	def ro_atm(self, v):
		h_current = self.r(v) - 6371000
		if h_current < 150000 and h_current >= 120000:
			A_0 = 0.210005867 * (10 ** (4))
			A_1 = - 0.5618444757 * (10 ** (-1))
			A_2 = 0.2547466858 * (10 ** (-6))
			A_3 = - 0.2547466858 * (10 ** (-11))
			A_4 = 0.4309844119 * (10 ** (-17))
			m_pol = 17
		if h_current < 200000 and h_current >= 150000:
			A_0 = 0.10163937 * (10 ** (4))
			A_1 = - 0.2119530830 * (10 ** (-1))
			A_2 = 0.1671627815 * (10 ** (-6))
			A_3 = - 0.5894237068 * (10 ** (-12))
			A_4 = 0.7826684089 * (10 ** (-18))
			m_pol = 16
		if h_current < 250000 and h_current >= 200000:
			A_0 = 0.7631575 * (10 ** (3))
			A_1 = - 0.1150600844 * (10 ** (-1))
			A_2 = 0.6612598428 * (10 ** (-7))
			A_3 = - 0.1708736137 * (10 ** (-12))
			A_4 = 0.1669823114 * (10 ** (-18))
			m_pol = 15
		if h_current < 350000 and h_current >= 250000:
			A_0 = 0.1882203 * (10 ** (3))
			A_1 = - 0.2265999519 * (10 ** (-2))
			A_2 = 0.1041726141 * (10 ** (-7))
			A_3 = - 0.2155574922 * (10 ** (-13))
			A_4 = 0.1687430962 * (10 ** (-19))
			m_pol = 15
		if h_current < 450000 and h_current >= 350000:
			A_0 = 0.2804823 * (10 ** (3))
			A_1 = - 0.2432231125 * (10 ** (-2))
			A_2 = 0.8055024663 * (10 ** (-8))
			A_3 = - 0.1202418519 * (10 ** (-13))
			A_4 = 0.6805101379 * (10 ** (-20))
			m_pol = 14
		if h_current < 600000 and h_current >= 450000:
			A_0 = 0.5599362 * (10 ** (3))
			A_1 = - 0.3714141392 * (10 ** (-2))
			A_2 = 0.9358870345 * (10 ** (-8))
			A_3 = - 0.1058591881 * (10 ** (-13))
			A_4 = 0.4525531532 * (10 ** (-20))
			m_pol = 13
		if h_current < 800000 and h_current >= 600000:
			A_0 = 0.8358756 * (10 ** (3))
			A_1 = - 0.4265393073 * (10 ** (-2))
			A_2 = 0.8252842085 * (10 ** (-8))
			A_3 = - 0.7150127437 * (10 ** (-14))
			A_4 = 0.2335744331 * (10 ** (-20))
			m_pol = 12
		if h_current < 1000000 and h_current >= 800000:
			A_0 = 0.8364965 * (10 ** (2))
			A_1 = - 0.3162492458 * (10 ** (-3))
			A_2 = 0.4602064246 * (10 ** (-9))
			A_3 = - 0.3021858469 * (10 ** (-15))
			A_4 = 0.7512304301 * (10 ** (-22))
			m_pol = 12
		if h_current < 1200000 and h_current >= 1000000:
			A_0 = 0.383220 * (10 ** (2))
			A_1 = - 0.50980 * (10 ** (-4))
			A_2 = 0.18100 * (10 ** (-10))
			A_3 = 0
			A_4 = 0
			m_pol = 11
		if h_current >= 1200000:
			A_0 = 0
			A_1 = 0
			A_2 = 0
			A_3 = 0
			A_4 = 0
			m_pol = 0
		n_air = (A_0 + A_1 * h_current + A_2 * (h_current ** (2)) + A_3 * (h_current ** (3)) + A_4 * (h_current ** (4))) * (10 ** (m_pol))
		if h_current < 250000 and h_current >= 120000:
			B_0 = 46.9083
			B_1 = - 29.71210 * (10 ** (-5))
			B_2 = 12.08693 * (10 ** (-10))
			B_3 = - 1.85675 * (10 ** (-15))
		if h_current < 400000 and h_current >= 250000:
			B_0 = 40.4668
			B_1 = - 15.52722 * (10 ** (-5))
			B_2 = 3.55735 * (10 ** (-10))
			B_3 = - 3.02340 * (10 ** (-16))
		if h_current < 650000 and h_current >= 400000:
			B_0 = 6.3770
			B_1 = 6.3770 * (10 ** (-5))
			B_2 = - 1.10144 * (10 ** (-10))
			B_3 = 3.36907 * (10 ** (-17))
		if h_current < 900000 and h_current >= 650000:
			B_0 = 75.6896
			B_1 = - 17.61243 * (10 ** (-5))
			B_2 = 1.33603 * (10 ** (-10))
			B_3 = - 2.87884 * (10 ** (-17))
		if h_current < 1050000 and h_current >= 900000:
			B_0 = 112.4838
			B_1 = - 30.68086 * (10 ** (-5))
			B_2 = 2.90329 * (10 ** (-10))
			B_3 = - 9.20616 * (10 ** (-17))
		if h_current < 1200000 and h_current >= 1050000:
			B_0 = 9.8970
			B_1 = - 1.19732 * (10 ** (-5))
			B_2 = 7.78247 * (10 ** (-12))
			B_3 = - 1.77541 * (10 ** (-18))
		if h_current >= 1200000:
			B_0 = 0
			B_1 = 0
			B_2 = 0
			B_3 = 0
		M_air = B_0 + B_1 * h_current + B_2 * (h_current ** (2)) + B_3 * (h_current ** (3))
		ro_atm = n_air * M_air / (6.02214076 * (10 ** (23)))
		return np.absolute(ro_atm)

	def V_current(self, v):
		V_current = (M_u / v[0]) ** (0.5) * (v[0] / self.r(v) + v[1] * np.cos(v[5]) + v[2] * np.sin(v[5]) + (v[1] ** (2)) + (v[2] ** (2))) ** (0.5)
		return V_current

	def V_rad(self, v):
		V_rad = (((M_u / v[0]) ** (0.5)) * (v[1] * np.sin(v[5]) - v[2] * np.cos(v[5])))
		return V_rad

	def V_normal(self, v):
		V_normal = ((M_u / v[0]) ** (0.5)) * (1 + v[1] * np.cos(v[5]) + v[2] * np.sin(v[5]))
		return V_normal

	#Солнечное давление----------------------------------------------------------------------
	def srat_time(self):
		return (self.month - 1) * 2629743.765 + float(self.day) * 86400 + float(self.hour) * 3600 + float(self.minute) * 60 + float(self.second)

	def r_sun(self, t):
		return (149.56 * (10 ** 9)) / (1 + 0.0167 * np.cos((self.srat_time() + t)/31556925.19))

	def find_alfa_sun(self, t):
		n_days = (float(self.year) - 2000) * 365.25  + (self.month - 1) * 30 + float(self.day) + float(self.hour) / 24 + float(self.minute) / 1440 + float(self.second) / 86400 + t / 86400
		average_longitude = 280.460 + 0.9856474 * n_days
		average_anomaly = 357.528 + 0.9856003 * n_days
		average_longitude = average_longitude - (360 * (average_longitude // 360))
		average_anomaly = average_anomaly - 360 * (average_anomaly // 360)
		ecliptic_longitude = average_longitude + 1.915 * np.sin(average_anomaly * np.pi / 180) + 0.020 * np.sin(2 * average_anomaly * np.pi / 180)
		inclination_of_ecliptic = 23.439 - 0.0000004 * n_days
		alfa_sun = np.arctan2(np.cos(inclination_of_ecliptic * np.pi / 180) * np.sin(ecliptic_longitude * np.pi / 180) , np.cos(ecliptic_longitude * np.pi / 180))
		return alfa_sun

	def find_delta_sun(self, t):
		n_days = (float(self.year) - 2000) * 365.25  + (self.month - 1) * 30 + float(self.day) + float(self.hour) / 24 + float(self.minute) / 1440 + float(self.second) / 86400 + t / 86400
		average_longitude = 280.460 + 0.9856474 * n_days
		average_anomaly = 357.528 + 0.9856003 * n_days
		average_longitude = average_longitude - (360 * (average_longitude // 360))
		average_anomaly = average_anomaly - 360 * (average_anomaly // 360)
		ecliptic_longitude = average_longitude + 1.915 * np.sin(average_anomaly * np.pi / 180) + 0.020 * np.sin(2 * average_anomaly * np.pi / 180)
		inclination_of_ecliptic = 23.439 - 0.0000004 * n_days
		delta_sun = np.arcsin(np.sin(inclination_of_ecliptic * np.pi / 180) * np.sin(ecliptic_longitude * np.pi / 180))
		return delta_sun


	def x_ka(self, v):
		return self.r(v) * (np.cos(v[3]) * np.cos(v[5]) - np.sin(v[3]) * np.sin(v[5]) * np.cos(v[4]))

	def y_ka(self, v):
		return self.r(v) * (np.sin(v[3]) * np.cos(v[5]) + np.cos(v[3]) * np.sin(v[5]) * np.cos(v[4]))

	def z_ka(self, v):
		return self.r(v) * np.sin(v[5]) * np.sin(v[4])

	def r_one(self, t,v):
		return ((self.r_sun(t) * np.cos(self.find_delta_sun(t)) * np.cos(self.find_alfa_sun(t)) - self.x_ka(v)) ** 2 + (self.r_sun(t) * np.cos(self.find_delta_sun(t)) * np.sin(self.find_alfa_sun(t)) - self.y_ka(v)) ** 2 + (self.r_sun(t) * np.sin(self.find_delta_sun(t)) - self.z_ka(v) ) ** 2) ** (0.5)

	def fi_1(self,t,v):
		return np.arccos( ((self.r(v) ** 2) + (self.r_one(t,v) ** 2) - (self.r_sun(t) ** 2)) / (2 * self.r(v) * self.r_one(t,v)))

	def r_big_e(self,v):
		return np.arcsin(6371000 / self.r(v))

	def r_big_s(self, t,v):
		return np.arcsin(696000000 / self.r_one(t,v))

	def fi_e(self, t,v):
		return 2 * np.arccos(((self.r_big_e(v) ** 2) - (self.r_big_s(t,v) ** 2) + (self.fi_1(t,v) ** 2)) / (2 * self.r_big_e(v) * self.fi_1(t,v)))

	def fi_s(self,t,v):
		return 2 * np.arccos((-(self.r_big_e(v) ** 2) + (self.r_big_s(t,v) ** 2) + (self.fi_1(t,v) ** 2)) / (2 * self.r_big_s(t,v) * self.fi_1(t,v)))

	def s_es(self, t,v):
		if self.fi_s(t, v) >= np.pi:
			s_es_param = ((self.r_big_e(v) ** 2) / 2) * (self.fi_e(t,v) - np.sin(self.fi_e(t,v))) + ((self.r_big_s(t,v) ** 2) / 2) * (self.fi_s(t,v) + np.sin(self.fi_s(t,v)))
		if self.fi_s(t, v) < np.pi:
			s_es_param = ((self.r_big_e(v) ** 2) / 2) * (self.fi_e(t,v) - np.sin(self.fi_e(t,v))) + ((self.r_big_s(t,v) ** 2) / 2) * (self.fi_s(t,v) - np.sin(self.fi_s(t,v)))
		return s_es_param

	def psi_p (self, t,v):
		return 1 - (self.s_es(t,v))/(np.pi * (self.r_big_s(t,v)) ** 2)

	def psi_t (self, t,v):
		if self.fi_1(t,v) >= self.r_big_e(v) + self.r_big_s(t,v):
			psi_t_param = 1
		elif self.fi_1(t,v) < self.r_big_e(v) + self.r_big_s(t,v) and self.fi_1(t,v) >= self.r_big_e(v) - self.r_big_s(t,v):
			psi_t_param = self.psi_p(t,v)
		else:
			psi_t_param = 0
		return psi_t_param

	def TT(self, t, v):
		T = self.T(t, v)
		if self.add_grav == True:
			T += (- ee / (self.r(v) ** 4)) * (np.sin(v[4]) ** (2)) * np.sin(2 * v[5])
		if self.add_atm == True:
			T += -0.5 * float(self.balistik_koef) * self.ro_atm(v) * (self.V_current(v) - OO * self.r(v) * np.cos(v[5])) * (self.V_normal(v) - OO * self.r(v) * np.cos(v[4]))
		if  self.add_sw == True:
			T += -1.2 * (float(self.balistik_koef) * 2 / 2.15) * (4.65 * (10 ** -6)) * self.psi_t(t,v) * ((1.4959787061 * (10 ** 11)) / self.r_sun(t)) * (np.sin(v[4]) * np.sin(self.find_delta_sun(t)) + np.cos(v[4]) * np.cos(self.find_delta_sun(t)) * np.cos(v[3] + v[5] - self.find_delta_sun(t)))
		return T

	def SS(self, t , v):
		S = 0
		if self.add_grav == True:
			S += (ee / (self.r(v) ** 4)) * (3 * (np.sin(v[4]) ** (2)) * (np.sin(v[5]) ** (2)) - 1)
		if self.add_atm == True:
			S += -0.5 * float(self.balistik_koef) * self.ro_atm(v) * (self.V_current(v) - OO * self.r(v) * np.cos(v[5])) * self.V_rad(v)
		if  self.add_sw == True:
			S += -1.2 * (float(self.balistik_koef) * 2 / 2.15) * (4.65 * (10 ** -6)) * self.psi_t(t,v) * ((1.4959787061 * (10 ** 11)) / self.r_sun(t)) * (np.cos(v[4]) * np.sin(self.find_delta_sun(t)) - np.sin(v[4]) * np.cos(self.find_delta_sun(t)) * np.cos(v[3] + v[5] - self.find_delta_sun(t)))
		return S

	def ww(self, t, v):
		W = self.w(t, v)
		if self.add_grav == True:
			W += (- ee / (self.r(v) ** 4)) * np.sin(2 * v[4]) * np.sin(v[5])
		if self.add_sw == True:
			W += -1.2 * (float(self.balistik_koef) * 2 / 2.15) * (4.65 * (10 ** -6)) * self.psi_t(t,v) * ((1.4959787061 * (10 ** 11)) / self.r_sun(t)) * (-np.cos(v[4]) * np.cos(self.find_delta_sun(t)) * np.sin(v[3] + v[5] - self.find_delta_sun(t)))
		return W

	def Pdpdt (self, t, v):
		return 2 * self.r(v) * ((v[0] / M_u) ** (0.5)) * self.TT(t, v)

	def Pdlmb1dt (self, t,v):
		if v[4] < 0.01:
			v[4] = 0.01
		return  ((v[0] / M_u) ** (0.5)) * (self.TT(t,v) * (1 + self.r(v) / v[0]) * np.cos(v[5]) + self.SS(t,v) * np.sin(v[5]) + (self.r(v) / v[0]) * (self.TT(t,v) * v[2] - self.ww(t,v) * v[1] * np.sin(v[5]) * (1 / np.tan(v[4]))))

	def Pdlmb2dt (self, t,v):
		if v[4] < 0.01:
			v[4] = 0.01
		return  ((v[0] / M_u) ** (0.5)) * (self.TT(t,v) * (1 + self.r(v) / v[0]) * np.sin(v[5]) - self.SS(t,v) * np.cos(v[5]) + (self.r(v) / v[0]) * (self.TT(t,v) * v[1] + self.ww(t,v) * v[2] * np.sin(v[5]) * (1 / np.tan(v[4]))))

	def Pdomgdt (self, t,v):
		if v[4] < 0.01:
			v[4] = 0.01
		return (self.r(v) / ((M_u * v[0]) ** (0.5))) * np.sin(v[5]) * self.ww(t,v) / np.sin(v[4]) 

	def Pdidt (self, t,v):
		return (self.r(v) / ((M_u * v[0]) ** (0.5))) * np.cos(v[5]) * self.ww(t,v)

	def Pdudt (self, t,v):
		if v[4] < 0.01:
			v[4] = 0.01
		return ((M_u * v[0]) ** (0.5)) / ((self.r(v)) ** 2) - self.r(v) * np.sin(v[5]) * (1 / np.tan(v[4])) * self.ww(t,v) / ((M_u * v[0]) ** (0.5))

	def T_accel(self,t,v):
		T = 0
		if int(self.add_grav) == True:
			T += (- ee / (self.r(v) ** 4)) * (np.sin(v[4]) ** (2)) * np.sin(2 * v[5])
		if int(self.add_atm) == True:
			T += -0.5 * float(self.balistik_koef) * self.ro_atm(v) * (self.V_current(v) - OO * self.r(v) * np.cos(v[5])) * (self.V_normal(v) - OO * self.r(v) * np.cos(v[4]))
		if  int(self.add_sw) == True:
			T += -1.2 * (float(self.balistik_koef) * 2 / 2.15) * (4.65 * (10 ** -6)) * self.psi_t(t,v) * ((1.4959787061 * (10 ** 11)) / self.r_sun(t)) * (np.sin(v[4]) * np.sin(self.find_delta_sun(t)) + np.cos(v[4]) * np.cos(self.find_delta_sun(t)) * np.cos(v[3] + v[5] - self.find_delta_sun(t)))
		return T

	def S_accel(self, t,v):
		S = 0
		if int(self.add_grav) == True:
			S += (ee / (self.r(v) ** 4)) * (3 * (np.sin(v[4]) ** (2)) * (np.sin(v[5]) ** (2)) - 1)
		if int(self.add_atm) == True:
			S += -0.5 * float(self.balistik_koef) * self.ro_atm(v) * (self.V_current(v) - OO * self.r(v) * np.cos(v[5])) * self.V_rad(v)
		if  int(self.add_sw) == True:
			S += -1.2 * (float(self.balistik_koef) * 2 / 2.15) * (4.65 * (10 ** -6)) * self.psi_t(t,v) * ((1.4959787061 * (10 ** 11)) / self.r_sun(t)) * (np.cos(v[4]) * np.sin(self.find_delta_sun(t)) - np.sin(v[4]) * np.cos(self.find_delta_sun(t)) * np.cos(v[3] + v[5] - self.find_delta_sun(t)))
		return S

	def w_accel(self, t,v):
		W = 0
		if int(self.add_grav) == True:
			W += (- ee / (self.r(v) ** 4)) * np.sin(2 * v[4]) * np.sin(v[5])
		if  int(self.add_sw) == True:
			W += -1.2 * (float(self.balistik_koef) * 2 / 2.15) * (4.65 * (10 ** -6)) * self.psi_t(t,v) * ((1.4959787061 * (10 ** 11)) / self.r_sun(t)) * (-np.cos(v[4]) * np.cos(self.find_delta_sun(t)) * np.sin(v[3] + v[5] - self.find_delta_sun(t)))
		return W

# tr1 = Transit(
# 	N_0 = 400,
# 	N_eng = 4.5,
# 	P_eng = 0.28,
# 	M_planet = 5.97*10**(24),
# 	r_0 = 6971,
# 	i_0 = 51.6,
# 	r_k = 42157,
# 	i_k = 0,
# 	M_0 = 20000,
# 	c_d = 17000,
# 	N_su = 310,
# 	M_su = 1.6,
# 	Alfa_k = 0.1,
# 	Gamma = 40,
# 	K_spx = 0.07,
# 	h_step = 100000,
# 	year = 2020,
# 	month=2,
# 	day = 10,
# 	hour = 5,
# 	minute = 32,
# 	second = 34,
# 	ch_rotate=False,
# 	add_atm= True,
# 	add_sw=True,
# 	add_grav=True
# 	)

# tr1.general_calculation()