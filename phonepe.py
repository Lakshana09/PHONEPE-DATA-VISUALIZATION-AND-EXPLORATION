import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import mysql.connector
import requests
import json
from PIL import Image

#Dataframe creation
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3306",
    database="phonepe",
    password="Luxpapa@09"
)
cursor = mydb.cursor()

#Agg_insurance_df
cursor.execute("SELECT * FROM aggregated_insurance")
table1 = cursor.fetchall()
mydb.commit()

Agg_insurance = pd.DataFrame(table1, columns=("States","Years", "Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#Agg_Transaction

cursor.execute("SELECT * FROM agg_transaction")
table2 = cursor.fetchall()
mydb.commit()

Agg_Transaction = pd.DataFrame(table2, columns=("States","Years", "Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#Agg_User

cursor.execute("SELECT * FROM agg_user")
table3 = cursor.fetchall()
mydb.commit()

Agg_user = pd.DataFrame(table3, columns=("States","Years", "Quarter","Brands","Transaction_count","Percentage"))

#Map_insurance
cursor.execute("SELECT * FROM map_insurance")
table4 = cursor.fetchall()
mydb.commit()

Map_insurance = pd.DataFrame(table4, columns=("States","Years", "Quarter","Districts","Transaction_count","Transaction_amount"))

#Map_transaction
cursor.execute("SELECT * FROM map_transaction")
table5 = cursor.fetchall()
mydb.commit()

Map_Transaction = pd.DataFrame(table5, columns=("States","Years", "Quarter","Districts","Transaction_count","Transaction_amount"))

#Map_user

cursor.execute("SELECT * FROM map_user")
table6 = cursor.fetchall()
mydb.commit()

Map_user = pd.DataFrame(table6, columns=("States","Years", "Quarter","Districts","RegisteredUser","AppOpens"))

#top_insurance
cursor.execute("SELECT * FROM top_insurance")
table7 = cursor.fetchall()
mydb.commit()

Top_insurance = pd.DataFrame(table7, columns=("States","Years", "Quarter","Pincodes","Transaction_count","Transaction_amount"))

#top_transcation
cursor.execute("SELECT * FROM top_transaction")
table8 = cursor.fetchall()
mydb.commit()

Top_Transaction = pd.DataFrame(table8, columns=("States","Years", "Quarter","Pincodes","Transaction_count","Transaction_amount"))

#top_user

cursor.execute("SELECT * FROM top_user ")
table9 = cursor.fetchall()
mydb.commit()

Top_user = pd.DataFrame(table9, columns=("States","Years", "Quarter","Pincodes","RegisteredUser"))

#Function for Agg insurance

def Transaction_amount_count_Y(df, year):

    Agg = df[df["Years"] == year]
    Agg.reset_index(drop = True, inplace=True)
    Aggin = Agg.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    Aggin.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(Aggin, x="States", y ="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_amount)
        
    with col2:

        fig_Count = px.bar(Aggin, x="States", y ="Transaction_count", title=f"{year} TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
        st.plotly_chart(fig_Count)
    

    col1,col2 =  st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()
        fig_india_1 = px.choropleth(Aggin, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                    range_color=(Aggin["Transaction_amount"].min(), Aggin["Transaction_amount"].max()),hover_name= "States", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations",height=650, width=600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
        
    with col2:

        fig_india_2 = px.choropleth(Aggin, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",color= "Transaction_count", color_continuous_scale= "Rainbow",
                                    range_color=(Aggin["Transaction_count"].min(), Aggin["Transaction_count"].max()),hover_name= "States", title= f"{year} TRANSACTION COUNT", fitbounds= "locations",height=650, width=600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return Agg


def Transaction_amount_count_Y_Q(df, quarter):
    Agg = df[df["Quarter"] == quarter]
    Agg.reset_index(drop = True, inplace=True)
    Aggin = Agg.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    Aggin.reset_index(inplace=True)
    
    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(Aggin, x="States", y ="Transaction_amount", title=f"{Agg['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650, width=600)
        st.plotly_chart(fig_amount)
    with col2:
        fig_Count = px.bar(Aggin, x="States", y ="Transaction_count", title=f"{Agg['Years'].min()} YEAR {quarter} QUARTER  TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600)
        st.plotly_chart(fig_Count)
    
    col1,col2 = st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(Aggin, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                    range_color=(Aggin["Transaction_amount"].min(), Aggin["Transaction_amount"].max()),hover_name= "States", title= f"{Agg['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations",height=650, width=600)
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2 = px.choropleth(Aggin, geojson=data1, locations= "States", featureidkey= "properties.ST_NM",color= "Transaction_count", color_continuous_scale= "Rainbow",
                                    range_color=(Aggin["Transaction_count"].min(), Aggin["Transaction_count"].max()),hover_name= "States", title= f"{Agg['Years'].min()} YEAR {quarter} QUARTER  TRANSACTION COUNT", fitbounds= "locations",height=650, width=600)
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return Agg

def Agg_Tran_Transaction_Type(df, state):

    Agg = df[df["States"] == state]
    Agg.reset_index(drop = True, inplace=True)
    Aggin = Agg.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    Aggin.reset_index(inplace=True)
    
    col1,col2 = st.columns(2)
    with col1:
        fig_pie_1 = px.pie(data_frame= Aggin, names= "Transaction_type", values="Transaction_amount", width= 600, title=f"{state.upper()} TRANSACTION AMOUNT", hole =0.5)
        st.plotly_chart(fig_pie_1)
    
    with col2:
        fig_pie_2 = px.pie(data_frame= Aggin, names= "Transaction_type", values="Transaction_count", width= 600, title=f"{state.upper()} TRANSACTION COUNT", hole =0.5)
        st.plotly_chart(fig_pie_2)

#Agg user
def Agg_user_plot_1(df, year):
    Aguy = df[df["Years"] == 2022]
    Aguy.reset_index(drop = True, inplace=True)
    Aguyg = Aguy.groupby("Brands")[["Transaction_count","Percentage"]].sum()
    Aguyg.reset_index(inplace=True)

    fig_bar_1 = px.bar(Aguyg, x="Brands", y= "Transaction_count", title="BRANDS AND TRANSACTION COUNT",width = 800, color_discrete_sequence= px.colors.sequential.haline)
    st.plotly_chart(fig_bar_1)

    return Aguy   

#Agg user quarter
def Agg_user_plot_2(df, quarter):
    Aguyq = Agg_user[Agg_user["Quarter"] == quarter]
    Aguyq.reset_index(drop = True, inplace=True)
    Aguyqg = Aguyq.groupby("Brands")[["Transaction_count","Percentage"]].sum()
    Aguyqg.reset_index(inplace=True)

    fig_bar_1 = px.bar(Aguyqg, x="Brands", y= "Transaction_count", title="BRANDS AND TRANSACTION COUNT",width = 800, color_discrete_sequence= px.colors.sequential.haline)
    st.plotly_chart(fig_bar_1)

    return Aguyq

def Agg_user_plot_3(df, state):
    Auyqs= df[df["States"] == state] 
    Auyqs.reset_index(drop=  True,inplace= True)

    fig_line_1= px.line(Auyqs, x="Brands", y="Transaction_count",hover_data= "Percentage",title=" BRANDS, TRANSACTIONCO COUNT, PERCENTAGE",width=1000)
    st.plotly_chart(fig_line_1)

#Map tranction  for Agg
def Map_insurance_Districts(df, state):
    Agg = df[df["States"] == state]
    Agg.reset_index(drop = True, inplace=True)
    Aggin = Agg.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    Aggin.reset_index(inplace=True)
    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar( Aggin, x ="Transaction_amount",y= "Districts",orientation= "h",height=600, title=f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2 = px.bar( Aggin,  x ="Transaction_count",y= "Districts",orientation= "h",height=600, title=f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)

def Map_user_Y(df, year):
    muy = df[df["Years"] == year]
    muy.reset_index(drop = True, inplace=True)
    muyg = muy.groupby("States")[["RegisteredUser","AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_bar_1 = px.line(muyg, x="States", y= ["RegisteredUser", "AppOpens"],title=f"{year} REGISTEREDUSER,  APPOPENS",width = 1000,height = 800, markers=  True)
    st.plotly_chart(fig_bar_1)

    return muy

#Map_user
def Map_user_Y_Q(df, quarter):
    muyq = df[df["Quarter"] == quarter]
    muyq.reset_index(drop = True, inplace=True)
    muyqg = muyq.groupby("States")[["RegisteredUser","AppOpens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_bar_1 = px.line(muyqg, x="States", y= ["RegisteredUser", "AppOpens"],title=f"{df['Years'].min()} YEARS {quarter} REGISTEREDUSER,  APPOPENS",width = 1000,height = 800, markers=  True)
    st.plotly_chart(fig_bar_1)

    return muyq

#Map_user_S
def Map_user_Y_Q_S(df, states):
    muyqs = df[df["States"] == states]
    muyqs.reset_index(drop = True, inplace=True)
    col1,col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(muyqs, x="RegisteredUser", y= "Districts",orientation= "h",title=f"{states.upper()} REGISTEREDUSER",height = 800)
        st.plotly_chart(fig_bar_1)
    with col2:
        fig_bar_2 = px.bar(muyqs, x="RegisteredUser", y= "Districts",orientation= "h",title=f"{states.upper()} APPOPENS",height = 800)
        st.plotly_chart(fig_bar_2)


#Top_insurance
def Top_Insur_plot_1(df, state):
    tiy = df[df["States"] == state]
    tiy.reset_index(drop = True, inplace=True)
    col1,col2 = st.columns(2)
    with col1:
        fig_ti_bar_1 = px.bar(tiy, x="Quarter", y= "Transaction_amount",orientation= "v", hover_data= "Pincodes",  title=" TRANSACTION AMOUNT",height = 800, color_discrete_sequence=px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_ti_bar_1)
    with col2:
        fig_ti_bar_2 = px.bar(tiy, x="Quarter", y= "Transaction_count",orientation= "v", hover_data= "Pincodes",  title=" TRANSACTION COUNT",height = 800,width=600, color_discrete_sequence=px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_ti_bar_2)

def top_user_1(df,year):
    tuy = df[df["Years"] == year]
    tuy.reset_index(drop = True, inplace=True)
    tuyg = pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUser"].sum())
    tuyg.reset_index(inplace=True)

    fig_top_user_1 = px.bar(tuyg,x= "States", y="RegisteredUser",hover_name="States",color="Quarter",width=1000,height =800 ,color_discrete_sequence=px.colors.sequential.Burgyl_r,title=f"{year} REGISTEREDUSERS")
    st.plotly_chart(fig_top_user_1)

    return tuy

def top_user_2(df,state):
    tuy = df[df["States"] == state]
    tuy.reset_index(drop = True, inplace=True)
    
    fig_top_user_2 = px.bar(tuy,x= "Quarter", y="RegisteredUser",hover_name="Pincodes",color="RegisteredUser",width=1000,height =800 ,color_continuous_scale= px.colors.sequential.Magenta,title=" REGISTEREDUSERS,PINCODES,QUARTERS")
    st.plotly_chart(fig_top_user_2)

#sql connection
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        database="phonepe",
        password="Luxpapa@09"
    )
cursor = mydb.cursor()


#sql_Connection
def Top_chart_1():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        database="phonepe",
        password="Luxpapa@09"
    )
    cursor = mydb.cursor()

    query_1= '''select States as STATES, sum(Transaction_amount) as TRANSACTION_AMOUNT From aggregated_insurance
                group by States
                Order by TRANSACTION_AMOUNT DESC
                limit 10'''
    cursor.execute(query_1)
    table1=cursor.fetchall()
    mydb.commit()

    df1=pd.DataFrame(table1,columns=("States","Transaction_amount"))
    fig_amount1 = px.bar(df1, x="States", y ="Transaction_amount", title="TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650, width=600)
    st.plotly_chart(fig_amount1)

    query_2= '''select States as STATES, sum(Transaction_amount) as TRANSACTION_AMOUNT From aggregated_insurance
                group by States
                Order by TRANSACTION_AMOUNT ASC
                limit 10'''
    cursor.execute(query_2)
    table2=cursor.fetchall()
    mydb.commit()

    df2=pd.DataFrame(table2,columns=("States","Transaction_amount"))

    fig_amount2 = px.bar(df2, x="States", y ="Transaction_amount", title="TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height=650, width=600)
    st.plotly_chart(fig_amount2)

    query_3= '''select States as STATES, Avg(Transaction_amount) as TRANSACTION_AMOUNT From aggregated_insurance
                group by States
                Order by TRANSACTION_AMOUNT
                '''
    cursor.execute(query_3)
    table3=cursor.fetchall()
    mydb.commit()

    df3=pd.DataFrame(table3,columns=("States","Transaction_amount"))
    fig_amount3 = px.bar(df3, x="States", y ="Transaction_amount", title="TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Bluered_r,height=650, width=600)
    st.plotly_chart(fig_amount3)

def ques2():
    lt= Agg_Transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= Map_Transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd) 

def ques4():
    htd= Map_Transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)

def ques5():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Agg_Transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Agg_Transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Agg_Transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= Map_Transaction[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)

    

#streamlit part

st.set_page_config(layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
with st.sidebar:
     Select = option_menu("MAIN MENU",["HOME", "DATA EXPLORATION", "TOP CHARTS"])

if Select == "HOME":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("   **-> Credit & Debit card linking**")
        st.write("   **-> Bank Balance check**")
        st.write("   **->Money Storage**")
        st.write("   **->PIN Authorization**")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

    with col2:
        st.image((r"C:\Users\DELL\Documents\Python\phonepe\th-2764620100.jpeg"),width=600)

    col3,col4= st.columns(2)
    
    with col3:
        st.image(r"C:\Users\DELL\Documents\Python\phonepe\phonepe3.jpeg")

    with col4:
        st.write("**-> Easy Transactions**")
        st.write("**-> One App For All Your Payments**")
        st.write("**-> Your Bank Account Is All You Need**")
        st.write("**-> Multiple Ways To Pay**")
        st.write("**-> 1.Direct Transfer & More**")
        st.write("**-> 2.QR Code**")

    col5,col6= st.columns(2)

    with col5:
        st.write("**-> Multiple Payment Modes**")
        st.write("**-> PhonePe Merchants**")
        st.write("**-> Earn Great Rewards**")
        st.write("**->No Wallet Top-Up Required**")
        st.write("**->Pay Directly From Any Bank To Any Bank A/C**")
        st.write("**->Instantly & Free**")

    with col6:
        st.image(r"C:\Users\DELL\Documents\Python\phonepe\phonepe2.jpeg") 

elif Select == "DATA EXPLORATION":
     
    tab1, tab2, tab3 = st.tabs(["**Aggregated Analysis**", "**Map Analysis**", "**Top Analysis**"])

    with tab1:

        method = st.radio("**SELECT THE METHOD**",{"Agg Insurance","Agg Transaction","Agg User"})

        if method == "Agg Insurance":

            col1,col2 = st.columns(2)
            with col1:
                years=st.slider("**SELECT THE YEAR AI**",Agg_insurance["Years"].min(),Agg_insurance["Years"].max(),Agg_insurance["Years"].min())
            tac_Y = Transaction_amount_count_Y(Agg_insurance, years)

            col1,col2 = st.columns(2)
            with col1:

                quarter=st.slider("**SELECT THE QUARTER AI**",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarter)

        elif method == "Agg Transaction":
            col1,col2 = st.columns(2)
            with col1:
                years=st.slider("**SELECT THE YEAR TY**",Agg_Transaction["Years"].min(),Agg_Transaction["Years"].max(),Agg_Transaction["Years"].min())
            Agg_Tran_tac_Y = Transaction_amount_count_Y(Agg_Transaction, years)

            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox ("**SELECT THE STATES TY**", Agg_Tran_tac_Y["States"].unique())
            
            Agg_Tran_Transaction_Type(Agg_Tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:

                quarter=st.slider("**SELECT THE QUARTER TY**",Agg_Tran_tac_Y["Quarter"].min(),Agg_Tran_tac_Y["Quarter"].max(),Agg_Tran_tac_Y["Quarter"].min())
        
            Agg_Tran_tac_Y_Q= Transaction_amount_count_Y_Q(Agg_Tran_tac_Y, quarter)

            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox ("**SELECT THE STATES TY1**", Agg_Tran_tac_Y_Q["States"].unique())

            Agg_Tran_Transaction_Type(Agg_Tran_tac_Y_Q, states)




        elif method =="Agg User":
            col1,col2 = st.columns(2)
            with col1:
                years=st.slider("**SELECT THE YEAR AU**",Agg_user["Years"].min(),Agg_user["Years"].max(),Agg_user["Years"].min())
            Agg_user_Y = Agg_user_plot_1(Agg_user, years)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.selectbox("**SELECT THE QUARTER AU**", Agg_user["Quarter"].unique())
            Agg_user_y_Q =  Agg_user_plot_2(Agg_user_Y, quarters)

            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox ("**SELECT THE STATES AU**", Agg_user_y_Q["States"].unique())
            
            Agg_user_plot_3(Agg_user_y_Q, states)


            

    with tab2:

        method_2 = st.radio("Select The Method",{"Map Insurance","Map Transaction","Map User"})

        if method_2== "Map Insurance":
            col1,col2 = st.columns(2)
            with col1:
                years=st.slider("**SELECT THE YEAR MI**",Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min())
            Map_insurance_tac_Y = Transaction_amount_count_Y(Map_insurance, years)

            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox ("**SELECT THE STATES MI**", Map_insurance_tac_Y["States"].unique(), key="states_select")
            
            Map_insurance_Districts(Map_insurance_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarter=st.slider("**SELECT THE QUARTER MI**",Map_insurance_tac_Y ["Quarter"].min(),Map_insurance_tac_Y ["Quarter"].max(),Map_insurance_tac_Y ["Quarter"].min())
            
            Map_insurance_Y_Q= Transaction_amount_count_Y_Q(Map_insurance_tac_Y, quarter)

            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox ("**SELECT THE STATES MI**",Map_insurance_Y_Q ["States"].unique())

            Map_insurance_Districts(Map_insurance_Y_Q , states)

        elif method_2 == "Map Transaction":
            col1,col2 = st.columns(2)
            with col1:
                years=st.slider("**SELECT THE YEAR MT**",Map_Transaction["Years"].min(),Map_Transaction["Years"].max(),Map_Transaction["Years"].min())
            Map_Tran_tac_Y = Transaction_amount_count_Y(Map_Transaction, years)

            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox ("**SELECT THE STATES MT**", Map_Tran_tac_Y["States"].unique(), key="states_select")
            
            Map_insurance_Districts(Map_Tran_tac_Y, states)

            col1,col2 = st.columns(2)
            with col1:
                quarter=st.slider("**SELECT THE QUARTER MT**",Map_Tran_tac_Y["Quarter"].min(),Map_Tran_tac_Y ["Quarter"].max(),Map_Tran_tac_Y ["Quarter"].min())
            
            Map_Tran_Y_Q= Transaction_amount_count_Y_Q(Map_Tran_tac_Y, quarter)

            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox ("**SELECT THE STATES MT**",Map_Tran_Y_Q["States"].unique())

            Map_insurance_Districts(Map_Tran_Y_Q , states)

        elif method_2 =="Map User":
            col1,col2 = st.columns(2)
            with col1:
                years=st.slider("**SELECT THE YEAR MU**",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            Map_user_1 = Map_user_Y(Map_user, years)

            col1,col2 = st.columns(2)
            with col1:
                quarter=st.slider("**SELECT THE QUARTER MU**",Map_user_1["Quarter"].min(),Map_user_1 ["Quarter"].max(),Map_user_1 ["Quarter"].min())
            
            Map_User_2= Map_user_Y_Q(Map_user_1, quarter)

            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox ("**SELECT THE STATES MU**",Map_User_2["States"].unique())

            Map_user_Y_Q_S(Map_User_2 , states)



    with tab3:

        method_3 = st.radio("Select The Method",{"Top Insurance","Top Transaction","Top User"})

        if method_3 == "Top Insurance":
            col1,col2 = st.columns(2)
            with col1:
                years=st.slider("**SELECT THE YEAR TI**",Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
            Top_insurance_tac_Y = Transaction_amount_count_Y(Top_insurance, years)

            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox ("**SELECT THE STATES TI**",Top_insurance_tac_Y["States"].unique())
            Top_Insur_plot_1(Top_insurance_tac_Y , states)

            col1,col2 = st.columns(2)
            with col1:
                quarter=st.slider("**SELECT THE QUARTER TI**",Top_insurance_tac_Y ["Quarter"].min(),Top_insurance_tac_Y  ["Quarter"].max(),Top_insurance_tac_Y ["Quarter"].min())
            
            Top_insur_tac_y_q=  Transaction_amount_count_Y_Q(Top_insurance_tac_Y , quarter)


        elif method_3 == "Top Transaction":
            col1,col2 = st.columns(2)
            with col1:
                years=st.slider("**SELECT THE YEAR TT**",Top_Transaction["Years"].min(),Top_Transaction["Years"].max(),Top_Transaction["Years"].min())
            Top_tran_tac_Y = Transaction_amount_count_Y(Top_Transaction, years)

            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox ("**SELECT THE STATES TT**",Top_tran_tac_Y["States"].unique())
            Top_Insur_plot_1(Top_tran_tac_Y , states)

            col1,col2 = st.columns(2)
            with col1:
                quarter=st.slider("**SELECT THE QUARTER TT**",Top_tran_tac_Y ["Quarter"].min(),Top_tran_tac_Y ["Quarter"].max(),Top_tran_tac_Y ["Quarter"].min())
            
            Top_tran_tac_y_q=  Transaction_amount_count_Y_Q(Top_tran_tac_Y , quarter)

        elif method_3 =="Top User":
            col1,col2 = st.columns(2)
            with col1:
                years=st.slider("**SELECT THE YEAR TU**",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            Top_user_y = top_user_1(Top_user, years)

            col1,col2 = st.columns(2)

            with col1:
                states = st.selectbox ("**SELECT THE STATES TU**", Top_user_y["States"].unique())
            
            top_user_2(Top_user_y, states)

elif Select == "TOP CHARTS":

    question= st.selectbox("select the Question",["1.Top 10 Transaction Amount of Aggregated Insurance",
                                                  "2.States With Lowest Trasaction Amount",
                                                  "3.Districts With Highest Transaction Amount",
                                                  "4.Top 10 Districts With Lowest Transaction Amount",
                                                  "5.Top 10 States With AppOpens",
                                                  "6.Least 10 States With AppOpens",
                                                  "7.States With Lowest Trasaction Count",
                                                  "8. States With Highest Trasaction Count",
                                                  "9. States With Highest Trasaction Amount",
                                                  "10.Top 50 Districts With Lowest Transaction Amount",])

    if question == "1.Top 10 Transaction Amount of Aggregated Insurance":
        Top_chart_1()

    if question == "2.States With Lowest Trasaction Amount":
        ques2()

    if question == "3.Districts With Highest Transaction Amount":
        ques3()

    if question == "4.Top 10 Districts With Lowest Transaction Amount":
        ques4()

    if question == "5.Top 10 States With AppOpens":
        ques5()

    if question == "6.Least 10 States With AppOpens":
        ques6()

    if question == "7.States With Lowest Trasaction Count":
        ques7()
    
    if question == "8. States With Highest Trasaction Count":
        ques8()

    if question == "9. States With Highest Trasaction Amount":
        ques9()

    if question == "10.Top 50 Districts With Lowest Transaction Amount":
        ques10()

    

