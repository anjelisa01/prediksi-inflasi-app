#Import Library
import streamlit as st
import pymysql
# import mysql.connector
import pandas as pd
import math
import numpy as np
import calendar
from numpy.linalg import inv
from streamlit_option_menu import option_menu
import datetime
import sklearn.metrics as sm
from sklearn.model_selection import train_test_split

#Set title page
st.set_page_config(page_title="Sistem Prediksi Inflasi")
#Set initial session state ketika aplikasi pertama kali running
if 'loggedIn' not in st.session_state:
        st.session_state.loggedIn = False
        st.session_state.username= 0

#Container
headerSection = st.container()
loginSection = st.container()
adminSection=st.container()
ubahDataAdminLogin=st.container()
logOutSection = st.container()
datasetSectionAdmin = st.container()  


import configdb

database_connection = pymysql.connect(
   host=configdb.hostdb,
   port=configdb.portdb,
   user=configdb.userdb,
   password=configdb.passdb,
   database=configdb.namadb
)
mycursor=database_connection.cursor()

# import konekdatabase as db
# database_connection=db.database_connection
# mycursor=database_connection.cursor()

#Functions
#-----------------------------------------------------
#Tentang Login Admin
def login_user(username,password):
    mycursor.execute('SELECT username, password FROM tb_admin WHERE username =%s AND password = %s',(username,password))
    data = mycursor.fetchall()
    return data
def LoggedIn_Clicked(userName, password):
    if login_user(userName, password):
        # st.success("Login berhasil: Logged In as {}".format(userName))
        st.session_state['loggedIn'] = True
        st.session_state['username']=userName
    else:
        st.session_state['loggedIn'] = False;
        st.error("Invalid user name or password")
def show_login_page():
    with loginSection:
        st.title("Login Sebagai Admin")
        if st.session_state['loggedIn'] == False:
            username=st.text_input("Username")
            password=st.text_input("Password",type='password')
            st.button("Login Admin",on_click=LoggedIn_Clicked,args=(username,password))
def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    st.session_state['username'] = 0
def show_logout_page():
    loginSection.empty();
    with logOutSection:
        kol1,kol2,kol3=st.columns([0.4,0.2,0.4])
        with kol1:
            st.write(' ')
        with kol2:
            st.button ("Log Out", key="logout", on_click=LoggedOut_Clicked)
        with kol3:
            st.write(' ') 
#-----------------------------------------------------
#Function db ke program: menu admin
def get_data_admin(task):
	mycursor.execute('SELECT * FROM tb_admin WHERE id_admin="{}"'.format(task))
	data = mycursor.fetchall()
	return data
def view_all_data_admin():
	mycursor.execute('SELECT id_admin,username,email,nama_admin FROM tb_admin')
	data = mycursor.fetchall()
	return data        
#-----------------------------------------------------
#Function db ke program: menu dataset untuk admin
def tampilDataJoin_Admin():
    # mycursor.execute('SELECT Orders.OrderID, Customers.CustomerName, Orders.OrderDate FROM Orders INNER JOIN Customers ON Orders.CustomerID=Customers.CustomerID;')
    mycursor.execute('SELECT tb_dataset.id_data, tb_dataset.bln_tahun,tb_dataset.nilai,tb_jenis_var.nama_var,tb_dataset.id_admin FROM tb_dataset INNER JOIN tb_jenis_var ON tb_dataset.id_jenis_var=tb_jenis_var.id_jenis_var;')
    #mycursor.execute('select * from tb_dataset where id_jenis_var=1')
    data = mycursor.fetchall()
    return data
def getDataSendiri1():
    mycursor.execute('SELECT tb_jenis_var.nama_var ,tb_dataset.bln_tahun,tb_dataset.nilai,tb_dataset.id_admin FROM tb_dataset INNER JOIN tb_jenis_var ON tb_dataset.id_jenis_var=tb_jenis_var.id_jenis_var where tb_dataset.id_jenis_var=1;')
    data = mycursor.fetchall()
    return data
def getDataSendiri2():
    mycursor.execute('SELECT tb_jenis_var.nama_var ,tb_dataset.bln_tahun,tb_dataset.nilai,tb_dataset.id_admin FROM tb_dataset INNER JOIN tb_jenis_var ON tb_dataset.id_jenis_var=tb_jenis_var.id_jenis_var where tb_dataset.id_jenis_var=2;')
    data = mycursor.fetchall()
    return data
def getDataSendiri3():
    mycursor.execute('SELECT tb_jenis_var.nama_var ,tb_dataset.bln_tahun,tb_dataset.nilai,tb_dataset.id_admin FROM tb_dataset INNER JOIN tb_jenis_var ON tb_dataset.id_jenis_var=tb_jenis_var.id_jenis_var where tb_dataset.id_jenis_var=3;')
    data = mycursor.fetchall()
    return data
def getDataSendiri4():
    mycursor.execute('SELECT tb_jenis_var.nama_var ,tb_dataset.bln_tahun,tb_dataset.nilai,tb_dataset.id_admin FROM tb_dataset INNER JOIN tb_jenis_var ON tb_dataset.id_jenis_var=tb_jenis_var.id_jenis_var where tb_dataset.id_jenis_var=4;')
    data = mycursor.fetchall()
    return data
#crud dataset
def view_all_data():
	mycursor.execute('SELECT * FROM tb_dataset')
	data = mycursor.fetchall()
	return data
def get_data(task):
	mycursor.execute('SELECT * FROM tb_dataset WHERE id_data="{}"'.format(task))
	data = mycursor.fetchall()
	return data
def add_data(bln_tahun,nilai,id_jenis_var,id_admin):
	mycursor.execute('INSERT INTO tb_dataset(bln_tahun,nilai,id_jenis_var,id_admin) VALUES (%s,%s,%s,%s)',(bln_tahun,nilai,id_jenis_var,id_admin))
	database_connection.commit() 
def edit_data(id_data,new_bln_tahun,new_nilai,new_id_jenis_var,new_id_admin):
	mycursor.execute("UPDATE tb_dataset SET bln_tahun =%s,nilai=%s,id_jenis_var=%s,id_admin=%s WHERE id_data=%s ",(new_bln_tahun,new_nilai,new_id_jenis_var,new_id_admin,id_data))
	database_connection.commit()
	data = mycursor.fetchall()
	return data 
def delete_data(id_data):
	mycursor.execute('DELETE FROM tb_dataset WHERE id_data="{}"'.format(id_data))
	database_connection.commit() 

#-----------------------------------------------------
#Fitur jika login sebagai admin
def show_admin_page():
    with adminSection:
        # st.title(f"Menu Admin")
        usernameLoggedIn=st.session_state.username
        st.title("Menu Admin")
        st.write("Logged In sebagai: ",usernameLoggedIn)
        option=st.sidebar.selectbox("Pilih Opsi:",("Lihat Daftar Admin","Tambah Admin Baru","Hapus Admin","Menu Admin LoggedIn"))
        if option=="Lihat Daftar Admin":
            sql_query = pd.read_sql_query ('''
                                SELECT
                                *
                                FROM tb_admin
                                ''', database_connection)
        
            dataset = pd.DataFrame(sql_query,columns = ['id_admin','username','email','nama_admin'])
            kol1,kol2,kol3=st.columns([0.15,0.7,0.15])
            with kol1:
                st.write(' ')
            with kol2:
                st.subheader("Daftar Admin")
                dataset
            with kol3:
                st.write(' ')
        elif option=="Tambah Admin Baru":
            kol1,kol2,kol3=st.columns([0.15,0.7,0.15])
            with kol1:
                st.write(' ')
            with kol2:
                st.subheader("Tambah Admin Baru")
                username=st.text_input("Username")
                password=st.text_input("Password",type='password')
                email=st.text_input("Email")
                nama_admin=st.text_input("Nama Admin")
                if st.button("Tambah"):
                    sql= "insert into tb_admin(username,password,email,nama_admin) values(%s,%s,%s,%s)"
                    val= (username,password,email,nama_admin)
                    mycursor.execute(sql,val)
                    database_connection.commit()
                    st.success("Data Admin Berhasil Ditambahkan")
            with kol3:
                st.write(' ')


        elif option=="Hapus Admin":
                    st.subheader("Hapus Admin")
                    with st.expander("Daftar admin di dalam Sistem"):
                        col1,col2,col3 = st.columns([0.1,0.8,0.1])
                        with col1:
                            st.write(" ")
                        with col2:
                            result = view_all_data_admin()
                            clean_df = pd.DataFrame(result,columns=["Id Admin","Usename","Email","Nama Admin"])
                            st.dataframe(clean_df)
                        with col3:
                            st.write(" ")
                    col1,col2,col3 = st.columns([0.15,0.7,0.15])
                    with col1:
                        st.write(" ")
                    with col2:
                        id=st.number_input("Masukan id admin yang ingin dihapus",step=1)
                        if st.button("Hapus admin"):
                            sql="delete from tb_admin where id_admin=%s"
                            val=(id,)
                            mycursor.execute(sql,val)
                            database_connection.commit()
                            st.success("Data Admin dengan id: {} Berhasil Dihapus!!!".format(id))
                    with col3:
                            st.write(" ")


        elif option=="Menu Admin LoggedIn":
            kol1,kol2,kol3=st.columns([0.15,0.7,0.15])
            with kol1:
                st.write(' ')
            with kol2:
                st.subheader("Menu Admin Logged In")
                with st.expander("Ubah Data"):
                    # list_data = [i[0] for i in view_id_data_admin()]
                    # selected_id = st.selectbox("Pilih Id Data yang ingin diubah:",list_data)
                    def getIdFromState():
                        username=usernameLoggedIn
                        mycursor.execute('SELECT id_admin FROM tb_admin WHERE username="{}"'.format(username))
                        idadmin = mycursor.fetchall()
                        return idadmin
                    idDriState=getIdFromState()
                    idAdminSiapUpdate=idDriState[0][0]
                    #ambil id admin dari matching dari session state admin
                    data_result = get_data_admin(idAdminSiapUpdate)
                    # data_result
                    if data_result:
                        idAdmin = data_result[0][0]
                        userName = str(data_result[0][1])
                        passWord = str(data_result[0][2])
                        eMail=str(data_result[0][3])
                        namaAdmin=str(data_result[0][4])
                        username=st.text_input("Username Baru",value=userName)
                        password=st.text_input("Password Baru",value=passWord,type='password')
                        email=st.text_input("Email Baru",value=eMail)
                        nama_admin=st.text_input("Nama Admin Baru",value=namaAdmin)

                        if st.button("Update"):
                            sql="update tb_admin set username=%s,password=%s,email=%s,nama_admin=%s where username =%s"
                            st.session_state['username']=username
                            val=(username,password,email,nama_admin,usernameLoggedIn)
                            mycursor.execute(sql,val)
                            database_connection.commit()
                            st.success("Data Admin Berhasil Diubah!!!")                           
                            st.write("View Updated Data")
                            result = get_data_admin(idAdmin)
                            clean_df = pd.DataFrame(result,columns=["ID Admin","Username","Password","Email","Nama Admin"])
                            st.dataframe(clean_df)
                show_logout_page()    
            with kol3:
                st.write(' ')   



        
def show_dataset_admin():
    with datasetSectionAdmin:
        st.title(f"Kelola Dataset") 
        option=st.sidebar.selectbox("Select an Operation",("Lihat Dataset","Tambah Data","Update Data","Hapus Data"))
        if option=="Lihat Dataset":
            showDatasetUserAdmin()
        elif option=="Tambah Data":
            st.subheader("Tambah Data")
            col1,col2,col3 = st.columns([0.1,0.8,0.1])
            with col1:
                st.write(" ")
            with col2:
                this_year = datetime.date.today().year
                this_month = datetime.date.today().month
                report_year = st.selectbox('', range(this_year, 2014, -1))
                month_abbr = calendar.month_abbr[1:]
                report_month_str = st.radio('', month_abbr, index=this_month - 1, horizontal=True)
                report_month = month_abbr.index(report_month_str) + 1
                periode=f'{report_year}-{report_month}-01'
                
                def cek_data(periode,id_jenis):
                    mycursor.execute('select bln_tahun,id_jenis_var FROM tb_dataset where bln_tahun="{}" and id_jenis_var="{}" '.format(periode,id_jenis))
                    data = mycursor.fetchall()
                    return data
                
                input_nilai=st.number_input("Nilai Variabel")
                input_id_jenis = st.selectbox('Nama Variabel:',
                        ('Nilai Inflasi', 'BI Rate', 'Nilai Tukar','Uang Beredar M2'))
                if input_id_jenis=="Nilai Inflasi":
                        input_id_jenis=1
                if input_id_jenis=='BI Rate': 
                        input_id_jenis=2
                if input_id_jenis=='Nilai Tukar':
                        input_id_jenis=3
                if input_id_jenis=='Uang Beredar M2':
                        input_id_jenis=4
                input_id_admin=st.number_input("ID Admin",min_value=1, step=1)
                if st.button("Tambah Data"):
                    cek_periode=cek_data(periode,input_id_jenis)
                    cek_periode2=pd.DataFrame(cek_periode,columns=["Periode","id jenis"])
                    if cek_periode2.empty:
                        t=0  
                    else:
                        t = str(cek_periode2['Periode'].values[0])     
                    if periode==t:
                        st.write('Data periode sudah ada!')
                    else:
                        add_data(periode,input_nilai,input_id_jenis,input_id_admin)
                        st.success("Berhasil Tambah data")
                
                
            with col3:
                st.write(" ")
        elif option=="Update Data":
            st.subheader("Update Data")
            with st.expander("Lihat Data"):
                col1,col2,col3 = st.columns([0.1,0.8,0.1])
                with col1:
                    st.write(" ")
                with col2:
                    result = view_all_data()
                    clean_df = pd.DataFrame(result,columns=["Id","Periode","Nilai Variabel","Id Variabel","Id Admin"])
                    st.dataframe(clean_df)
                with col3:
                    st.write(" ")
                
            #buat inputan untuk id
            inputid=st.number_input("Masukan ID Data yang ingin diubah: ",step=1)
            data_result = get_data(inputid)
            if data_result:
                id_data = data_result[0][0]
                bln_tahun = str(data_result[0][1])
                nilai = str(data_result[0][2])
                id_jenis=str(data_result[0][3])
                id_admin=str(data_result[0][4])
                col1,col2,col3 = st.columns([0.1,0.8,0.1])
                with col1:
                     st.write(" ")
                with col2:
                    st.write("Ubah data dengan ID : ",str(id_data))
                    y=datetime.datetime.strptime(bln_tahun, '%Y-%m-%d').date()
                    new_bln_tahun= st.date_input("Periode: ",value=y)
                    new_nilai=st.number_input("Nilai Variabel",value=float(nilai))
                    # new_id_jenis=st.number_input("Jenis Variabel",min_value=1, max_value=4, value=int(id_jenis), step=1)
                    new_id_jenis = st.selectbox(
                            'Nama Variabel:',
                            ('Nilai Inflasi', 'BI Rate', 'Nilai Tukar','Uang Beredar M2'))
                    if new_id_jenis=="Nilai Inflasi":
                         new_id_jenis=1
                    if new_id_jenis=='BI Rate': 
                         new_id_jenis=2
                    if new_id_jenis=='Nilai Tukar':
                         new_id_jenis=3
                    if new_id_jenis=='Uang Beredar M2':
                         new_id_jenis=4
                    new_id_admin=st.number_input("ID Admin",min_value=1,value=int(id_admin), step=1)
                    if st.button("Update Data"):
                        edit_data(id_data,new_bln_tahun,new_nilai,new_id_jenis,new_id_admin)
                        st.success("Berhasil update data")
                        with st.expander("View Updated Data"):
                            result = view_all_data()
                            clean_df = pd.DataFrame(result,columns=["Id","Periode","Nilai Variabel","Id Variabel","Id Admin"])
                            # st.dataframe(clean_df)
                            col1,col2,col3 = st.columns([0.1,0.8,0.1])
                            with col1:
                                st.write(" ")
                            with col2:
                                st.dataframe(clean_df)
                            with col3:
                                st.write(" ")
                with col3:
                    st.write(" ")
                
        elif option=="Hapus Data":
            st.subheader("Hapus Data")
            with st.expander("Lihat Data"):
                col1,col2,col3 = st.columns([0.15,0.7,0.15])
                with col1:
                    st.write(" ")
                with col2:
                    result = view_all_data()
                    clean_df = pd.DataFrame(result,columns=["Id","Periode","Nilai Variabel","Id Variabel","Id Admin"])
                    st.dataframe(clean_df)
                with col3:
                    st.write(" ")

            col1,col2,col3 = st.columns([0.15,0.7,0.15])
            with col1:
                st.write(" ")
            with col2:
                inputid=st.number_input("Masukian ID Data yang ingin dihapus: ",step=1)
                if st.button("Delete"):
                    delete_data(inputid)
                    st.warning("Deleted: '{}'".format(inputid))
                    with st.expander("View Updated Data"):
                        result = view_all_data()
                        clean_df = pd.DataFrame(result,columns=["Id","Periode","Nilai Variabel","Id Variabel","Id Admin"])
                        # st.dataframe(clean_df)
                        col1,col2,col3 = st.columns([0.1,0.8,0.1])
                        with col1:
                            st.write(" ")
                        with col2:
                            st.dataframe(clean_df)
                        with col3:
                            st.write(" ")   
            with col3:
                    st.write(" ")        
            
              
#-----------------------------------------------------
def show_dataset_user():
    st.title(f"Dataset") 
    showDatasetUserAdmin()

#-----------------------------------------------------
# Read dataset
def showDatasetUserAdmin():
    col1,col2,col3=st.columns([0.1,0.8,0.1])
    with col1:
        st.write(" ")
    with col2:
        st.subheader("Keseluruhan Dataset")
        r=tampilDataJoin_Admin()
        rr = pd.DataFrame(r,columns=["Id","Bulan & Tahun","Nilai Variabel","Nama Variabel","Id Admin"])
        st.dataframe(rr)

        pilihDF = st.selectbox(
                    'Pilih Data Variabel:',
                    ('Nilai Inflasi', 'BI Rate', 'Nilai Tukar','Uang Beredar M2'))
        k1,k2,k3=st.columns([0.1,0.8,0.1])
        with k1:
            st.write(" ")
        with k2:
            if pilihDF=="Nilai Inflasi":
                dataInflasi=getDataSendiri1()
                datInflasiDF=pd.DataFrame(dataInflasi,columns=["Nama Variabel","Bulan & Tahun","Nilai Variabel","Id Admin"])
                st.dataframe(datInflasiDF)
            if pilihDF=='BI Rate': 
                dataBI=getDataSendiri2()
                dataBIDF=pd.DataFrame(dataBI,columns=["Nama Variabel","Bulan & Tahun","Nilai Variabel","Id Admin"])
                st.dataframe(dataBIDF)
            if pilihDF=='Nilai Tukar':
                dataInflasi=getDataSendiri3()
                datInflasiDF=pd.DataFrame(dataInflasi,columns=["Nama Variabel","Bulan & Tahun","Nilai Variabel","Id Admin"])
                st.dataframe(datInflasiDF)
            if pilihDF=='Uang Beredar M2':
                dataInflasi=getDataSendiri4()
                datInflasiDF=pd.DataFrame(dataInflasi,columns=["Nama Variabel","Bulan & Tahun","Nilai Variabel","Id Admin"])
                st.dataframe(datInflasiDF)     
        with k3:
            st.write(" ")
    
        
            #Query pivot
            #SELECT bln_tahun, AVG(CASE when id_jenis_var=1 THEN nilai ELSE 0 END )as NilaiInflasi, AVG(CASE when id_jenis_var=2 THEN nilai ELSE 0 END )as bi, AVG(CASE when id_jenis_var=3 THEN nilai ELSE 0 END )as tukar, AVG(CASE when id_jenis_var=4 THEN nilai ELSE 0 END )as beredar FROM tb_dataset GROUP by id_data;
    with col3:
        st.write(" ")  
    # st.write(st.session_state.username)
#-----------------------------------------------------
#Ambil dataset dari DB jadiin Dataframe
def DFInflasi():
    mycursor.execute('SELECT bln_tahun, AVG(CASE when id_jenis_var=1 THEN nilai ELSE null END )as NilaiInflasi FROM tb_dataset GROUP by id_data;')
    data = mycursor.fetchall()
    return data
def DFBIRate():
    mycursor.execute('SELECT bln_tahun, AVG(CASE when id_jenis_var=2 THEN nilai ELSE null END )as BIRate FROM tb_dataset GROUP by id_data;')
    data = mycursor.fetchall()
    return data
def DFNilaiTukar():
    mycursor.execute('SELECT bln_tahun, AVG(CASE when id_jenis_var=3 THEN nilai ELSE null END )as NilaiTukar FROM tb_dataset GROUP by id_data;')
    data = mycursor.fetchall()
    return data
def DFM2():
    mycursor.execute('SELECT bln_tahun, AVG(CASE when id_jenis_var=4 THEN nilai ELSE null END )as M2 FROM tb_dataset GROUP by id_data;')
    data = mycursor.fetchall()
    return data
#-----------------------------------------------------
#Regresi Linier Berganda from scratch
def get_predictions(model, X):
    '''
    Obtain the predictions for the given model and inputs.
    model: np.array of Floats with shape (p,) of parameters
    X: np.array of Floats with shape (n, p-1) of inputs
    Returns: np.array of Floats with shape (n,).
    '''
    (n, p_minus_one) = X.shape
    p = p_minus_one + 1
    new_X = np.ones(shape=(n, p))
    new_X[:, 1:] = X
    return np.dot(new_X, model)

def get_best_model(X, y):
    '''
    Returns the model with the parameters that minimize the MSE.
    X: np.array of Floats with shape (n, p-1) of inputs
    y: np.array of Floats with shape (n,) of observed outputs
    Returns: np.array of shape (p,) representing the model.
    '''
    (n, p_minus_one) = X.shape
    p = p_minus_one + 1
    new_X = np.ones(shape=(n, p))
    new_X[:, 1:] = X
    return np.dot(np.dot(inv(np.dot(new_X.T, new_X)), new_X.T), y)
#-----------------------------------------------------
#Fitur Utama
def fiturPrediksiHistoris(): 
    dataInflasi=DFInflasi()
    datInflasiDF=pd.DataFrame(dataInflasi,columns=["Periode","Nilai Inflasi"])
    datInflasiDF=datInflasiDF.set_index('Periode')        
    datInflasiDF.dropna(inplace=True)
    
    #Penjelasan singkat
    st.write("Prediksi nilai inflasi menggunakan data historis nilai inflasi (time series) dengan data lag dari nilai inflasi sebagai variabel prediktor yang digunakan untuk memprediksi nilai inflasi (variabel target).")
    #Menampilkan dataframe
    col1, col2, col3= st.columns([0.2, 0.6, 0.2])
    with col1:
        st.write(' ')
    with col2:
        st.caption('Visualisasi dataframe')
        st.line_chart(datInflasiDF['Nilai Inflasi'])
        
    with col3:
        st.write(' ')

    col1, col2, col3= st.columns([0.35, 0.3, 0.35])
    with col1:
        st.write(' ')
    with col2:
        st.caption('Isi dataframe')
        datInflasiDF
        
    with col3:
        st.write(' ')

    st.write("Untuk memperoleh variabel independent dari data time series inflasi di atas, dilakukan feature engineering yang mana feature yang digunakan adalah data lag dari data inflasi. Data lag yang digunakan adalah data lag 6, lag 9 dan lag 12. Ketiga lag ini adalah variabel input untuk memprediksi nilai inflasi.")
    
    #feature engineering
    dfHistoris1 = datInflasiDF.copy()
    dfHistoris1['lag_6'] = dfHistoris1['Nilai Inflasi'].shift(6)
    dfHistoris1['lag_9'] = dfHistoris1['Nilai Inflasi'].shift(9)
    dfHistoris1['lag_12'] = dfHistoris1['Nilai Inflasi'].shift(12)

    #Datafram dengan feature
    df_wfeature = dfHistoris1[['lag_12','lag_9','lag_6','Nilai Inflasi']]
    st.write("Berikut dataframe yang diperoleh:")

    col1, col2, col3= st.columns([0.2,0.6,0.2])
    with col1:
        st.write(' ')
    with col2:
        df_wfeature
    with col3:
        st.write(' ')
    
    st.write("Dari dataframe di atas dilakukan penghapusan baris data yang memiliki nilai null, sehingga bentuk dataframe adalah sebagai berikut:")
    #cek nilai null, kemudian hapus
    cek1=df_wfeature.isnull().sum()
    df_wfeature.dropna(inplace=True)
    cek2=df_wfeature.isnull().sum()
    col1, col2, col3= st.columns([0.2,0.6,0.2])
    with col1:
        st.write(' ')
    with col2:
        df_wfeature
    with col3:
        st.write(' ')

    #Penjelasan buat Model Regresi
    st.write("Langkah selanjutnya adalah membuat model regresi linier berganda. Sebelumnya variabel prediktor dan target telah didefinisikan yaitu nilai lag 6, lag 9 dan lag 12 sebagai variabel prediktor dan nilai inflasi sebagai variabel target. Dataframe kemudian dibagi dua untuk data training 50% dan data testing 50%. Dari data training dilakukan fit model untuk memperoleh model regresi linier berganda.")
    
    #ekstrasi fitur x (variabel independen/prediktor/input) dan y (variabel dependen/target/output)
    y = df_wfeature["Nilai Inflasi"]
    X = df_wfeature.drop(['Nilai Inflasi'], axis=1)

    #split data training (untuk memperoleh model), testing (untuk uji model)
    import matplotlib.pyplot as plt
    train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.50, random_state=0, shuffle=False)
    
    #Perolehan Model dari scratch:
    from numpy.linalg import inv
    #Buat dataframe untuk nampilin hasil prediksi model data training
    dfPrediction = pd.DataFrame({'Lag 12': train_X['lag_12'],
                                'Lag 9': train_X['lag_9'],
                              'Lag 6': train_X['lag_6'],
                               'Nilai Inflasi': train_y})
    #Dapatin best model
    best_model = get_best_model(train_X, train_y) #model terbaik
    dfPrediction['Prediksi Data Training'] = get_predictions(best_model, train_X) #prediksi dgn model terbaik
    
    #Buat dataframe untuk nampilin hasil prediksi model data testing
    dfPredictionTest = pd.DataFrame({'Lag 12': test_X['lag_12'],
                                'Lag 9': test_X['lag_9'],
                              'Lag 6': test_X['lag_6'],
                               'Nilai Inflasi': test_y})
    dfPredictionTest['Prediksi Data Testing'] = get_predictions(best_model, test_X) #prediksi dgn model terbaik
    
    #Tampilin Bentukan model regresinya:
    #Cara ekstrasi intercept dan koef
    #karna dia array harus diekstrasi satu satu
    #Belum sempurna, harus dicek lagi koef sama interceptny
    intercept=best_model[0]
    x1koef=best_model[1]
    x2koef=best_model[2]
    x3koef=best_model[3]
    #Intercept sama koef terakhir keknya kebalik, cek hitung manual
    st.write(' Dari hasil fit data traning, diperoleh model regresi linier berganda sebagai berikut:')
    st.write("y = ",str(intercept),
             "+ (",str(x1koef),
             " * x1 ) +",
             " (",str(x2koef),
             " * x2 ) +",
             " (",str(x3koef),
             " * x3 )"
             )
    
    #Ini tinggal copy paste antar fitur
    #------------------------------------------
    #dfPrediction #Dataframe Trainning yang ada hasilnya
    hasil_y_train=dfPrediction["Prediksi Data Training"]
    hasil_y_test=dfPredictionTest["Prediksi Data Testing"]
    # uji data Terhadap data training dan data testing
    st.write("Dari model yang diperoleh dilakukan uji model untuk melihat performa model pada data training dan data testing." )
    col1, col2= st.columns(2)
    with col1:
        st.header("Performa Model data Training")
        dfPrediction
        mseTraining=sm.mean_squared_error(train_y, hasil_y_train)
        rmseTraining=math.sqrt(mseTraining)
        st.write("Nilai MSE= ",str(round(mseTraining, 4))) #round(sm.mean_squared_error(train_y, ujitrain_y), 2)
        st.write("Nilai RMSE= ",str(round(rmseTraining,4))) #round(sm.mean_squared_error(train_y, ujitrain_y), 2)
        st.write(f"Dilihat dari nilai RMSE yang diperoleh, dapat diartikan bahwa model memprediksi nilai inflasi dengan nilai eror antara data asli dengan hasil prediksi sebesar {str(round(rmseTraining,4))}")
        chart_data=pd.DataFrame({
            'Nilai Inflasi': train_y,
            'Hasil Prediksi':hasil_y_train}
        )
        st.line_chart(chart_data,x=id)     
    with col2:
        st.header("Performa Model data Testing")
        dfPredictionTest
        # mseTraining=sm.mean_squared_error(train_y, hasil_y_train)
        # rmseTraining=math.sqrt(mseTraining)
        # st.write("Nilai MSE= ",str(round(mseTraining, 4))) #round(sm.mean_squared_error(train_y, ujitrain_y), 2)
        # st.write("Nilai RMSE= ",str(round(rmseTraining,4))) #round(sm.mean_squared_error(train_y, ujitrain_y), 2)
        # st.write(f"Dilihat dari nilai RMSE yang diperoleh, dapat diartikan bahwa model memprediksi nilai inflasi dengan nilai eror antara data asli dengan hasil prediksi sebesar {str(round(rmseTraining,4))}")
        mseTesting=sm.mean_squared_error(test_y, hasil_y_test)
        rmseTesting=math.sqrt(mseTesting)
        st.write("Nilai MSE= ",str(round(mseTesting, 4))) #round(sm.mean_squared_error(train_y, ujitrain_y), 2)
        st.write("Nilai RMSE= ",str(round(rmseTesting, 4))) #round(sm.mean_squared_error(train_y, ujitrain_y), 2)
        st.write(f"Dilihat dari nilai RMSE yang diperoleh, dapat diartikan bahwa model memprediksi nilai inflasi dengan nilai eror antara data asli dengan hasil prediksi sebesar {str(round(rmseTesting,4))}")
        chart_data=pd.DataFrame({
            'Nilai Inflasi': test_y,
            'Hasil Prediksi':hasil_y_test}
        )
        st.line_chart(chart_data,x=id)
    
    st.header("Prediksi data baru")
    st.write("Model yang telah diperoleh dapat digunakan untuk memprediksi data inflasi bulanan selanjutnya")
    
    kol1,kol2,kol3=st.columns([0.2,0.6,0.2])
    with kol1:
        st.write(" ")
    with kol2:
        bulan=st.number_input("Masukan jumlah bulan untuk proyeksi nilai inflasi berikutnya:",step=1)
        dfbru = datInflasiDF.iloc[-12:]
        kolominflasi=dfbru["Nilai Inflasi"]
        arrayInflasi=kolominflasi.to_numpy()
        if st.button("Prediksi Nilai Inflasi"):
            for i in range(bulan):
                with st.container():
                    #prediksi data baru 12 bulan kedepan (run blok kode sebanyak bulan yang ingin diprediksi)
                    reverseArrayInflasi = arrayInflasi[::-1]
                    listInflasi = reverseArrayInflasi.tolist()
                    dataquartil=[listInflasi[5],listInflasi[8],listInflasi[11]]
                    def persamaanRegresi(x1,x2,x3):
                        y = intercept + (x1koef*x1) + (x2koef*x2) + (x3koef*x3)
                        return round(y,2)
                    hasil= persamaanRegresi(dataquartil[2],dataquartil[1],dataquartil[0])
                    arrayInflasi = np.append(arrayInflasi, hasil)
            hasilforecast=arrayInflasi[11:]
            date = np.array('2023-03', dtype=np.datetime64)
            s=date + np.arange(hasilforecast.size)   
            chartHasil=pd.DataFrame({
                'Periode':s,
                'Hasil Prediksi':hasilforecast}) 
            # chartHasil=chartHasil.set_index('Periode')
            st.line_chart(chartHasil,x='Periode') 
            dd= chartHasil['Periode'].astype(str)
            tblHasil=pd.DataFrame({
                'Periode':dd,
                'Hasil Prediksi':hasilforecast})
            tblHasil = tblHasil.drop(0)
            col1,col2,col3=st.columns([0.2,0.6,0.2])
            with col1:
                st.write(" ")
            with col2:
                tblHasil
            with col3:
                st.write(" ")
    with kol3:
        st.write(" ")  

def fiturPrediksiFEkonomi():
    
    dataInflasi=DFInflasi()
    datInflasiDF=pd.DataFrame(dataInflasi,columns=["Periode","Nilai Inflasi"])
    datInflasiDF=datInflasiDF.set_index('Periode')        
    datInflasiDF.dropna(inplace=True)
    dataBIrate=DFBIRate()
    BIRateDF=pd.DataFrame(dataBIrate,columns=["Periode","BI Rate"])
    BIRateDF=BIRateDF.set_index('Periode')
    BIRateDF.dropna(inplace=True)
    dataNilaiTukar=DFNilaiTukar()
    nilaiTukarDF=pd.DataFrame(dataNilaiTukar,columns=["Periode","Nilai Tukar"])
    nilaiTukarDF=nilaiTukarDF.set_index('Periode')
    nilaiTukarDF.dropna(inplace=True)   
    dataM2=DFM2()
    m2DF=pd.DataFrame(dataM2,columns=["Periode","Uang Beredar"])    
    m2DF=m2DF.set_index('Periode')    
    m2DF.dropna(inplace=True)    
    dfEkonomi=pd.concat([datInflasiDF, BIRateDF,nilaiTukarDF,m2DF], axis=1)
  
    st.write("Prediksi Nilai Inflasi menggunakan nilai faktor ekonomi sebagai variabel independent (prediktor) dengan faktor-faktor ekonomi tersebut yaitu: Nilai BI Rate, \n Nilai Tukar Rupiah terhadap Dolar Amerika, dan Jumlah Uang Beredar (M2).")
    #Menampilkan dataframe
    col1, col2, col3= st.columns([0.2, 0.6, 0.2])
    with col1:
        st.write(' ')
    with col2:
        st.caption('Dataframe')
        dfEkonomi
    with col3:
        st.write(' ')
    
    #Visualisasi DataFrame
    st.write("Berikut visualisasi dari masing masing variabel:")
    col1, col2, col3,col4= st.columns(4)
    with col1:
        st.line_chart(dfEkonomi['BI Rate'],height=250)
    with col2:
        st.line_chart(dfEkonomi['Nilai Tukar'],height=250)
    with col3:
        st.line_chart(dfEkonomi['Uang Beredar'],height=250)
    with col4:
        st.line_chart(dfEkonomi['Nilai Inflasi'],height=250)

    #Penjelasan buat Model Regresi
    st.write("Untuk membuat model regresi linier berganda, variabel target beserta variabel prediktor terlebih dahulu didefinisikan yaitu nilai inflasi sebagai variabel target dengan 3 faktor ekonomi berupa bi rate, nilai tukar, dan jumlah uang beredar sebagai variabel prediktor. Dataframe kemudian dibagi dua untuk data training dan testing dengan perbandingan 90:10. Data training digunakan untuk fit model, dan data testing digunakan untuk menguji model yang diperoleh.")
    
    #ekstrasi fitur x (variabel independen/prediktor/input) dan y (variabel dependen/target/output)
    x = dfEkonomi[['BI Rate','Nilai Tukar','Uang Beredar']]
    y = dfEkonomi['Nilai Inflasi']
    
    #split data training (untuk memperoleh model), testing (untuk uji model)
    import matplotlib.pyplot as plt
    train_X, test_X, train_y, test_y = train_test_split(x, y, test_size = 0.10,random_state=10)

    #Perolehan Model dari scratch:
    from numpy.linalg import inv
    
    #Buat dataframe untuk nampilin hasil prediksi model data training
    dfPrediction = pd.DataFrame({'BI Rate': train_X['BI Rate'],
                              'Nilai Tukar': train_X['Nilai Tukar'],
                               'Uang Beredar': train_X['Uang Beredar'],
                               'Nilai Inflasi': train_y})
    #Dapatin best model
    best_model = get_best_model(train_X, train_y) #model terbaik
    dfPrediction['Prediksi Data Training'] = get_predictions(best_model, train_X) #prediksi dgn model terbaik
    
    #Buat dataframe untuk nampilin hasil prediksi model data testing
    dfPredictionTest = pd.DataFrame({'BI Rate': test_X['BI Rate'],
                              'Nilai Tukar': test_X['Nilai Tukar'],
                               'Uang Beredar': test_X['Uang Beredar'],
                               'Nilai Inflasi': test_y})
    dfPredictionTest['Prediksi Data Testing'] = get_predictions(best_model, test_X) #prediksi dgn model terbaik
    #Tampilin Bentukan model regresinya:
    #Cara ekstrasi intercept dan koef
    #karna dia array harus diekstrasi satu satu
    #Belum sempurna, harus dicek lagi koef sama interceptny
    intercept=best_model[0]
    x1koef=best_model[1]
    x2koef=best_model[2]
    x3koef=best_model[3]
    #Intercept sama koef terakhir keknya kebalik, cek hitung manual
    st.write('Setelah dilakukan fit model pada data training, model regresi linier berganda yang diperoleh adalah sebagai berikut:')
    st.write("y = ",str(intercept),
             "+ (",str(x1koef),
             " * x1 ) +",
             " (",str(x2koef),
             " * x2 ) +",
             " (",str(x3koef),
             " * x3 )"
             )
    #dfPrediction #Dataframe Trainning yang ada hasilnya
    hasil_y_train=dfPrediction["Prediksi Data Training"]
    hasil_y_test=dfPredictionTest["Prediksi Data Testing"]
    # uji data Terhadap data training dan data testing
    st.write("Dari model tersebut dilakukan pengujian untuk melihat performa model pada data training dan data testing" )
    col1, col2= st.columns(2)
    with col1:
        st.header("Performa Model data Training")
        dfPrediction
        mseTraining=sm.mean_squared_error(train_y, hasil_y_train)
        rmseTraining=math.sqrt(mseTraining)
        st.write("Nilai MSE= ",str(round(mseTraining, 4))) #round(sm.mean_squared_error(train_y, ujitrain_y), 2)
        st.write("Nilai RMSE= ",str(round(rmseTraining,4))) #round(sm.mean_squared_error(train_y, ujitrain_y), 2)
        st.write(f"Dilihat dari nilai RMSE yang diperoleh, dapat diartikan bahwa model memprediksi nilai inflasi dengan nilai eror antara data asli dengan hasil prediksi sebesar {str(round(rmseTraining,4))}")
        
        # st.write("Nilai MSE= ",str(round(sm.mean_squared_error(train_y, hasil_y_train), 4))) #round(sm.mean_squared_error(train_y, ujitrain_y), 2)    
    with col2:
        st.header("Performa Model data Testing")
        dfPredictionTest
        mseTesting=sm.mean_squared_error(test_y, hasil_y_test)
        rmseTesting=math.sqrt(mseTesting)
        st.write("Nilai MSE= ",str(round(mseTesting, 4))) #round(sm.mean_squared_error(train_y, ujitrain_y), 2)
        st.write("Nilai RMSE= ",str(round(rmseTesting, 4))) #round(sm.mean_squared_error(train_y, ujitrain_y), 2)
        st.write(f"Dilihat dari nilai RMSE yang diperoleh, dapat diartikan bahwa model memprediksi nilai inflasi dengan nilai eror antara data asli dengan hasil prediksi sebesar {str(round(rmseTesting,4))}")
        
        # st.write("Nilai MSE= ",str(round(sm.mean_squared_error(test_y, hasil_y_test), 4))) #round(sm.mean_squared_error(train_y, ujitrain_y), 2)
         
    
    #Model untuk prediksi
    def persamaanRegresi(x1,x2,x3):
        #Manggil konstanta
        y = intercept + (x1koef*x1) + (x2koef*x2) + (x3koef*x3)
        return round(y,2)
    
    #Form Prediksi
    st.write("Dari model regresi yang diperoleh, nilai inflasi dapat diprediksi dengan memasukan nilai BI Rate, Nilai Tukar dan Jumlah Uang beredar.")
    st.header("Prediksi nilai Inflasi")
    st.write('Masukan nilai:')
    kol1, kol2,kol3=st.columns([0.1,0.8,0.1])
    with kol1:
        st.header("")
    with kol2:
        bi_rate=st.number_input("BI Rate")
        nilai_tukar=st.number_input("Nilai Tukar")
        uang_beredar=st.number_input("Jumlah Uang Beredar (M2)")
        if st.button("Prediksi"):
            hasilPrediksi=persamaanRegresi(bi_rate,nilai_tukar,uang_beredar)
            st.write("Hasil Prediksi: ",str(hasilPrediksi))
    with kol3:
        st.header("")
#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------
#Sidebar Menu
EXAMPLE_NO = 1
def streamlit_menu(example=1):
    if example == 1:
        # 1. as sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title="Sistem Prediksi Inflasi",  # required
                options=["Prediksi Inflasi: Data Historis", "Prediksi Inflasi: Faktor Ekonomi", "Dataset","Admin"],  # required
                icons=["graph-up", "graph-up", "table","person"],  # optional
                menu_icon="none",  # optional
                default_index=0,  # optional
            )
        return selected
selected = streamlit_menu(example=EXAMPLE_NO)
if selected == "Prediksi Inflasi: Data Historis":
    st.title(f"Prediksi Inflasi Berdasarkan Data Historis Inflasi")
    fiturPrediksiHistoris()
if selected == "Prediksi Inflasi: Faktor Ekonomi":
    st.title(f"Prediksi Inflasi Berdasarkan Nilai Faktor Ekonomi")
    fiturPrediksiFEkonomi()
if selected == "Dataset":
    if st.session_state['loggedIn']==True:
        show_dataset_admin()        
    else:
        show_dataset_user()
if selected == "Admin":
    #jika session state loggedin masih false ->show login page
    if st.session_state['loggedIn'] == False:
        show_login_page()
    else:
        if st.session_state['loggedIn']==True:
            show_admin_page()
        else:
            show_login_page()






