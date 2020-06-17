import sqlite3
import os
import traceback
name_db = 'database.db'
cur_dir = os.getcwd()
path_db = os.path.join(cur_dir, name_db)

# проверка на существование базы данных
if not os.path.exists(path_db):
    try:
        # создание базы данных + создание таблиц
        conn = sqlite3.connect(path_db)
        cursor = conn.cursor()

        # создание таблиц + наполнение
        cursor.executescript("""
			BEGIN TRANSACTION;
			CREATE TABLE "zagotovka" (
				`name`    TEXT,
				`Rz`    INTEGER,
				`Ti`    INTEGER,
				`p` INTEGER,
				`e` INTEGER,
				`kvalitet1` INTEGER
			);
            CREATE TABLE "operations" (
				`name`    TEXT,
				`Rz`    INTEGER,
				`Ti`    INTEGER,
				`p` INTEGER,
				`e` INTEGER,
				`kvalitet1` INTEGER
			);
			CREATE TABLE "kvalitet" (
				`d`    INTEGER,
				`d1`    INTEGER,
				`k0`    INTEGER,
				`k1`    INTEGER,
				`k2`    INTEGER,
				`k3`    INTEGER,
				`k4`    INTEGER,
				`k5`    INTEGER,
				`k6`    INTEGER,
				`k7`    INTEGER,
				`k8`    INTEGER,
				`k9`    INTEGER,
				`k10`    INTEGER,
				`k11`    INTEGER,
				`k12`    INTEGER,
				`k13`    INTEGER,
				`k14`    INTEGER,
				`k15`    INTEGER,
				`k16`    INTEGER,
				`k17`    INTEGER
			);
			INSERT INTO `kvalitet`  (d, d1, k0,k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,k17)  
			VALUES(0,3,0.5,0.8,1.2,2,3,4,6,10,14,25,40,60,100,140,250,400,600,1000);
			
			INSERT INTO `kvalitet`  (d, d1, k0,k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,k17)  
			VALUES(3,6,0.6,1,1.5,2.5,4,5,8,12,18,30,48,75,120,180,300,480,750,1200);
			
			INSERT INTO `kvalitet`  (d, d1, k0,k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,k17)
			VALUES(6,10,0.6,1,1.5,2.5,4,6,9,15,22,36,58,90,150,220,360,580,900,1500);
			INSERT INTO `kvalitet`  (d, d1, k0,k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,k17)
			VALUES(10,18,0.8,1.2,2,3,5,8,11,18,27,43,70,110,180,270,430,700,1100,1800);
			
			INSERT INTO `kvalitet`  (d, d1, k0,k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,k17)  
			VALUES(18,30,1,1.5,2.5,4,6,9,13,21,33,52,84,130,210,330,520,840,1300,2100);
			
			INSERT INTO `kvalitet`  (d, d1, k0,k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,k17)  
			VALUES(30,50,1,1.5,2.5,4,7,11,16,25,39,62,100,160,250,390,620,1000,1600,2500);
			
			INSERT INTO `kvalitet`  (d, d1, k0,k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,k17)  
			VALUES(50,80,1.2,2,3,5,8,13,19,30,46,74,120,190,30,460,740,1200,1900,3000);
			
			INSERT INTO `kvalitet`  (d, d1, k0,k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,k17)  
			VALUES(80,120,1.5,2.5,4,6,10,15,22,35,54,87,140,220,350,540,870,1400,2200,3500);
			
			INSERT INTO `kvalitet`  (d, d1, k0,k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,k17)  
			VALUES(120,180,2,3.5,5,8,12,18,25,40,63,100,160,250,400,630,1000,1600,2500,4000);

            INSERT INTO `kvalitet`  (d, d1, k0,k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,k17)  
			VALUES(180,200,3,4.5,7,10,14,20,29,46,72,115,185,290,460,720,1150,1850,2900,4600);
            								
			
			INSERT INTO `zagotovka`  (name, Rz, Ti,p,e,kvalitet1)  
			VALUES('Лиття в кокіль',300, 200,180,90,15);
			
			INSERT INTO `zagotovka`  (name, Rz, Ti,p,e,kvalitet1)  
			VALUES('Лиття відцентрове',200, 200,160,60,15);
			
			INSERT INTO `zagotovka`  (name, Rz, Ti,p,e,kvalitet1)  
			VALUES('Лиття в оболонкові форми',40 , 116,120,50,12);
			
			INSERT INTO `zagotovka`  (name, Rz, Ti,p,e,kvalitet1)  
			VALUES('Лиття під тиском',50,100,80,70,15);
			
			INSERT INTO `zagotovka`  (name, Rz, Ti,p,e,kvalitet1)  
			VALUES('Лиття за виплавлюваних моделях',30 , 100,60,80,15);
			
			INSERT INTO `zagotovka`  (name, Rz, Ti,p,e,kvalitet1)  
			VALUES('Гаряча штамповка',400,400,120,135,16);
			
			INSERT INTO `zagotovka`  (name, Rz, Ti,p,e,kvalitet1)  
			VALUES('Холодна штамповка',400,400,120,135,16);
			
			INSERT INTO `zagotovka`  (name, Rz, Ti,p,e,kvalitet1)  
			VALUES('Прокат',240,240,90,140,16);
			
			
			
			
			INSERT INTO `operations`  (name, Rz, Ti,p,e,kvalitet1)  
			VALUES('Точіння чорнове',80, 40,38,60,12);
			
			INSERT INTO `operations`  (name, Rz, Ti,p,e,kvalitet1)  
			VALUES('Точіння напівчистове',40 , 30,2,15,11);
			
			INSERT INTO `operations`  (name, Rz, Ti,p,e,kvalitet1)  
			VALUES('Точіння чистове',1.6 , 25,7,7,9);
		
			INSERT INTO `operations`  (name, Rz, Ti,p,e,kvalitet1)  
			VALUES('Полірування',10 , 25,7,7,6);
			
			INSERT INTO `operations`  (name, Rz, Ti,p,e,kvalitet1)  
			VALUES('Шліфування',6.3, 25,7,7,8);
			COMMIT; """)

        # фиксирую коммит
        conn.commit()


    except Exception:

        print(str(traceback.format_exc()))
