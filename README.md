# 🛡️ Risk Assessment Dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Una dashboard interattiva e professionale per la gestione e valutazione dei rischi di progetto, sviluppata con Streamlit e AgGrid.

## ✨ Caratteristiche Principali

- **📊 Heat Map Interattiva**: Visualizzazione dei rischi su matrice probabilità/impatto con posizionamento preciso per valori decimali
- **📋 Tabella Dinamica**: Gestione completa dei rischi con AgGrid (aggiunta, modifica, eliminazione)
- **📈 Calcolo Automatico**: Priorità calcolate automaticamente basate su probabilità × impatto
- **📄 Export Avanzato**: Esportazione in PDF e Excel con heat map inclusa
- **💾 Persistenza Dati**: Salvataggio automatico su CSV con sincronizzazione real-time
- **🎨 UI Moderna**: Interfaccia dark theme responsive e professionale
- **⚡ Performance**: Optimizzato per gestire centinaia di rischi senza lag

## 🚀 Demo

![Risk Assessment Dashboard](https://via.placeholder.com/800x400/0d1117/DC143C?text=Risk+Assessment+Dashboard)

*Sostituisci questo placeholder con uno screenshot reale della tua dashboard*

## 📦 Installazione

### Prerequisiti

- Python 3.8 o superiore
- pip (gestore pacchetti Python)

### Installazione Rapida

1. **Clona il repository**
   ```bash
   git clone https://github.com/tuousername/risk-assessment-dashboard.git
   cd risk-assessment-dashboard
   ```

2. **Crea un ambiente virtuale** (raccomandato)
   ```bash
   python -m venv venv
   
   # Su Windows
   venv\Scripts\activate
   
   # Su macOS/Linux
   source venv/bin/activate
   ```

3. **Installa le dipendenze**
   ```bash
   pip install -r requirements.txt
   ```

4. **Avvia l'applicazione**
   ```bash
   streamlit run risk_dashboard.py
   ```

5. **Apri il browser** e vai su `http://localhost:8501`

## 📋 Requisiti

```txt
streamlit==1.32.0
streamlit-aggrid==1.0.5
pandas==2.2.0
openpyxl==3.1.2
reportlab==4.1.0
matplotlib==3.8.0
```

## 🔧 Utilizzo

### Aggiungere un Nuovo Rischio

1. Compila il form "Aggiungi Nuovo Rischio"
2. Imposta **Probabilità** e **Impatto** (scala 1-5 con incrementi 0.5)
3. La **Priorità** viene calcolata automaticamente
4. Premi **Aggiungi** per salvare

### Gestire Rischi Esistenti

- **Visualizzare**: Tutti i rischi sono mostrati nella tabella interattiva
- **Eliminare**: Spunta la checkbox "Elimina" per rimuovere rischi
- **Esportare**: Usa i pulsanti PDF/Excel per esportare i dati

### Heat Map dei Rischi

La heat map mostra visivamente i rischi posizionati secondo:
- **Asse X**: Probabilità (1-5)
- **Asse Y**: Impatto (1-5) 
- **Colori**: 
  - 🟢 Verde: Bassa (1-5)
  - 🟡 Giallo: Media (6-10)
  - 🟠 Arancione: Alta (11-15)
  - 🔴 Rosso: Estrema (16-25)

## 🏗️ Architettura

```
risk-assessment-dashboard/
├── risk_dashboard.py          # Applicazione principale
├── requirements.txt           # Dipendenze Python
├── risk_data.csv             # Database dei rischi (generato automaticamente)
├── .gitignore                # File Git ignore
├── README.md                 # Documentazione
└── screenshots/              # Screenshot per documentazione
    └── dashboard_preview.png
```

## 🎨 Personalizzazione

### Modificare i Colori del Tema

Nel file `risk_dashboard.py`, sezione CSS:

```python
# Cambia il colore principale (attualmente rosso)
color: #DC143C;  # Sostituisci con il tuo colore

# Cambia il gradiente del titolo
background: linear-gradient(135deg, #8B0000 0%, #DC143C 50%, #FF6347 100%);
```

### Modificare le Soglie di Priorità

Nella funzione `calcola_priorita()`:

```python
def calcola_priorita(valore_rischio):
    if valore_rischio >= 16:    # Modifica questa soglia
        return "Estrema"
    elif valore_rischio >= 11:  # Modifica questa soglia
        return "Alta"
    # ... etc
```

## 🤝 Contribuire

1. Fai un **Fork** del progetto
2. Crea un **branch** per la tua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** le tue modifiche (`git commit -m 'Add some AmazingFeature'`)
4. **Push** al branch (`git push origin feature/AmazingFeature`)
5. Apri una **Pull Request**

## 📊 Roadmap

- [ ] **Autenticazione utenti** e multi-tenancy
- [ ] **Dashboard analytics** con metriche avanzate
- [ ] **Notifiche automatiche** per rischi ad alta priorità
- [ ] **API REST** per integrazione con altri sistemi
- [ ] **Backup automatico** su cloud storage
- [ ] **Tema chiaro/scuro** configurabile
- [ ] **Mobile responsive** ottimizzato

## 🐛 Problemi Noti

- ⚠️ L'export PDF richiede librerie aggiuntive su alcuni sistemi
- ⚠️ La heat map potrebbe non caricare correttamente su browser molto vecchi

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 👨‍💻 Autore

**Il Tuo Nome**
- GitHub: [@tuousername](https://github.com/tuousername)
- LinkedIn: [Il Tuo Nome](https://linkedin.com/in/tuoprofilo)
- Email: tua.email@esempio.com

## 🙏 Ringraziamenti

- [Streamlit](https://streamlit.io/) per il framework web
- [AgGrid](https://github.com/PablocFonseca/streamlit-aggrid) per la tabella interattiva
- [ReportLab](https://www.reportlab.com/) per la generazione PDF
- [Matplotlib](https://matplotlib.org/) per i grafici

---

⭐ Se questo progetto ti è stato utile, lascia una stella!

## 📞 Supporto

Hai trovato un bug o hai una richiesta di feature? 
- Apri una [Issue](https://github.com/tuousername/risk-assessment-dashboard/issues)
- Contattami direttamente via email

---

<div align="center">
  <strong>Risk Assessment Dashboard</strong><br>
  Gestione professionale dei rischi di progetto
</div>