import streamlit as st
import pandas as pd
import re

# 1. Configuração da Página
st.set_page_config(page_title="Gamificação | Level 5", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .titulo { text-align: center; font-size: 3em; font-weight: bold; color: #1E90FF; } 
    .subtitulo { text-align: center; color: #A9A9A9; margin-bottom: 40px; }
    .missao-card { background-color: #1E1E24; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #1E90FF; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="titulo">🚀 Portal de Gamificação Level 5</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Sua jornada de desenvolvimento começa aqui. 1 Estrela = 1 Nível!</div>', unsafe_allow_html=True)

# 2. Função Robusta para ler os dados da Planilha
@st.cache_data(ttl=30)
def carregar_dados(url_planilha):
    # Extrai o ID da planilha de forma segura usando Expressão Regular (Regex)
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url_planilha)
    if match:
        id_planilha = match.group(1)
        url_csv = f"https://docs.google.com/spreadsheets/d/{id_planilha}/export?format=csv"
    else:
        url_csv = url_planilha
        
    df = pd.read_csv(url_csv)
    
    # Remove espaços em branco invisíveis antes ou depois dos nomes das colunas
    df.columns = df.columns.str.strip()
    
    # Garante que a coluna Estrelas exista e seja numérica
    if 'Estrelas' not in df.columns:
        df['Estrelas'] = 0
    df['Estrelas'] = pd.to_numeric(df['Estrelas'], errors='coerce').fillna(0).astype(int)
        
    # Ordena do maior para o menor número de estrelas
    df = df.sort_values(by="Estrelas", ascending=False).reset_index(drop=True)
    return df

# ==========================================
# COLOQUE O LINK DA SUA PLANILHA AQUI
# ==========================================
LINK_GOOGLE_SHEETS = "https://docs.google.com/spreadsheets/d/1Ynoj6-Pm2WqTZ0uUnJCJ0IGL_7J81KFj/edit?usp=sharing&ouid=111398974253454738302&rtpof=true&sd=true" 

try:
    df = carregar_dados(LINK_GOOGLE_SHEETS)
    
    # Verifica se as colunas esperadas realmente existem após a leitura
    if 'Nome Completo' in df.columns and 'Equipe' in df.columns:
        
        col_ranking, col_regras = st.columns([2, 1])

        with col_ranking:
            st.markdown("<h3 style='text-align: center;'>🏆 Pódio de Honra</h3><br>", unsafe_allow_html=True)
            
            # Pódio Top 3 (Ouro, Prata e Bronze)
            p1, p2, p3 = st.columns(3)
            if len(df) >= 3:
                with p2:
                    st.success("🥇 Ouro (1º Lugar)")
                    nome_p1 = df.iloc[0]['Nome Completo'].split()[0]
                    st.metric(label=f"{nome_p1} ({df.iloc[0]['Equipe']})", value=f"Nível {df.iloc[0]['Estrelas']} ⭐️")
                with p1:
                    st.info("🥈 Prata (2º Lugar)")
                    nome_p2 = df.iloc[1]['Nome Completo'].split()[0]
                    st.metric(label=f"{nome_p2} ({df.iloc[1]['Equipe']})", value=f"Nível {df.iloc[1]['Estrelas']} ⭐️")
                with p3:
                    st.warning("🥉 Bronze (3º Lugar)")
                    nome_p3 = df.iloc[2]['Nome Completo'].split()[0]
                    st.metric(label=f"{nome_p3} ({df.iloc[2]['Equipe']})", value=f"Nível {df.iloc[2]['Estrelas']} ⭐️")
            else:
                st.write("Adicione pelo menos 3 membros na planilha para exibir o pódio completo.")

            st.divider()

            # Tabela Geral Interativa
            st.markdown("### 📋 Tabela de Classificação")
            busca = st.text_input("🔍 Busque pelo seu nome:")
            
            if busca:
                df_filtrado = df[df['Nome Completo'].str.contains(busca, case=False, na=False)]
            else:
                df_filtrado = df
                
            st.dataframe(
                df_filtrado[['Nome Completo', 'Equipe', 'Estrelas']], 
                use_container_width=True, 
                hide_index=True
            )

        with col_regras:
            st.markdown("### 🎯 Mural de Missões")
            st.markdown("*Cumpra as missões abaixo e reivindique sua estrela com o RH!*")
            
            st.markdown("""
            <div class="missao-card">
                <b>🎩 Hat-Trick de RG</b><br>Participar de 3 Reuniões Gerais seguidas.
            </div>
            <div class="missao-card">
                <b>💼 Sextou com Vaga</b><br>Mandar uma vaga de estágio/trainee na sexta no grupo.
            </div>
            <div class="missao-card">
                <b>📱 Embaixador Level</b><br>Curtir e comentar todos os posts do mês nas redes.
            </div>
            <div class="missao-card">
                <b>🤝 Presença Vip</b><br>100% de presença nas reuniões semanais da equipe no mês.
            </div>
            <div class="missao-card">
                <b>🌐 Representante</b><br>Participar de um evento da rede EJ.
            </div>
            """, unsafe_allow_html=True)
            
            st.divider()
            st.markdown("### 🌟 Cumpriu uma missão?")
            st.link_button("Reivindicar minha Estrela (Forms)", "COLE_AQUI_O_LINK_DO_SEU_FORMS", use_container_width=True)
            
    else:
        # Mensagem de diagnóstico caso os nomes das colunas na planilha ainda estejam diferentes
        st.error(f"⚠️ Erro de Colunas! O código esperava encontrar 'Nome Completo' e 'Equipe'. As colunas detectadas na sua planilha foram: {list(df.columns)}")

except Exception as e:
    st.error(f"⚠️ Erro crítico ao ler a planilha: {e}. Verifique se o link foi colado corretamente dentro das aspas.")
