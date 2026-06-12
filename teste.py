from utils import *

df = read_excel()

st.set_page_config(layout="wide")

previous_month:str = (datetime.now() - relativedelta(months=1)).strftime("%B").capitalize()

st.title("Checklist - {}".format(previous_month))


df.drop(df.loc[:, "Acumulado Prev":"Previsão mês próximo"], axis=1, inplace=True)
df.drop("Unnamed: 31", axis=1, inplace=True)
df.drop(df.query("Pilar == '-' or Pilar == 'TOTAL ACUMULADO' or Distribuidora == 'Global Distribuidora'").index,inplace=True)
nova_col_dict = {col: "Realizado {}/26".format(name_Month(col)) for col in df.loc[:, "2026-01-01 00:00:00.1":].columns}
df.rename(columns=nova_col_dict, inplace=True)
nova_icol_dict = {col: "Previsto {}/26".format(col.strftime("%B").capitalize()) for col in df.iloc[:, 19:31].columns}
df.rename(columns=nova_icol_dict, inplace=True)
df_global = df.query("Regional == 'TODAS'")
df_regionais = df.query("Regional != 'TODAS'")


Distribuidoras = list(df_global['Distribuidora'].unique())

mask = df.columns.str.contains(previous_month)
matching_columns = df.columns[mask]

tabelas_distribuidoras = {}

for distribuidora in Distribuidoras:
    
    tabela_filtrada = df_global.query(
        "`Status das ações` == 'Iniciada' and "
        "Distribuidora == @distribuidora and "
        "Pilar != 'CAPACITAÇÃO' and "
        "`Ação Iniciada?` == 'Em Execução na Distribuidora'"
    ).groupby("Pilar").agg(
        Apuração=("Ação Iniciada?", "count"), 
        Recebido=(matching_columns[1], "count") 
    ).assign(
        Status=lambda x: x['Recebido'] / x['Apuração'] 
    )
    
    tabelas_distribuidoras[distribuidora] = tabela_filtrada


# for name, tab in tabelas_distribuidoras.items():
#     st.subheader(name)
    

#     tab_corrigida = tab.reset_index()
    

#     ordem_desejada = ["COMPORTAMENTO", "POPULAÇÃO", "FORNECEDOR", "LIDERANÇA"]
    
   
#     tab_corrigida['Pilar'] = pd.Categorical(
#         tab_corrigida['Pilar'], 
#         categories=ordem_desejada, 
#         ordered=True
#     )
    
#     tab_corrigida = tab_corrigida.sort_values('Pilar')
    

#     df_estilizado = (
#         tab_corrigida.style
#         .map(colorir_pilar, subset=['Pilar']) 
#         .map(colorir_status, subset=['Status']) 
#         .format({'Status': '{:.0%}'})
#     )
    
#     st.dataframe(df_estilizado, hide_index=True, use_container_width=True, column_config={
#         "Apuração":"Qntd de Apurações",
#         "Recebido":"Qntd de Recebidos",
#         "Status":"Status de Recebimento"
#     })

#     st.divider()

itens_distribuidoras = list(tabelas_distribuidoras.items())
ordem_desejada = ["COMPORTAMENTO", "POPULAÇÃO", "FORNECEDOR", "LIDERANÇA"]


for i in range(0, len(itens_distribuidoras), 3):
    
    cols = st.columns(3)
    
    for j in range(3):
        
        if i + j < len(itens_distribuidoras):
            name, tab = itens_distribuidoras[i + j]
            
            
            with cols[j]:
                st.subheader(name)
                
                tab_corrigida = tab.reset_index()
                
                tab_corrigida['Pilar'] = pd.Categorical(
                    tab_corrigida['Pilar'], 
                    categories=ordem_desejada, 
                    ordered=True
                )
                
                tab_corrigida = tab_corrigida.sort_values('Pilar')
                
                df_estilizado = (
                    tab_corrigida.style
                    .map(colorir_pilar, subset=['Pilar']) 
                    .map(colorir_status, subset=['Status']) 
                    .format({'Status': '{:.0%}'})
                )
                
                st.dataframe(
                    df_estilizado, 
                    hide_index=True, 
                    use_container_width=True, 
                    column_config={
                        "Apuração": "Qntd de Apurações",
                        "Recebido": "Qntd de Recebidos",
                        "Status": "Status de Recebimento"
                    }
                )
   
    st.divider()


st.markdown(
    '<iframe title="Jornada de Segurança - Dash Distribuidoras 2026" width="1024" height="1060" src="https://app.powerbi.com/view?r=eyJrIjoiYjZkZGJiODEtMmExMS00ZGRjLWE0YzQtOTE4ZGZhNGU2ZTJlIiwidCI6IjkxZDEwNWNkLTEwYzYtNDJkMC04N2VlLWFjMDg2YmM1YTUyNyJ9&pageName=ReportSection" frameborder="0" allowFullScreen="true"></iframe>',
    unsafe_allow_html=True
)