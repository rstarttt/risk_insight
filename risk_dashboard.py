"""
Risk Assessment Dashboard - Streamlit + AgGrid

Lancia con:
    streamlit run risk_dashboard.py

Dipendenze:
    pip install streamlit streamlit-aggrid pandas

Questa dashboard permette di gestire, visualizzare e modificare in modo avanzato i rischi di progetto tramite una tabella interattiva, esportazione dati e grafico riepilogativo.
"""

import streamlit as st
import pandas as pd
import os
from datetime import date
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode, DataReturnMode
from io import BytesIO

# Nome del file per la persistenza dei dati (nel percorso corrente)
DATA_FILE = 'risk_data.csv'

# Streamlit page config (opzionale, per layout wide)
st.set_page_config(page_title="Dashboard Risk Assessment", layout="wide")

# CSS globale per tema scuro uniforme ottimizzato
st.markdown("""
<style>
body {
    color: #e0e6f0;
    background-color: #0d1117;
}
.stApp {
    background-color: #0d1117;
}
.stAppHeader {
    background-color: #0d1117;
}
/* Miglioramenti form e input */
div[data-testid="stSlider"] label, 
div[data-testid="stSelectbox"] label, 
div[data-testid="stDateInput"] label,
div[data-testid="stTextInput"] label {
    color: #e0e6f0 !important;
    font-weight: 500 !important;
}
.stSlider > div > div > div {
    background-color: #1f2937 !important;
}
.stSelectbox > div > div {
    background-color: #1f2937 !important;
    border-color: #374151 !important;
}
.stTextInput > div > div > input {
    background-color: #1f2937 !important;
    border-color: #374151 !important;
    color: #e0e6f0 !important;
}
/* Stile per i pulsanti principali */
.stButton > button {
    background: transparent;
    color: #DC143C;
    border: 2px solid #DC143C;
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background: rgba(220, 20, 60, 0.1);
    border-color: #FF1744;
    color: #FF1744;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(220, 20, 60, 0.2);
}
/* Header styling */
h1, h2, h3 {
    color: #e0e6f0 !important;
    font-weight: 600 !important;
}
h2 {
    border-bottom: 2px solid #DC143C;
    padding-bottom: 2px;
    margin-bottom: 16px;
}
/* Success messages */
.stSuccess {
    background-color: rgba(34, 197, 94, 0.1) !important;
    border: 1px solid rgba(34, 197, 94, 0.3) !important;
}
/* Info messages */
.stInfo {
    background-color: rgba(59, 130, 246, 0.1) !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
}
/* Warning messages */
.stWarning {
    background-color: rgba(251, 191, 36, 0.1) !important;
    border: 1px solid rgba(251, 191, 36, 0.3) !important;
}

/* CSS PERFETTO PER ALLINEAMENTO PULSANTI ELIMINA */
.delete-button-container {
    display: flex;
    flex-direction: column;
    gap: 0;
    padding-top: 2.75rem; /* Allineamento preciso con prima riga dati */
}

.delete-button-row {
    height: 35px; /* Altezza esatta di una riga della tabella */
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0;
    padding: 0;
}

/* Stile specifico per i pulsanti di eliminazione */
.delete-button-row .stButton {
    margin: 0 !important;
    padding: 0 !important;
    height: 24px !important;
    width: 24px !important;
}

.delete-button-row .stButton > button {
    min-height: 24px !important;
    height: 24px !important;
    width: 24px !important;
    padding: 0 !important;
    margin: 0 !important;
    font-size: 14px !important;
    font-weight: bold !important;
    border-radius: 4px !important;
    line-height: 1 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: rgba(239, 68, 68, 0.1) !important;
    border: 1px solid rgba(239, 68, 68, 0.4) !important;
    color: #ef4444 !important;
    transition: all 0.15s ease !important;
}

.delete-button-row .stButton > button:hover {
    background: rgba(239, 68, 68, 0.25) !important;
    border-color: rgba(239, 68, 68, 0.7) !important;
    color: #dc2626 !important;
    transform: scale(1.05) !important;
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3) !important;
}

/* Assicura che il dataframe abbia altezza delle righe consistente */
div[data-testid="stDataFrame"] {
    font-size: 14px !important;
}

div[data-testid="stDataFrame"] tbody tr {
    height: 35px !important;
}

div[data-testid="stDataFrame"] thead tr {
    height: 44px !important;
}
</style>
""", unsafe_allow_html=True)

# Titolo della dashboard con stile premium
st.markdown("""
<div style='width:100%; text-align:center; margin-bottom: 40px;'>
    <h1 style='
        display: inline-block; 
        margin: 0; 
        color: #e0e6f0;
        background: linear-gradient(135deg, #8B0000 0%, #DC143C 50%, #FF6347 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        text-shadow: 0 4px 8px rgba(220, 20, 60, 0.3);
    '>
        🛡️ Dashboard Risk Assessment
    </h1>
    <div style='
        width: 100px; 
        height: 4px; 
        background: linear-gradient(135deg, #8B0000 0%, #DC143C 50%, #FF6347 100%); 
        margin: 16px auto;
        border-radius: 2px;
    '></div>
</div>
""", unsafe_allow_html=True)

# Funzione per caricare il DataFrame da CSV, se esiste
def load_data(file_path):
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            # Assicurati che le colonne abbiano i tipi corretti
            if not df.empty:
                df['ID'] = df['ID'].astype(int)
                df['Probabilità'] = df['Probabilità'].astype(float)  # Float per decimali
                df['Impatto'] = df['Impatto'].astype(float)        # Float per decimali
                df['Valore_Rischio'] = df['Valore_Rischio'].astype(float)  # Float per decimali
            return df
        except Exception as e:
            st.error(f"Errore nel caricamento dei dati: {e}")
            return create_empty_dataframe()
    else:
        return create_empty_dataframe()

# Funzione per creare DataFrame vuoto
def create_empty_dataframe():
    return pd.DataFrame({
        "ID": [],
        "Descrizione": [],
        "Probabilità": [],
        "Impatto": [],
        "Valore_Rischio": [],
        "Priorità": [],
        "Contromisura": [],
        "Stato": [],
        "Data scadenza": []
    })

# Funzione per salvare il DataFrame su CSV
def save_data(df, file_path):
    try:
        df.to_csv(file_path, index=False)
        return True
    except Exception as e:
        st.error(f"Errore nel salvataggio dei dati: {e}")
        return False

# Inizializza i dati
if 'df' not in st.session_state:
    st.session_state.df = load_data(DATA_FILE)

# Forza il reload dei dati dal file ad ogni refresh per garantire sincronizzazione
def refresh_data():
    st.session_state.df = load_data(DATA_FILE)

# Verifica se c'è stato un rerun e ricarica i dati
if 'page_refresh' not in st.session_state:
    st.session_state.page_refresh = 0
    refresh_data()

# Funzione per calcolare priorità basata su Valore_Rischio (0-25)
def calcola_priorita(valore_rischio):
    if valore_rischio >= 16:
        return "Estrema"
    elif valore_rischio >= 11:
        return "Alta"
    elif valore_rischio >= 6:
        return "Media"
    else:
        return "Bassa"

# Funzione per eliminare un rischio
def elimina_rischio(risk_id):
    """Elimina un rischio e salva immediatamente"""
    # Rimuovi il rischio dal DataFrame
    st.session_state.df = st.session_state.df[st.session_state.df['ID'] != risk_id]
    
    # Salva immediatamente nel file
    if save_data(st.session_state.df, DATA_FILE):
        return True
    return False

# Funzione per creare heat map come immagine
def create_heatmap_image(df):
    """Crea una heat map come immagine per il PDF"""
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        import numpy as np
        from io import BytesIO
        
        # Configura matplotlib per funzionare senza display
        plt.switch_backend('Agg')
        
        # Crea figura
        fig, ax = plt.subplots(figsize=(10, 8))
        fig.patch.set_facecolor('white')
        
        # Definisci colori per priorità
        def get_risk_color(prob, imp):
            risk_value = prob * imp
            if risk_value >= 16:
                return '#ef4444'  # Rosso
            elif risk_value >= 11:
                return '#f97316'  # Arancione
            elif risk_value >= 6:
                return '#eab308'  # Giallo
            elif risk_value >= 1:
                return '#22c55e'  # Verde
            else:
                return '#9ca3af'  # Grigio
        
        # Crea griglia 5x5 con ordine crescente dal basso-sinistra all'alto-destra
        # Griglia rappresenta valori da 1 a 5
        for i in range(5):  # Impatto (dal basso all'alto)
            for j in range(5):  # Probabilità (da sinistra a destra)
                # Calcola il valore per ogni cella della griglia
                prob = j + 1  # 1, 2, 3, 4, 5
                imp = i + 1   # 1, 2, 3, 4, 5 (dal basso all'alto)
                color = get_risk_color(prob, imp)
                
                # Disegna rettangolo
                rect = patches.Rectangle((j, i), 1, 1, linewidth=2, 
                                       edgecolor='#334155', facecolor=color, alpha=0.7)
                ax.add_patch(rect)
        
        # Raggruppa rischi per posizione
        risk_positions = {}
        for _, row in df.iterrows():
            prob = float(row['Probabilità'])
            imp = float(row['Impatto'])
            risk_id = int(row['ID'])
            position_key = (prob, imp)
            
            if position_key not in risk_positions:
                risk_positions[position_key] = []
            risk_positions[position_key].append(risk_id)
        
        # Aggiungi punti dei rischi con posizionamento decimale preciso
        for (prob, imp), risk_ids in risk_positions.items():
            if prob >= 1 and imp >= 1:  # Valori validi da 1 a 5
                # Posizionamento preciso basato sui valori decimali
                # Per prob=1, x=0.5 (centro prima cella)
                # Per prob=2, x=1.5 (centro seconda cella)
                # Per prob=2.5, x=2.0 (tra seconda e terza cella)
                x = prob - 0.5  # Converte valori 1-5 in posizioni 0.5-4.5
                y = imp - 0.5   # Converte valori 1-5 in posizioni 0.5-4.5
                
                # Crea etichetta con ID
                id_string = ', '.join(map(str, sorted(risk_ids)))
                
                # Dimensione punto basata sul numero di rischi
                size = 200 + len(risk_ids) * 100
                
                # Aggiungi punto nero con bordo bianco
                ax.scatter(x, y, s=size, c='black', edgecolors='white', 
                          linewidth=2, zorder=10)
                
                # Aggiungi testo ID
                ax.text(x, y, id_string, ha='center', va='center', 
                       color='white', fontweight='bold', fontsize=8, zorder=11)
        
        # Configurazione assi per range 1-5
        ax.set_xlim(0, 5)
        ax.set_ylim(0, 5)
        ax.set_aspect('equal')
        
        # Etichette assi - da 1 a 5
        prob_labels = ['1', '2', '3', '4', '5']
        imp_labels = ['1', '2', '3', '4', '5']
        
        ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5])
        ax.set_xticklabels(prob_labels, fontsize=9)
        ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5])
        ax.set_yticklabels(imp_labels, fontsize=9)
        
        # Titoli assi
        ax.set_xlabel('PROBABILITÀ', fontweight='bold', fontsize=12, labelpad=10)
        ax.set_ylabel('IMPATTO', fontweight='bold', fontsize=12, labelpad=10)
        
        # Titolo
        ax.set_title('HEAT MAP DEI RISCHI', fontweight='bold', fontsize=14, pad=20)
        
        # Griglia
        ax.grid(True, alpha=0.3)
        ax.set_axisbelow(True)
        
        # Legenda
        legend_elements = [
            patches.Patch(color='#22c55e', label='Bassa (1-5)'),
            patches.Patch(color='#eab308', label='Media (6-10)'),
            patches.Patch(color='#f97316', label='Alta (11-15)'),
            patches.Patch(color='#ef4444', label='Estrema (16-25)')
        ]
        ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1), 
                 title='Priorità', title_fontsize=10, fontsize=9)
        
        # Salva in buffer
        img_buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(img_buffer, format='PNG', dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        plt.close()
        
        img_buffer.seek(0)
        return img_buffer
        
    except ImportError:
        st.warning("Matplotlib non disponibile. Heat map non inclusa nel PDF.")
        return None
    except Exception as e:
        st.warning(f"Errore nella creazione della heat map: {str(e)}")
        return None

# Funzione per creare PDF con gestione errori robusta
def create_pdf_report(df):
    """Crea un report PDF con heat map inclusa"""
    try:
        # Import con gestione errori
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib.enums import TA_CENTER
        import io
        
        # Crea buffer per il PDF
        pdf_buffer = io.BytesIO()
        
        # Crea documento PDF con parametri semplificati
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=landscape(A4),
            rightMargin=20,
            leftMargin=20,
            topMargin=20,
            bottomMargin=20
        )
        
        # Lista elementi da aggiungere al PDF
        elements = []
        
        # Stili base
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=20,
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        # Titolo
        elements.append(Paragraph("🛡️ Risk Assessment Report", title_style))
        elements.append(Paragraph(f"Data: {date.today().strftime('%d/%m/%Y')}", styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Prepara dati per la tabella (versione semplificata) con decimali
        data = [['ID', 'Descrizione', 'Prob.', 'Imp.', 'Priorità', 'Stato']]
        
        for _, row in df.iterrows():
            # Tronca le descrizioni lunghe per evitare problemi di layout
            desc = str(row['Descrizione'])
            if len(desc) > 40:
                desc = desc[:37] + "..."
                
            data.append([
                str(row['ID']),
                desc,
                f"{row['Probabilità']:.1f}",  # Mostra un decimale
                f"{row['Impatto']:.1f}",      # Mostra un decimale
                str(row['Priorità']),
                str(row['Stato'])
            ])
        
        # Crea tabella con stile semplificato
        table = Table(data)
        
        # Stile tabella base
        table_style = TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Corpo tabella
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        
        table.setStyle(table_style)
        elements.append(table)
        
        # Aggiungi riepilogo
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph("Riepilogo per Priorità", styles['Heading2']))
        
        # Conta rischi per priorità
        priority_counts = df['Priorità'].value_counts()
        summary_text = ""
        for priority in ['Estrema', 'Alta', 'Media', 'Bassa']:
            count = priority_counts.get(priority, 0)
            summary_text += f"{priority}: {count} rischi<br/>"
        
        elements.append(Paragraph(summary_text, styles['Normal']))
        
        # Aggiungi heat map se possibile
        heatmap_img = create_heatmap_image(df)
        if heatmap_img is not None:
            elements.append(PageBreak())
            elements.append(Paragraph("Heat Map dei Rischi", styles['Heading2']))
            elements.append(Spacer(1, 0.2*inch))
            
            # Crea immagine per ReportLab
            img = Image(heatmap_img, width=7*inch, height=5*inch)
            elements.append(img)
            
            # Note esplicative
            elements.append(Spacer(1, 0.3*inch))
            elements.append(Paragraph("Note: I numeri neri indicano gli ID dei rischi posizionati secondo probabilità e impatto (valori da 1 a 5 con incrementi di 0.5). "
                                    "I colori rappresentano le priorità: Verde (Bassa), Giallo (Media), Arancione (Alta), Rosso (Estrema).", 
                                    styles['Normal']))
        
        # Costruisci PDF
        doc.build(elements)
        pdf_buffer.seek(0)
        
        return pdf_buffer
        
    except ImportError:
        st.error("Librerie necessarie non disponibili. Installa con: pip install reportlab matplotlib")
        return None
    except Exception as e:
        st.error(f"Errore nella creazione del PDF: {str(e)}")
        return None

# Inizializza i valori del form nel session_state
if 'form_descrizione' not in st.session_state:
    st.session_state.form_descrizione = ""
if 'form_prob' not in st.session_state:
    st.session_state.form_prob = 1.0
if 'form_imp' not in st.session_state:
    st.session_state.form_imp = 1.0
if 'form_contromisura' not in st.session_state:
    st.session_state.form_contromisura = ""
if 'form_stato' not in st.session_state:
    st.session_state.form_stato = "Da pianificare"
if 'form_data_scad' not in st.session_state:
    st.session_state.form_data_scad = date.today()
if 'form_counter' not in st.session_state:
    st.session_state.form_counter = 0

# Sezione per aggiungere un nuovo rischio
st.header("Aggiungi Nuovo Rischio")
# Uso un key dinamico che cambia ad ogni reset per forzare la ricreazione del form
with st.form(key=f'form_nuovo_rischio_{st.session_state.form_counter}'):
    descrizione = st.text_input("Descrizione del rischio", value=st.session_state.form_descrizione)
    prob = st.slider("Probabilità (1-5)", min_value=1.0, max_value=5.0, value=st.session_state.form_prob, step=0.5)
    imp = st.slider("Impatto (1-5)", min_value=1.0, max_value=5.0, value=st.session_state.form_imp, step=0.5)
    contromisura = st.text_input("Contromisura", value=st.session_state.form_contromisura)
    stato = st.selectbox("Stato", options=["Da pianificare", "In corso", "Monitoraggio", "Chiuso"], 
                        index=["Da pianificare", "In corso", "Monitoraggio", "Chiuso"].index(st.session_state.form_stato))
    data_scad = st.date_input("Data scadenza", value=st.session_state.form_data_scad)
    submit_button = st.form_submit_button(label='Aggiungi')
    
    if submit_button:
        if descrizione.strip() != '':
            valore = prob * imp
            priorita = calcola_priorita(valore)
            data_scad_str = data_scad.strftime("%Y-%m-%d")
            nuovo_id = int(st.session_state.df["ID"].max()) + 1 if not st.session_state.df.empty else 1
            new_row = {
                "ID": nuovo_id,
                "Descrizione": descrizione,
                "Probabilità": prob,
                "Impatto": imp,
                "Valore_Rischio": valore,
                "Priorità": priorita,
                "Contromisura": contromisura,
                "Stato": stato,
                "Data scadenza": data_scad_str
            }
            new_df = pd.DataFrame([new_row])
            st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
            
            if save_data(st.session_state.df, DATA_FILE):
                # RESET AUTOMATICO DEL FORM dopo aggiunta riuscita
                st.session_state.form_descrizione = ""
                st.session_state.form_prob = 1.0
                st.session_state.form_imp = 1.0
                st.session_state.form_contromisura = ""
                st.session_state.form_stato = "Da pianificare"
                st.session_state.form_data_scad = date.today()
                st.session_state.form_counter += 1  # Incrementa counter per forzare ricreazione form
                
                st.success("Nuovo rischio aggiunto!")
                st.rerun()
            else:
                st.error("Errore nel salvataggio del nuovo rischio")
        else:
            st.warning("La descrizione non può essere vuota.")

# JavaScript per gestire il tasto Invio nel form
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Trova il form e aggiungi listener per il tasto Invio
    const formInputs = document.querySelectorAll('input[type="text"], input[type="date"]');
    
    formInputs.forEach(function(input) {
        input.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                // Trova il pulsante submit del form
                const submitButton = document.querySelector('button[kind="formSubmit"]');
                if (submitButton) {
                    submitButton.click();
                }
            }
        });
    });
});

// Alternative: listener globale per catturare Invio ovunque nel form
document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        // Controlla se siamo nel form di aggiunta rischio
        const activeElement = document.activeElement;
        const isInForm = activeElement && (
            activeElement.closest('form') || 
            activeElement.tagName === 'INPUT' || 
            activeElement.tagName === 'TEXTAREA'
        );
        
        if (isInForm) {
            const submitButton = document.querySelector('button[kind="formSubmit"]');
            if (submitButton) {
                event.preventDefault();
                submitButton.click();
            }
        }
    }
});
</script>
""", unsafe_allow_html=True)

# Sezione tabella rischi
st.header("Tabella dei rischi")
st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

if not st.session_state.df.empty:
    # Preparo DataFrame per AgGrid con colonna Elimina
    display_df = st.session_state.df.copy()
    display_df = display_df.drop(columns=['Valore_Rischio'])
    
    # Accorcio le descrizioni e contromisure per evitare scroll laterale E AGGIUNGO MAIUSCOLA
    display_df['Descrizione'] = display_df['Descrizione'].apply(
        lambda x: (str(x)[:35] + '...' if len(str(x)) > 35 else str(x)).capitalize()
    )
    display_df['Contromisura'] = display_df['Contromisura'].apply(
        lambda x: (str(x)[:30] + '...' if len(str(x)) > 30 else str(x)).capitalize()
    )
    
    # Aggiungo icone agli stati
    status_mapping = {
        'Da pianificare': '📋',
        'In corso': '⚡', 
        'Monitoraggio': '👀',
        'Chiuso': '✅'
    }
    display_df['Stato'] = display_df['Stato'].map(status_mapping)
    
    # Aggiungo colonna per eliminazione con valore editabile
    display_df['Elimina'] = False  # Valore boolean invece di stringa
    
    # Configurazione AgGrid
    gb = GridOptionsBuilder.from_dataframe(display_df)
    
    # Configurazione generale
    gb.configure_default_column(
        groupable=False,
        value=True,
        enableRowGroup=False,
        aggFunc="sum",
        editable=False,
        resizable=True
    )
    
    # Configurazione colonne specifiche con stili inline forzati e TUTTI i titoli in maiuscolo
    gb.configure_column("ID", width=60, type=["numericColumn"], header_name="ID",
                       cellStyle={'textAlign': 'center', 'fontSize': '16px', 'fontWeight': '600', 
                                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                                'borderRight': '1px solid #334155', 'height': '60px'})
    gb.configure_column("Descrizione", width=220, header_name="DESCRIZIONE",
                       cellStyle={'textAlign': 'center', 'fontSize': '15px', 'fontWeight': '700',
                                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                                'borderRight': '1px solid #334155', 'height': '60px'})
    gb.configure_column("Probabilità", width=100, header_name="PROBABILITÀ", type=["numericColumn"], 
                       cellStyle={'textAlign': 'center', 'fontSize': '16px', 'fontWeight': '600',
                                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                                'borderRight': '1px solid #334155', 'height': '60px'})
    gb.configure_column("Impatto", width=90, header_name="IMPATTO", type=["numericColumn"], 
                       cellStyle={'textAlign': 'center', 'fontSize': '16px', 'fontWeight': '600',
                                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                                'borderRight': '1px solid #334155', 'height': '60px'})
    gb.configure_column("Priorità", width=100, header_name="PRIORITÀ",
                       cellStyle={'textAlign': 'center', 'fontSize': '15px', 'fontWeight': '700',
                                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                                'borderRight': '1px solid #334155', 'height': '60px'})
    gb.configure_column("Contromisura", width=200, header_name="CONTROMISURA",
                       cellStyle={'textAlign': 'center', 'fontSize': '15px', 'fontWeight': '700',
                                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                                'borderRight': '1px solid #334155', 'height': '60px'})
    gb.configure_column("Stato", width=80, header_name="STATO",
                       cellStyle={'textAlign': 'center', 'fontSize': '18px', 'fontWeight': '500',
                                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                                'borderRight': '1px solid #334155', 'height': '60px'})
    gb.configure_column("Data scadenza", width=120, header_name="SCADENZA", 
                       cellStyle={'textAlign': 'center', 'fontSize': '15px', 'fontWeight': '700',
                                'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',
                                'borderRight': '1px solid #334155', 'height': '60px'})
    
    # Colonna Elimina con checkbox editabile che appare come un pulsante
    gb.configure_column(
        "Elimina", 
        width=80,
        header_name="ELIMINA",
        editable=True,
        cellEditor="agCheckboxCellEditor",
        cellRenderer="agCheckboxCellRenderer",
        cellStyle={
            'textAlign': 'center', 
            'borderRight': '1px solid #334155', 
            'height': '60px',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center'
        }
    )
    
    # Configurazione grid
    gb.configure_selection(selection_mode="single", use_checkbox=False)
    gb.configure_grid_options(domLayout='normal', rowHeight=60)
    
    # Tema scuro per AgGrid
    grid_options = gb.build()
    
    # Mostra la griglia con gestione delle modifiche
    grid_response = AgGrid(
        display_df,
        gridOptions=grid_options,
        height=400,
        width='100%',
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        fit_columns_on_grid_load=True,
        theme='streamlit',
        allow_unsafe_jscode=True,
        custom_css={
            "#gridToolBar": {
                "padding-bottom": "0px !important"
            },
            ".ag-theme-streamlit": {
                "border": "2px solid #334155 !important",
                "border-radius": "12px !important",
                "overflow": "hidden !important",
                "box-shadow": "0 8px 32px rgba(0, 0, 0, 0.3) !important"
            },
            ".ag-theme-streamlit .ag-header": {
                "background": "linear-gradient(135deg, #1e293b 0%, #334155 100%) !important",
                "color": "#e2e8f0 !important",
                "font-weight": "600 !important",
                "text-align": "center !important",
                "border-bottom": "2px solid #DC143C !important"
            },
            ".ag-theme-streamlit .ag-header-cell": {
                "border-right": "1px solid #475569 !important",
                "text-align": "center !important"
            },
            ".ag-theme-streamlit .ag-header-cell-text": {
                "text-align": "center !important",
                "width": "100% !important"
            },
            ".ag-theme-streamlit .ag-row": {
                "background-color": "#0f172a !important",
                "color": "#e2e8f0 !important",
                "border-bottom": "1px solid #1e293b !important",
                "transition": "all 0.2s ease !important"
            },
            ".ag-theme-streamlit .ag-row:hover": {
                "background-color": "#1e293b !important",
                "transform": "translateY(-1px) !important",
                "box-shadow": "0 4px 12px rgba(220, 20, 60, 0.1) !important"
            },
            ".ag-theme-streamlit .ag-row-even": {
                "background-color": "#1e293b !important"
            },
            ".ag-theme-streamlit .ag-row-odd": {
                "background-color": "#0f172a !important"
            },
            ".ag-theme-streamlit .ag-row-even:hover": {
                "background-color": "#334155 !important"
            },
            ".ag-theme-streamlit .ag-row-odd:hover": {
                "background-color": "#1e293b !important"
            },
            ".ag-theme-streamlit .ag-cell": {
                "border-right": "1px solid #374151 !important",
                "text-align": "center !important",
                "display": "flex !important",
                "align-items": "center !important",
                "justify-content": "center !important",
                "font-weight": "500 !important"
            },
            ".ag-theme-streamlit .ag-cell-value": {
                "text-align": "center !important"
            },
            # CSS specifico per la colonna Elimina
            ".ag-theme-streamlit [col-id='Elimina'] .ag-cell": {
                "background": "linear-gradient(135deg, rgba(220, 20, 60, 0.1) 0%, rgba(139, 0, 0, 0.15) 100%) !important",
                "border": '2px solid rgba(220, 20, 60, 0.4) !important',
                "border-radius": '8px !important',
                "margin": '4px !important'
            },
            ".ag-theme-streamlit [col-id='Elimina'] .ag-cell:hover": {
                "background": 'linear-gradient(135deg, rgba(220, 20, 60, 0.25) 0%, rgba(139, 0, 0, 0.3) 100%) !important',
                "border-color": 'rgba(220, 20, 60, 0.7) !important',
                "transform": 'scale(1.05) !important'
            },
            ".ag-theme-streamlit [col-id='Elimina'] input[type='checkbox']": {
                "width": '20px !important',
                "height": '20px !important',
                "accent-color": '#ff4757 !important',
                "cursor": 'pointer !important'
            }
        }
    )
    
    # Controlla se qualche checkbox è stata selezionata per l'eliminazione
    if 'data' in grid_response and grid_response['data'] is not None:
        updated_df = pd.DataFrame(grid_response['data'])
        
        # Trova le righe marcate per eliminazione
        if 'Elimina' in updated_df.columns:
            rows_to_delete = updated_df[updated_df['Elimina'] == True]
            
            if not rows_to_delete.empty:
                # Elimina tutti i rischi marcati
                ids_to_delete = rows_to_delete['ID'].tolist()
                
                for risk_id in ids_to_delete:
                    st.session_state.df = st.session_state.df[st.session_state.df['ID'] != risk_id]
                
                # Salva i dati e ricarica
                if save_data(st.session_state.df, DATA_FILE):
                    st.rerun()
                else:
                    st.error(f"Errore nel salvataggio dopo eliminazione")

else:
    st.info("Nessun rischio presente.")

# Heat Map Risk Assessment
if not st.session_state.df.empty:
    st.header("Heat Map dei Rischi")
    
    # Creo l'HTML della heatmap con posizionamento proporzionale per valori decimali
    impact_labels = ['1', '2', '3', '4', '5']
    likelihood_labels = ['1', '2', '3', '4', '5']
    
    # Definisco i colori per le 4 categorie di priorità (0-25)
    def get_risk_color_and_priority(prob, imp):
        risk_value = prob * imp
        if risk_value >= 16:
            return '#ef4444', 'ESTREMA'  # Rosso (16-25)
        elif risk_value >= 11:
            return '#f97316', 'ALTA'     # Arancione (11-15)
        elif risk_value >= 6:
            return '#eab308', 'MEDIA'    # Giallo (6-10)
        elif risk_value >= 1:
            return '#22c55e', 'BASSA'    # Verde (1-5)
        else:
            return '#374151', 'NESSUNO'  # Grigio (0)
    
    # Container principale della heat map
    heatmap_complete = '<div style="display: flex; justify-content: center; margin: 20px 0; padding: 15px;">'
    heatmap_complete += '<div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 40px; border-radius: 16px; box-shadow: 0 15px 40px rgba(0,0,0,0.4); border: 1px solid #475569; max-width: 800px; width: 100%; position: relative;">'
    
    # Etichetta IMPATTO verticale a sinistra (centrata perfettamente sulla griglia)
    heatmap_complete += '<div style="position: absolute; left: 75px; top: 290px; transform: translateY(-50%) rotate(-90deg); font-weight: 700; color: #e2e8f0; font-size: 16px; text-transform: uppercase; letter-spacing: 0.8px; text-shadow: 0 1px 2px rgba(0,0,0,0.5);">IMPATTO</div>'
    
    # Contenitore della griglia con area di disegno assoluta (più largo)
    heatmap_complete += '<div style="position: relative; width: 520px; height: 520px; margin: 0 auto;">'
    
    # Disegno la griglia 5x5 di sfondo (più larga)
    grid_width = 450  # Era 350, ora 450 per più spazio
    grid_height = 450  # Era 350, ora 450 per più spazio
    cell_width = grid_width / 5
    cell_height = grid_height / 5
    
    # Area della griglia di sfondo
    heatmap_complete += f'<div style="position: absolute; top: 29px; left: 80px; width: {grid_width}px; height: {grid_height}px;">'
    
    # Creo le celle di sfondo 5x5 per rappresentare valori da 0 a 5 (corrette)
    for i in range(5):  # Righe (Impact da Alto a Basso nella visualizzazione)
        for j in range(5):  # Colonne (Probabilità da Bassa ad Alta)
            # Calcolo dei valori per ogni cella della griglia
            prob = j + 1  # 1, 2, 3, 4, 5 (da sinistra a destra)
            imp = 5 - i   # 5, 4, 3, 2, 1 (da alto a basso nella visualizzazione)
            color, priority = get_risk_color_and_priority(prob, imp)
            
            x = j * cell_width
            y = i * cell_height
            
            heatmap_complete += f'<div style="position: absolute; left: {x}px; top: {y}px; width: {cell_width}px; height: {cell_height}px; background-color: {color}; border: 2px solid #334155; border-radius: 8px; box-shadow: 0 3px 8px rgba(0,0,0,0.2);" title="Prob: {prob}, Imp: {imp}, Priorità: {priority}"></div>'
    
    # Raggruppo i rischi per posizione (probabilità, impatto)
    risk_positions = {}
    for _, row in st.session_state.df.iterrows():
        prob = float(row['Probabilità'])
        imp = float(row['Impatto'])
        risk_id = int(row['ID'])
        position_key = (prob, imp)
        
        if position_key not in risk_positions:
            risk_positions[position_key] = []
        risk_positions[position_key].append(risk_id)
    
    # Posizionamento corretto dei cerchi con valori decimali
    for (prob, imp), risk_ids in risk_positions.items():
        # Verifica che i valori siano nel range valido 1-5
        if prob < 1 or prob > 5 or imp < 1 or imp > 5:
            continue  # Salta rischi con valori fuori range
            
        risk_value = prob * imp
        
        # CALCOLO CORRETTO: coordinate relative al contenitore griglia
        # Stesse coordinate delle celle di sfondo
        pixel_x = ((prob - 0.5) * cell_width)
        pixel_y = ((5.5 - imp) * cell_height)
        
        # Dimensioni pallino
        num_risks = len(risk_ids)
        size = 28 + (num_risks - 1) * 6
        font_size = 11 if num_risks == 1 else 10
        
        # Crea stringa degli ID
        id_string = ", ".join(map(str, sorted(risk_ids)))
        
        # Posizione finale del pallino (centrato)
        final_x = round(pixel_x - size/2)
        final_y = round(pixel_y - size/2)
        
        heatmap_complete += f'<div style="position: absolute; left: {final_x}px; top: {final_y}px; width: {size}px; height: {size}px; background: #000000; color: #ffffff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; box-shadow: 0 3px 8px rgba(0,0,0,0.6); border: 2px solid #ffffff; font-size: {font_size}px; z-index: 10;" title="Rischi ID: {id_string} - Prob: {prob}, Imp: {imp}, Valore: {risk_value:.1f}">{id_string}</div>'
    
    heatmap_complete += '</div>'  # Chiude area griglia
    
    # Etichette degli assi
    # Etichette Impact (verticali a sinistra) - da 0 a 5 dal basso all'alto
    for i, label in enumerate(reversed(impact_labels)):
        y_pos = 25 + i * cell_height + cell_height/2 - 10
        heatmap_complete += f'<div style="position: absolute; left: 35px; top: {y_pos}px; font-size: 12px; font-weight: 600; color: #cbd5e1; text-transform: uppercase; letter-spacing: 0.3px; width: 40px; text-align: right;">{label}</div>'
    
    # Etichette Probabilità (orizzontali in basso) - allineate come quelle dell'impatto
    for i, label in enumerate(likelihood_labels):
        x_pos = 80 + i * cell_width + cell_width/2 - 10
        heatmap_complete += f'<div style="position: absolute; left: {x_pos}px; top: {25 + grid_height + 15}px; font-size: 12px; font-weight: 600; color: #cbd5e1; text-transform: uppercase; letter-spacing: 0.3px; width: 20px; text-align: center;">{label}</div>'
    
    # Etichetta PROBABILITÀ centrata in basso (perfettamente centrata sulla griglia)
    heatmap_complete += '<div style="position: absolute; left: 305px; top: 520px; transform: translateX(-50%); font-weight: 700; color: #e2e8f0; font-size: 16px; text-transform: uppercase; letter-spacing: 0.8px; text-shadow: 0 1px 2px rgba(0,0,0,0.5);">PROBABILITÀ</div>'
    
    heatmap_complete += '</div>'  # Chiude contenitore griglia
    heatmap_complete += '</div>'  # Chiude heatmap-wrapper
    heatmap_complete += '</div>'  # Chiude heatmap-container
    
    # Mostro la heatmap
    st.markdown(heatmap_complete, unsafe_allow_html=True)

# Sezione per esportazione dati
if not st.session_state.df.empty:
    st.header("Esportazione Dati")
    
    # Aggiungi spazio sopra i pulsanti
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Export PDF con gestione errori migliorata
    with col1:
        if st.button("📄 Esporta in PDF", use_container_width=True):
            with st.spinner("Generazione PDF in corso..."):
                pdf_buffer = create_pdf_report(st.session_state.df)
                
                if pdf_buffer is not None:
                    st.download_button(
                        label="⬇️ Scarica Report PDF",
                        data=pdf_buffer,
                        file_name=f"risk_assessment_report_{date.today()}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success("PDF generato con successo!")
                else:
                    st.error("Impossibile generare il PDF. Verifica che la libreria ReportLab sia installata.")
    
    # Export Excel
    with col2:
        if st.button("📊 Esporta in Excel", use_container_width=True):
            try:
                from openpyxl import Workbook
                from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
                from openpyxl.utils.dataframe import dataframe_to_rows
                
                # Crea workbook
                wb = Workbook()
                ws = wb.active
                ws.title = "Risk Assessment"
                
                # Stili
                header_font = Font(bold=True, color="FFFFFF", size=12)
                header_fill = PatternFill(start_color="1e293b", end_color="1e293b", fill_type="solid")
                header_alignment = Alignment(horizontal="center", vertical="center")
                
                border = Border(
                    left=Side(style='thin', color='334155'),
                    right=Side(style='thin', color='334155'),
                    top=Side(style='thin', color='334155'),
                    bottom=Side(style='thin', color='334155')
                )
                
                # Titolo
                ws.merge_cells('A1:H1')
                ws['A1'] = '🛡️ RISK ASSESSMENT REPORT'
                ws['A1'].font = Font(bold=True, size=20, color="DC143C")
                ws['A1'].alignment = Alignment(horizontal="center", vertical="center")
                ws.row_dimensions[1].height = 40
                
                # Data
                ws.merge_cells('A2:H2')
                ws['A2'] = f'Data Report: {date.today().strftime("%d/%m/%Y")}'
                ws['A2'].font = Font(size=12, italic=True)
                ws['A2'].alignment = Alignment(horizontal="center", vertical="center")
                ws.row_dimensions[2].height = 25
                
                # Spazio
                ws.row_dimensions[3].height = 10
                
                # Header tabella
                headers = ['ID', 'Descrizione', 'Probabilità', 'Impatto', 'Valore Rischio', 'Priorità', 'Contromisura', 'Stato', 'Data Scadenza']
                for col, header in enumerate(headers, 1):
                    cell = ws.cell(row=4, column=col, value=header)
                    cell.font = header_font
                    cell.fill = header_fill
                    cell.alignment = header_alignment
                    cell.border = border
                
                # Dati con valori decimali formattati
                for row_idx, (_, row) in enumerate(st.session_state.df.iterrows(), start=5):
                    ws.cell(row=row_idx, column=1, value=row['ID']).border = border
                    ws.cell(row=row_idx, column=2, value=row['Descrizione']).border = border
                    ws.cell(row=row_idx, column=3, value=f"{row['Probabilità']:.1f}").border = border
                    ws.cell(row=row_idx, column=4, value=f"{row['Impatto']:.1f}").border = border
                    ws.cell(row=row_idx, column=5, value=f"{row['Valore_Rischio']:.1f}").border = border
                    
                    # Cella priorità con colore
                    priority_cell = ws.cell(row=row_idx, column=6, value=row['Priorità'])
                    priority_cell.border = border
                    priority_cell.alignment = Alignment(horizontal="center", vertical="center")
                    
                    if row['Priorità'] == 'Estrema':
                        priority_cell.fill = PatternFill(start_color="FFE4E1", end_color="FFE4E1", fill_type="solid")
                        priority_cell.font = Font(bold=True, color="8B0000")
                    elif row['Priorità'] == 'Alta':
                        priority_cell.fill = PatternFill(start_color="FFE4B5", end_color="FFE4B5", fill_type="solid")
                        priority_cell.font = Font(bold=True, color="FF8C00")
                    elif row['Priorità'] == 'Media':
                        priority_cell.fill = PatternFill(start_color="FFFACD", end_color="FFFACD", fill_type="solid")
                        priority_cell.font = Font(bold=True, color="FFD700")
                    else:
                        priority_cell.fill = PatternFill(start_color="90EE90", end_color="90EE90", fill_type="solid")
                        priority_cell.font = Font(bold=True, color="006400")
                    
                    ws.cell(row=row_idx, column=7, value=row['Contromisura']).border = border
                    ws.cell(row=row_idx, column=8, value=row['Stato']).border = border
                    ws.cell(row=row_idx, column=9, value=row['Data scadenza']).border = border
                    
                    # Allineamento centrale per alcune colonne
                    for col in [1, 3, 4, 5, 6, 8, 9]:
                        ws.cell(row=row_idx, column=col).alignment = Alignment(horizontal="center", vertical="center")
                
                # Larghezza colonne
                ws.column_dimensions['A'].width = 8
                ws.column_dimensions['B'].width = 40
                ws.column_dimensions['C'].width = 12
                ws.column_dimensions['D'].width = 10
                ws.column_dimensions['E'].width = 15
                ws.column_dimensions['F'].width = 12
                ws.column_dimensions['G'].width = 35
                ws.column_dimensions['H'].width = 15
                ws.column_dimensions['I'].width = 15
                
                # Aggiungi foglio riepilogo
                ws2 = wb.create_sheet("Riepilogo")
                
                # Titolo riepilogo
                ws2.merge_cells('A1:B1')
                ws2['A1'] = 'RIEPILOGO RISCHI PER PRIORITÀ'
                ws2['A1'].font = Font(bold=True, size=16, color="DC143C")
                ws2['A1'].alignment = Alignment(horizontal="center", vertical="center")
                
                # Conta rischi
                priority_counts = st.session_state.df['Priorità'].value_counts()
                
                # Header riepilogo
                ws2['A3'] = 'Priorità'
                ws2['B3'] = 'Numero Rischi'
                ws2['A3'].font = header_font
                ws2['A3'].fill = header_fill
                ws2['B3'].font = header_font
                ws2['B3'].fill = header_fill
                
                # Dati riepilogo
                row = 4
                for priority in ['Estrema', 'Alta', 'Media', 'Bassa']:
                    ws2[f'A{row}'] = priority
                    ws2[f'B{row}'] = priority_counts.get(priority, 0)
                    row += 1
                
                # Totale
                ws2[f'A{row}'] = 'TOTALE'
                ws2[f'B{row}'] = len(st.session_state.df)
                ws2[f'A{row}'].font = Font(bold=True)
                ws2[f'B{row}'].font = Font(bold=True)
                
                # Larghezza colonne riepilogo
                ws2.column_dimensions['A'].width = 15
                ws2.column_dimensions['B'].width = 15
                
                # Salva Excel
                excel_buffer = BytesIO()
                wb.save(excel_buffer)
                excel_buffer.seek(0)
                
                st.download_button(
                    label="⬇️ Scarica Report Excel",
                    data=excel_buffer,
                    file_name=f"risk_assessment_report_{date.today()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
                st.success("Excel generato con successo!")
                
            except ImportError:
                st.error("Libreria openpyxl non disponibile. Installa con: pip install openpyxl")
            except Exception as e:
                st.error(f"Errore nella generazione Excel: {str(e)}")