import pandas as pd 
import plotly.express as px
import streamlit as st 

st.set_page_config(page_title = 'Employee Attrition', #Nombre de la pagina, sale arriba cuando se carga streamlit
                   page_icon = ':chart_with_downwards_trend:', # https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")

st.title(':earth_americas: Employee Demographics') #Titulo del Dash
## st.markdown('##') #Para separar el titulo de los KPIs, se inserta un paragrafo usando un campo de markdown

st.markdown('----')

# Leo el dataset
attrition = pd.read_csv('data/employee_attrition.csv')

# Reemplazo los valores números de las variables categoricas por sus valores

attrition['Education'] = attrition['Education'].replace([1,2,3,4,5], ['Below College', 'College', 'Bachelor', 'Master', 'Doctor'])

attrition['EnvironmentSatisfaction'] = attrition['EnvironmentSatisfaction'].replace([1,2,3,4], ['Low', 'Medium', 'High', 'Very High'])

attrition['JobInvolvement'] = attrition['JobInvolvement'].replace([1,2,3,4], ['Low', 'Medium', 'High', 'Very High'])

attrition['JobLevel'] = attrition['JobLevel'].replace([1,2,3,4,5], ['Entry Level', 'Mid Level', 'Senior', 'Lead', 'Executive'])

attrition['JobSatisfaction'] = attrition['JobSatisfaction'].replace([1,2,3,4], ['Low', 'Medium', 'High', 'Very High'])

attrition['PerformanceRating'] = attrition['PerformanceRating'].replace([1,2,3,4], ['Low', 'Good', 'Excellent', 'Outstanding'])

attrition['RelationshipSatisfaction'] = attrition['RelationshipSatisfaction'].replace([1,2,3,4], ['Low', 'Medium', 'High', 'Very High'])

attrition['WorkLifeBalance'] = attrition['WorkLifeBalance'].replace([1,2,3,4], ['Bad', 'Good', 'Better', 'Best'])

#st.dataframe(df) 

st.sidebar.header("Filters:") #sidebar lo que nos va a hacer es crear en la parte izquierda un cuadro para agregar los filtros que queremos tener
attrition_values = st.sidebar.multiselect(
    "Attrition:",
    options = attrition['Attrition'].unique(),
    default = attrition['Attrition'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

business_travel = st.sidebar.multiselect(
    "Business Travel:",
    options = attrition['BusinessTravel'].unique(),
    default = attrition['BusinessTravel'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

department = st.sidebar.multiselect(
    "Department:",
    options = attrition['Department'].unique(),
    default = attrition['Department'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

education = st.sidebar.multiselect(
    "Education:",
    options = attrition['Education'].unique(),
    default = attrition['Education'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

education_field = st.sidebar.multiselect(
    "Education Field:",
    options = attrition['EducationField'].unique(),
    default = attrition['EducationField'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

environment_satisfaction = st.sidebar.multiselect(
    "EnvironmentSatisfaction:",
    options = attrition['EnvironmentSatisfaction'].unique(),
    default = attrition['EnvironmentSatisfaction'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

gender = st.sidebar.multiselect(
    "Gender:",
    options = attrition['Gender'].unique(),
    default = attrition['Gender'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

job_involvement = st.sidebar.multiselect(
    "Job Involvement:",
    options = attrition['JobInvolvement'].unique(),
    default = attrition['JobInvolvement'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

job_level = st.sidebar.multiselect(
    "Job Level:",
    options = attrition['JobLevel'].unique(),
    default = attrition['JobLevel'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

job_role = st.sidebar.multiselect(
    "Job Role:",
    options = attrition['JobRole'].unique(),
    default = attrition['JobRole'].unique() #Aqui podría por default dejar un filtro especifico pero vamos a dejarlos todos puestos por default
)

attrition_selection = attrition.query("Attrition == @attrition_values  & BusinessTravel == @business_travel & Department == @department & Education == @education & EducationField == @education_field & EnvironmentSatisfaction == @environment_satisfaction & Gender == @gender & JobInvolvement == @job_involvement & JobLevel == @job_level & JobRole == @job_role") 

# Gráficos

gender_attrition = attrition_selection.groupby(['Gender','Attrition']).apply(lambda x:x['Gender'].count()).reset_index(name='Employees')
gender_attrition = px.bar(gender_attrition, x='Gender', y='Employees', color='Attrition', title='Desertion by gender')

age_attrition = attrition_selection.groupby(['Age','Attrition']).apply(lambda x:x['Age'].count()).reset_index(name='Employees')
age_attrition = px.histogram(age_attrition,x='Age',y='Employees',color='Attrition',title='Number of employees by age')

left_column, right_column = st.columns(2)


left_column.plotly_chart(gender_attrition, use_container_width = True) 
right_column.plotly_chart(age_attrition, use_container_width = True) 
            
marital_status_attrition = attrition_selection.groupby(['MaritalStatus','Attrition']).apply(lambda x:x['MaritalStatus'].count()).reset_index(name='Employees').sort_values(by='Employees', ascending = True)
marital_status_attrition = px.bar(marital_status_attrition,x='Employees',y='MaritalStatus',color='Attrition', orientation='h', title='Monthly income in thousands according to marital status')

distance_job_attrition= attrition_selection.groupby(['DistanceFromHome','Attrition']).apply(lambda x:x['DistanceFromHome'].count()).reset_index(name='Employees')
distance_job_attrition = px.histogram(distance_job_attrition,x='DistanceFromHome',y='Employees',color='Attrition',title='Number of employees according to distance from home')


left_column, right_column = st.columns(2)

left_column.plotly_chart(marital_status_attrition, use_container_width = True) 
right_column.plotly_chart(distance_job_attrition, use_container_width = True) 

# Hide streamlit style
hide_st_style = """
            <style>
   
            footer {visibility: hidden;}
           
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html= True)
