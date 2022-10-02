import pandas as pd
import plotly.express as px 
import streamlit as st 
import streamlit.components.v1 as components
import webbrowser

st.set_page_config(page_title = 'Employee Attrition', #Nombre de la pagina, sale arriba cuando se carga streamlit
                   page_icon = ':chart_with_downwards_trend:', # https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")

st.title(':clipboard: Job Role') #Titulo del Dash

st.subheader('IBM HR Analytics Employee Attrition & Performance')

st.text('Dataset: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset')

url = 'https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset'

if st.button('View dataset'):
    webbrowser.open_new_tab(url)

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

job_role_attrition = attrition_selection.groupby(['JobRole','Attrition']).apply(lambda x:x['JobRole'].count()).reset_index(name='Employees').sort_values(by='Employees', ascending = False)
job_role_attrition = px.bar(job_role_attrition,x='JobRole', y='Employees' ,color='Attrition',title='Number of employees per job role')

income_life_balance = px.violin(attrition_selection,x='WorkLifeBalance', y='MonthlyIncome' ,color='Gender',title='Relationship between work-life balance and monthly income (in thousands)')

left_column, right_column = st.columns(2)


left_column.plotly_chart(job_role_attrition, use_container_width = True) 
right_column.plotly_chart(income_life_balance, use_container_width = True) 

monthly_income_attrition = attrition_selection.groupby(['MonthlyIncome','Attrition']).apply(lambda x:x['MonthlyIncome'].count()).reset_index(name='Employees')
monthly_income_attrition = px.histogram(monthly_income_attrition,x='MonthlyIncome', y='Employees', color='Attrition',title='Number of employees according to monthly income (in thousands)')

income_working_year = px.scatter(attrition_selection,x='TotalWorkingYears', y='MonthlyIncome' ,color='JobLevel', title='Relationship between total years worked and monthly income (in thousands)')

left_column.plotly_chart(monthly_income_attrition, use_container_width = True)
right_column.plotly_chart(income_working_year, use_container_width = True)

# Hide streamlit style
hide_st_style = """
            <style>
   
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
           
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html= True)

components.html(
    """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js" integrity="sha384-u1OknCvxWvY5kfmNBILK2hRnQC3Pr17a+RTT6rIHI7NnikvbZlHgTPOOmMi466C8" crossorigin="anonymous"></script>
    <script src="https://kit.fontawesome.com/ddfb8eeb9e.js" crossorigin="anonymous"></script>
    <footer class="bg-light text-center text-black">
    <!-- Grid container -->
    <div class="container p-4 pb-0">
        <!-- Section: Social media -->
        <section class="mb-4">
        <!-- Linkedin -->
        <a class="btn btn-outline-dark btn-floating m-1" href="https://www.linkedin.com/in/juan-gallardo-digital/" target="_blank" role="button"
            ><i class="fab fa-linkedin-in"></i
        ></a>

        <!-- Github -->
        <a class="btn btn-outline-dark btn-floating m-1" href="https://github.com/juan-gallardo" target="_blank" role="button"
            ><i class="fab fa-github"></i
        ></a>
        </section>
        <!-- Section: Social media -->
    </div>
    <!-- Grid container -->

    <!-- Copyright -->
    <div class="text-center p-3" style="background-color: rgba(220, 220, 220, 0.2);">
        Design by:
        <a class="text-black" href="https://www.linkedin.com/in/juan-gallardo-digital/"target="_blank">Juan Gallardo</a>
    </div>
    <!-- Copyright -->
    </footer>
    """,
    height=600,
)
