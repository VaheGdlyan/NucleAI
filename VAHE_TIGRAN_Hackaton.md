# HackAtom 2025 — Vahe & Tigran Mission Brief
### RAG Chatbot + Streamlit Data Dashboard
**Deadline: May 26, 10:00 AM | Stack: Python · Streamlit · LangChain · FAISS · OpenAI**

---

## 0. What You Are Building — The Big Picture

You are building **two connected things** inside one Streamlit app:

1. **A RAG (Retrieval-Augmented Generation) chatbot** — a smart AI assistant that answers questions about nuclear energy, radiation safety, and Armenia's energy situation. It doesn't just use a generic LLM; it reads from a curated knowledge base of IAEA documents and data you provide. When the jury asks "Is nuclear safe for Armenia?", the bot answers with citations from real sources, not hallucinations.

2. **An interactive data dashboard** — Streamlit graphs and charts that visualize Armenia's energy mix, CO₂ comparisons, radiation dose comparisons, and nuclear application statistics. These are clickable, filterable, and look professional.

**Why RAG and not just ChatGPT?**  
Because RAG grounds the AI in *your specific documents*. You feed it IAEA PDFs, Armenia energy statistics, radiation data. When a jury member asks something, the system searches your documents first, pulls the relevant chunks, and gives the LLM that context to answer. The LLM never makes things up beyond what's in your knowledge base. This is scientifically credible and impressive to judges.

---

## 1. Project Structure

Create this folder structure immediately:

```
hackatom/
├── app.py                        # Main Streamlit entry point
├── requirements.txt              # All dependencies
│
├── rag/
│   ├── __init__.py
│   ├── ingestion.py              # Load + chunk + embed documents
│   ├── retriever.py              # FAISS vector store + similarity search
│   ├── chain.py                  # LangChain RAG chain definition
│   └── prompts.py                # System prompts and templates
│
├── data/
│   ├── documents/                # Raw source files (PDFs, txt, md)
│   │   ├── iaea_nuclear_safety.txt
│   │   ├── armenia_energy_stats.txt
│   │   ├── radiation_doses.txt
│   │   └── nuclear_medicine_facts.txt
│   ├── faiss_index/              # Auto-generated vector index (gitignore this)
│   └── charts_data.py            # All chart data as Python dicts
│
├── components/
│   ├── chatbot_ui.py             # Chat interface component
│   ├── energy_charts.py          # All Streamlit chart functions
│   └── sidebar.py                # Navigation + controls
│
└── .env                          # API keys (never commit this)
```

---

## 2. Dependencies — requirements.txt

Create this file first and run `pip install -r requirements.txt`:

```
streamlit==1.35.0
langchain==0.2.0
langchain-openai==0.1.0
langchain-community==0.2.0
faiss-cpu==1.8.0
openai==1.30.0
python-dotenv==1.0.0
plotly==5.22.0
pandas==2.2.0
tiktoken==0.7.0
pypdf==4.2.0
```

**What each package does:**
- `streamlit` — the UI framework. Turns Python into a web app instantly.
- `langchain` — the orchestration framework. Connects LLM + retriever + prompts.
- `langchain-openai` — OpenAI bindings for LangChain.
- `faiss-cpu` — Facebook's vector similarity search. This is your local vector database. Fast, no server needed.
- `openai` — to call GPT-4o or GPT-3.5-turbo for generating answers.
- `pypdf` — reads PDF files if you have IAEA PDFs.
- `tiktoken` — counts tokens so chunks don't exceed model limits.
- `plotly` — interactive charts inside Streamlit.
- `python-dotenv` — loads your `.env` file for API keys.

---

## 3. The Knowledge Base — data/documents/

This is the soul of the RAG system. You need to create text files with real facts. The AI will search these when answering questions.

### File 1: data/documents/iaea_nuclear_safety.txt

```
IAEA Nuclear Safety — Key Facts for Public Communication

1. RADIATION BASICS
Nuclear power plants do not explode like atomic bombs. The physics are fundamentally different.
A nuclear bomb requires highly enriched uranium (>90%). Power plant fuel is only 3-5% enriched.
The Chernobyl accident happened due to a combination of design flaws specific to RBMK reactors 
and operator error during an unauthorized experiment. Modern reactors have passive safety systems.
The Fukushima accident killed zero people from radiation. The evacuation itself caused 
approximately 2,202 indirect deaths from stress and disruption.

2. RADIATION DOSE CONTEXT (in millisieverts, mSv)
- Eating one banana: 0.0001 mSv (contains natural potassium-40)
- Dental X-ray: 0.005 mSv
- Chest X-ray: 0.1 mSv
- Flight from London to New York: 0.08 mSv
- Annual background radiation globally: 2.4 mSv average
- Living within 50km of a nuclear plant (annual): 0.00009 mSv
- Smoking one pack of cigarettes daily for a year: 70 mSv
- Chernobyl exclusion zone today (center): ~0.5 mSv/hour
- Regulatory limit for radiation workers: 20 mSv/year

3. NUCLEAR POWER SAFETY RECORD (deaths per TWh of electricity produced)
- Coal: 24.6 deaths per TWh
- Oil: 18.4 deaths per TWh  
- Natural gas: 2.8 deaths per TWh
- Rooftop solar: 0.44 deaths per TWh (installation falls)
- Wind: 0.15 deaths per TWh
- Nuclear: 0.07 deaths per TWh
Nuclear is statistically the safest form of energy production in human history.

4. WASTE MANAGEMENT
All the high-level nuclear waste ever produced by civilian power plants in the US 
would fit on a single football field stacked 10 meters high.
Nuclear waste does not leak into the environment under normal storage conditions.
Finland has built the world's first permanent geological repository (Onkalo) 500m underground.

5. IAEA SAFEGUARDS
The IAEA conducts regular inspections of all member state nuclear facilities.
Armenia's Metsamor plant operates under IAEA safeguards.
The Nuclear Non-Proliferation Treaty (NPT) has 191 member states.
```

### File 2: data/documents/armenia_energy_stats.txt

```
Armenia Energy Statistics and Nuclear Situation

1. CURRENT ENERGY MIX (2023 data)
Armenia total electricity generation: approximately 8.5 TWh/year
- Nuclear (Metsamor NPP): ~40% of total generation (~3.4 TWh)
- Hydropower: ~30% (~2.5 TWh)
- Natural gas thermal: ~25% (~2.1 TWh)
- Solar and wind: ~5% (~0.4 TWh, rapidly growing)

2. METSAMOR NUCLEAR POWER PLANT
Location: Metsamor, Armavir Province, 36km west of Yerevan
Reactor type: VVER-440 (Soviet-era pressurized water reactor)
Current operating unit: Unit 2 (Unit 1 shut down 1989 after Spitak earthquake)
Installed capacity: 407.5 MW
Annual generation: ~2.3-2.7 TWh
Operational since: 1980 (Unit 2)
Current license extended to: 2026 (extension discussions ongoing)
Operator: Armenian Nuclear Power Plant CJSC

3. ENERGY SECURITY CONTEXT
Armenia is a landlocked country bordered by Turkey (trade embargo), Azerbaijan (conflict),
with access only through Georgia and Iran.
Energy independence is a national security priority.
Without Metsamor, Armenia would need to import significantly more natural gas from Russia/Iran.
Electricity prices would increase an estimated 40-60% without nuclear in the mix.

4. GRID STABILITY
Armenia's grid benefits from nuclear baseload power.
Nuclear provides constant, weather-independent power unlike solar/wind.
The hydro plants in Armenia depend on seasonal water levels.
Peak demand occurs in winter when hydro is less reliable.

5. CANCER AND HEALTH IN ARMENIA
Armenia has above-average cancer rates compared to EU average.
Access to nuclear medicine diagnostics (PET scans, scintigraphy) remains limited.
Yerevan has limited radiotherapy infrastructure.
Nuclear medicine could significantly improve cancer diagnosis rates in Armenia.

6. FUTURE PLANS
The Armenian government has expressed interest in small modular reactors (SMRs).
Discussions have included Russian ROSATOM VVER-1200 and US NuScale SMR designs.
Solar capacity target: 1 GW by 2030 (from near-zero today).
The new energy strategy aims for 15% renewables by 2030.
```

### File 3: data/documents/radiation_doses.txt

```
Radiation Dose Comparison Data — Public Education Reference

NATURAL RADIATION SOURCES (everyone receives this):
- Cosmic radiation at sea level: 0.24 mSv/year
- Terrestrial radiation (ground, rocks): 0.28 mSv/year
- Internal radiation (from food/water): 0.29 mSv/year
- Radon gas inhalation: 1.26 mSv/year (highly variable by location)
- Average global background total: ~2.4 mSv/year

COMMON MEDICAL PROCEDURES:
- Dental X-ray (bitewing): 0.005 mSv
- Chest X-ray (PA view): 0.02-0.1 mSv
- Mammogram: 0.4 mSv
- Abdominal CT scan: 8 mSv
- Full-body PET scan: 14 mSv
- Cardiac catheterization: 7 mSv

EVERYDAY ACTIVITIES:
- Eating one banana: 0.0001 mSv
- Living in a brick/concrete building (vs wood): 0.07 mSv/year extra
- Transatlantic flight (8 hours): 0.08 mSv
- Living in Denver, Colorado vs sea level: 1.5 mSv/year extra (altitude)
- Smoking 1.5 packs/day for a year: ~160 mSv

NUCLEAR INDUSTRY:
- Living within 80km of a nuclear plant (annual): 0.00009 mSv
- Nuclear power plant worker (annual average): 1-2 mSv
- Regulatory limit for radiation workers: 20 mSv/year
- Regulatory limit for public from nuclear facilities: 1 mSv/year

ACCIDENT CONTEXTS:
- Chernobyl exclusion zone perimeter today: 0.001-0.003 mSv/hour
- Chernobyl center (reactor building area): 0.5-1 mSv/hour
- Fukushima exclusion zone (most areas today): normal background
- Hiroshima/Nagasaki: acute doses of 2,000-10,000 mSv in seconds

HEALTH THRESHOLDS:
- No proven health effect below: 100 mSv (acute dose)
- Radiation sickness threshold: 1,000 mSv (acute)
- LD50 (lethal dose for 50%): ~4,000 mSv (acute, no treatment)
```

### File 4: data/documents/nuclear_medicine_facts.txt

```
Nuclear Medicine and Non-Energy Applications of Nuclear Technology

1. NUCLEAR MEDICINE — DIAGNOSTICS
PET (Positron Emission Tomography) scans use radioactive tracers to detect:
- Cancer with 95%+ accuracy at early stages
- Heart disease: measuring blood flow and heart muscle function
- Brain disorders: Alzheimer's, epilepsy, Parkinson's disease
The radiotracer used in PET scans (FDG) has a half-life of 110 minutes — it's gone from the body in hours.
SPECT (Single Photon Emission CT) is cheaper than PET and used for bone, kidney, thyroid imaging.
Technetium-99m is the most widely used medical isotope — used in 40 million procedures per year globally.

2. NUCLEAR MEDICINE — THERAPY
Iodine-131 therapy: treats thyroid cancer and hyperthyroidism with targeted radiation.
Cure rate for thyroid cancer with I-131: >95% for differentiated thyroid cancer.
Lutetium-177 DOTATATE: new targeted therapy for neuroendocrine tumors.
Brachytherapy: tiny radioactive seeds placed inside or next to tumors (prostate cancer).

3. FOOD IRRADIATION AND AGRICULTURE
Gamma irradiation kills bacteria (Salmonella, E.coli) in food without making food radioactive.
Used in 60+ countries. Approved by WHO, FDA, IAEA.
The food itself does NOT become radioactive — radiation passes through, kills pathogens.
Radiation mutation breeding: creating new crop varieties by exposing seeds to radiation.
Over 3,200 new crop varieties developed this way — including disease-resistant wheat, rice.
Sterile Insect Technique (SIT): male insects are sterilized with radiation, released to reduce pest populations.
Used to eradicate screwworm fly from North America (saved $900M/year in livestock losses).

4. INDUSTRIAL NON-DESTRUCTIVE TESTING (NDT)
Industrial radiography uses X-rays and gamma rays to inspect welds, pipes, aircraft parts without cutting them.
Detects cracks, voids, and defects invisible to the naked eye.
Used in: aerospace, oil & gas pipelines, construction, automotive manufacturing.
Nuclear gauges: measure density and moisture in soil and asphalt for construction quality control.

5. WATER TREATMENT AND ENVIRONMENTAL MONITORING
Radiation can disinfect drinking water and wastewater more effectively than chlorine.
Used in some countries to treat sewage sludge, making it safe for agricultural use.
Nuclear isotopes used as tracers to track water flow in underground aquifers.
Can detect environmental pollution sources and track oil spill movement.

6. SPACE AND SCIENTIFIC RESEARCH
Radioisotope Thermoelectric Generators (RTGs) power spacecraft like Voyager, Cassini, New Horizons.
Without nuclear power, space exploration beyond Mars is nearly impossible (too far from Sun for solar panels).
Neutron beams from research reactors used to study materials, drug design, cultural artifacts.
```

---

## 4. RAG System — Core Implementation

### 4.1 rag/ingestion.py — Load and Chunk Documents

```python
import os
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

DOCUMENTS_DIR = Path("data/documents")
FAISS_INDEX_PATH = "data/faiss_index"

def load_documents():
    """Load all text and PDF files from the documents directory."""
    documents = []
    
    for file_path in DOCUMENTS_DIR.iterdir():
        if file_path.suffix == ".txt":
            loader = TextLoader(str(file_path), encoding="utf-8")
            docs = loader.load()
            # Add source metadata so we can cite it later
            for doc in docs:
                doc.metadata["source"] = file_path.name
            documents.extend(docs)
        
        elif file_path.suffix == ".pdf":
            loader = PyPDFLoader(str(file_path))
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = file_path.name
            documents.extend(docs)
    
    print(f"Loaded {len(documents)} document sections")
    return documents


def chunk_documents(documents):
    """
    Split documents into smaller chunks for embedding.
    
    Why chunking? LLMs have token limits. We can't feed 50 pages at once.
    We split into ~500 character chunks with 50 character overlap so
    context isn't lost at boundaries.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,        # Each chunk ~500 characters
        chunk_overlap=50,      # Overlap prevents losing context at splits
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]  # Prefer splitting on paragraphs
    )
    
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks


def build_vector_store(chunks):
    """
    Embed all chunks and store in FAISS.
    
    Embedding converts text into a vector (list of ~1536 numbers).
    Similar texts get similar vectors. FAISS lets us search by similarity.
    
    This runs ONCE and saves to disk. Don't re-run every time.
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    print("Building FAISS index... (this takes ~30 seconds)")
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Save to disk so we don't rebuild every app restart
    vector_store.save_local(FAISS_INDEX_PATH)
    print(f"FAISS index saved to {FAISS_INDEX_PATH}")
    
    return vector_store


def load_or_build_index():
    """
    Smart loader: use existing index if available, build if not.
    Call this from app.py on startup.
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    if os.path.exists(FAISS_INDEX_PATH):
        print("Loading existing FAISS index...")
        return FAISS.load_local(
            FAISS_INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True  # Required flag for local loads
        )
    else:
        print("No index found. Building from scratch...")
        documents = load_documents()
        chunks = chunk_documents(documents)
        return build_vector_store(chunks)
```

### 4.2 rag/prompts.py — System Prompts

```python
SYSTEM_PROMPT = """You are NuclearGuide, an expert AI assistant for HackAtom Armenia 2025.
You specialize in nuclear energy, radiation safety, and Armenia's energy future.

Your knowledge comes from IAEA documents and verified Armenian energy statistics.
Always answer based on the provided context. If the context doesn't contain the answer,
say "I don't have specific data on that, but here's what I know generally:" and give
a brief general answer.

COMMUNICATION STYLE:
- Be clear, confident, and educational — not scary
- Use specific numbers and comparisons (e.g., "less radiation than a banana")  
- Always relate answers to Armenia's specific situation when relevant
- Keep answers concise: 3-5 sentences unless a detailed explanation is needed
- If you cite statistics, mention the source (IAEA, Armenian energy ministry, etc.)

NEVER:
- Claim nuclear energy has zero risks (it has very low, manageable risks)
- Dismiss concerns without addressing them
- Give medical advice or specific radiation safety procedures
"""

RAG_PROMPT_TEMPLATE = """Use the following context from our knowledge base to answer the question.

CONTEXT FROM KNOWLEDGE BASE:
{context}

QUESTION: {question}

Provide a clear, accurate answer. If the context contains specific statistics or facts
relevant to the question, use them and mention the source. Keep the answer focused and helpful.

ANSWER:"""
```

### 4.3 rag/chain.py — The RAG Chain

```python
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from .prompts import SYSTEM_PROMPT, RAG_PROMPT_TEMPLATE


def build_rag_chain(vector_store):
    """
    Build the complete RAG chain.
    
    Flow of a single question:
    1. User types question
    2. Question is embedded into a vector
    3. FAISS finds the 4 most similar document chunks
    4. Those chunks + the question are sent to GPT-4o
    5. GPT-4o generates an answer grounded in those chunks
    6. Answer is returned with source references
    """
    
    # The language model that generates answers
    llm = ChatOpenAI(
        model="gpt-4o-mini",      # Cheap and fast. Switch to gpt-4o for quality.
        temperature=0.3,           # Low temperature = more factual, less creative
        max_tokens=500             # Keep answers concise
    )
    
    # Memory: remember last 5 exchanges so users can ask follow-up questions
    memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        k=5,                       # Remember last 5 Q&A pairs
        return_messages=True,
        output_key="answer"
    )
    
    # The retriever: searches FAISS for relevant chunks
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}     # Return top 4 most relevant chunks
    )
    
    # Combine document prompt — how to format each retrieved chunk
    combine_docs_prompt = PromptTemplate(
        template=RAG_PROMPT_TEMPLATE,
        input_variables=["context", "question"]
    )
    
    # Build the full chain
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,  # We want to show citations
        combine_docs_chain_kwargs={"prompt": combine_docs_prompt},
        verbose=False
    )
    
    return chain


def ask_question(chain, question):
    """
    Ask a question and return the answer + sources.
    
    Returns:
        dict with keys: 'answer', 'sources' (list of source filenames)
    """
    try:
        result = chain.invoke({"question": question})
        
        # Extract unique source filenames for citation
        sources = list(set([
            doc.metadata.get("source", "Knowledge Base")
            for doc in result.get("source_documents", [])
        ]))
        
        return {
            "answer": result["answer"],
            "sources": sources
        }
    except Exception as e:
        return {
            "answer": f"I encountered an error: {str(e)}. Please try again.",
            "sources": []
        }
```

---

## 5. Charts — data/charts_data.py

```python
"""
All chart data in one place. Edit these numbers to update all charts.
Sources: IAEA, Armenian Energy Ministry, Our World in Data
"""

# Radiation dose comparison (millisieverts)
RADIATION_DATA = {
    "sources": [
        "Banana (one)",
        "Dental X-ray",
        "Transatlantic flight",
        "Annual from living near NPP",
        "Chest X-ray",
        "Annual background (global avg)",
        "Mammogram",
        "Abdominal CT scan",
        "Chernobyl worker (1986 avg)",
    ],
    "doses_msv": [0.0001, 0.005, 0.08, 0.00009, 0.1, 2.4, 0.4, 8, 165],
    "colors": [
        "#f1c40f", "#3498db", "#87ceeb", "#2ecc71",
        "#3498db", "#95a5a6", "#e67e22", "#e74c3c", "#8e44ad"
    ],
    "category": [
        "Food", "Medical", "Travel", "Nuclear Industry",
        "Medical", "Natural", "Medical", "Medical", "Accident"
    ]
}

# Deaths per TWh of electricity generated
SAFETY_DATA = {
    "energy_sources": ["Coal", "Oil", "Natural Gas", "Biomass", "Solar", "Wind", "Nuclear"],
    "deaths_per_twh": [24.6, 18.4, 2.8, 4.6, 0.44, 0.15, 0.07],
    "colors": ["#2c2c2c", "#8e44ad", "#f39c12", "#27ae60", "#f1c40f", "#3498db", "#e74c3c"]
}

# Armenia energy mix 2023
ARMENIA_ENERGY_MIX = {
    "sources": ["Nuclear (Metsamor)", "Hydropower", "Natural Gas", "Solar & Wind"],
    "percentages": [40, 30, 25, 5],
    "colors": ["#e74c3c", "#3498db", "#f39c12", "#2ecc71"],
    "twh": [3.4, 2.55, 2.125, 0.425]
}

# CO2 emissions by energy source (grams per kWh)
CO2_DATA = {
    "sources": ["Coal", "Natural Gas", "Biomass", "Solar PV", "Geothermal", "Nuclear", "Wind", "Hydro"],
    "grams_co2_per_kwh": [820, 490, 230, 48, 38, 12, 11, 4],
    "colors": ["#2c2c2c", "#f39c12", "#27ae60", "#f1c40f", "#e67e22", "#e74c3c", "#3498db", "#1abc9c"]
}

# Nuclear medicine impact
NUCLEAR_MEDICINE_DATA = {
    "applications": [
        "PET Scan — cancer detection",
        "SPECT — heart/bone imaging",
        "I-131 — thyroid cancer cure",
        "Brachytherapy — prostate cancer",
        "Radiation therapy — general",
    ],
    "annual_procedures_millions": [4.5, 18.0, 0.8, 1.2, 14.5],
    "success_rate_pct": [95, 92, 95, 93, 80]
}

# Suggested chatbot questions for demo
SUGGESTED_QUESTIONS = [
    "Is nuclear energy safe for Armenia?",
    "How does radiation from Metsamor compare to a dental X-ray?",
    "What would happen to electricity prices if Metsamor closed?",
    "What is nuclear medicine and can Armenia benefit from it?",
    "How does nuclear compare to coal in terms of deaths?",
    "Is the Metsamor plant safe by modern standards?",
    "What happened at Chernobyl and can it happen at Metsamor?",
    "What are Small Modular Reactors and does Armenia need them?",
]
```

---

## 6. Chart Components — components/energy_charts.py

```python
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd
from data.charts_data import (
    RADIATION_DATA, SAFETY_DATA, ARMENIA_ENERGY_MIX, CO2_DATA, NUCLEAR_MEDICINE_DATA
)

# ─── Color theme ────────────────────────────────────────────────
DARK_BG = "#0f0f0f"
CARD_BG = "#1a1a1a"
GOLD = "#d4af37"
TEXT_COLOR = "#f5f5f5"
MUTED_TEXT = "#b0b0b0"

PLOTLY_LAYOUT = dict(
    plot_bgcolor=CARD_BG,
    paper_bgcolor=DARK_BG,
    font=dict(color=TEXT_COLOR, family="Segoe UI"),
    margin=dict(l=20, r=20, t=50, b=20),
    title_font=dict(size=16, color=GOLD),
)


def render_radiation_chart():
    """Horizontal log-scale bar chart — radiation dose comparison."""
    st.markdown("### ☢️ Radiation Dose Reality Check")
    st.caption("Source: IAEA, WHO — doses in millisieverts (mSv)")
    
    df = pd.DataFrame({
        "source": RADIATION_DATA["sources"],
        "dose": RADIATION_DATA["doses_msv"],
        "category": RADIATION_DATA["category"]
    }).sort_values("dose")
    
    fig = go.Figure(go.Bar(
        x=df["dose"],
        y=df["source"],
        orientation="h",
        marker=dict(
            color=df["dose"],
            colorscale=[[0, "#2ecc71"], [0.5, "#f39c12"], [1, "#e74c3c"]],
            showscale=False
        ),
        text=[f"{d:.4f} mSv" if d < 0.01 else f"{d:.3f} mSv" for d in df["dose"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Dose: %{x:.5f} mSv<extra></extra>"
    ))
    
    fig.update_xaxes(type="log", title="Dose (mSv) — log scale", color=MUTED_TEXT)
    fig.update_yaxes(color=TEXT_COLOR)
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title="Annual radiation dose comparison",
        height=420
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Key insight callout
    st.info("💡 **Key fact:** Living next to a nuclear plant for a year gives you **0.00009 mSv** — "
            "thousands of times less than a single chest X-ray.")


def render_safety_chart():
    """Bar chart — deaths per TWh by energy source."""
    st.markdown("### 💀 Which Energy Source Kills the Most People?")
    st.caption("Deaths per TWh of electricity generated — includes accidents, air pollution, mining")
    
    df = pd.DataFrame({
        "source": SAFETY_DATA["energy_sources"],
        "deaths": SAFETY_DATA["deaths_per_twh"],
    }).sort_values("deaths", ascending=False)
    
    colors = [GOLD if src == "Nuclear" else "#555555" for src in df["source"]]
    
    fig = go.Figure(go.Bar(
        x=df["source"],
        y=df["deaths"],
        marker=dict(color=colors, line=dict(color="transparent")),
        text=[f"{d}" for d in df["deaths"]],
        textposition="outside",
        textfont=dict(color=TEXT_COLOR),
        hovertemplate="<b>%{x}</b><br>Deaths per TWh: %{y}<extra></extra>"
    ))
    
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title="Deaths per TWh of electricity (lower = safer)",
        yaxis_title="Deaths per TWh",
        height=400
    )
    fig.update_yaxes(color=MUTED_TEXT)
    fig.update_xaxes(color=TEXT_COLOR)
    
    st.plotly_chart(fig, use_container_width=True)
    st.success("✅ Nuclear has the **lowest death rate** of any energy source ever studied — including solar and wind.")


def render_armenia_energy_mix():
    """Donut chart — Armenia's current energy mix."""
    st.markdown("### 🇦🇲 Armenia's Energy Mix Today (2023)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = go.Figure(go.Pie(
            labels=ARMENIA_ENERGY_MIX["sources"],
            values=ARMENIA_ENERGY_MIX["percentages"],
            hole=0.5,
            marker=dict(colors=ARMENIA_ENERGY_MIX["colors"]),
            textinfo="label+percent",
            textfont=dict(color=TEXT_COLOR, size=12),
            hovertemplate="<b>%{label}</b><br>%{percent}<br>%{value}%<extra></extra>"
        ))
        
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title="Electricity generation share",
            showlegend=False,
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Quick stats:**")
        for i, (src, pct, twh) in enumerate(zip(
            ARMENIA_ENERGY_MIX["sources"],
            ARMENIA_ENERGY_MIX["percentages"],
            ARMENIA_ENERGY_MIX["twh"]
        )):
            color = ARMENIA_ENERGY_MIX["colors"][i]
            st.markdown(
                f'<div style="border-left: 3px solid {color}; padding: 6px 12px; margin: 8px 0;">'
                f'<strong>{src}</strong><br>{pct}% · {twh} TWh/year</div>',
                unsafe_allow_html=True
            )
        
        st.warning("⚠️ Without Metsamor, electricity prices in Armenia would rise **40-60%**.")


def render_co2_chart():
    """CO₂ emissions by energy source."""
    st.markdown("### 🌍 CO₂ Emissions per kWh Generated")
    st.caption("Lifecycle emissions including manufacturing, fuel, decommissioning")
    
    df = pd.DataFrame({
        "source": CO2_DATA["sources"],
        "co2": CO2_DATA["grams_co2_per_kwh"]
    }).sort_values("co2", ascending=False)
    
    colors = [GOLD if src == "Nuclear" else "#555555" for src in df["source"]]
    
    fig = go.Figure(go.Bar(
        x=df["source"],
        y=df["co2"],
        marker=dict(color=colors),
        text=df["co2"],
        textposition="outside",
        textfont=dict(color=TEXT_COLOR),
    ))
    
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title="Lifecycle CO₂ per kWh (g CO₂-eq/kWh)",
        yaxis_title="grams CO₂ per kWh",
        height=380
    )
    
    st.plotly_chart(fig, use_container_width=True)
```

---

## 7. Chatbot UI — components/chatbot_ui.py

```python
import streamlit as st
from data.charts_data import SUGGESTED_QUESTIONS


def init_chat_state():
    """Initialize session state for chat history."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chain" not in st.session_state:
        st.session_state.chain = None


def render_chat_header():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
        border: 1px solid #d4af37;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    ">
        <h2 style="color: #d4af37; margin: 0 0 0.5rem;">⚛️ NuclearGuide AI</h2>
        <p style="color: #b0b0b0; margin: 0; font-size: 14px;">
            Ask me anything about nuclear energy, radiation safety, or Armenia's energy future.
            My answers come from IAEA documents and verified Armenian energy statistics.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_suggested_questions():
    """Clickable suggested questions for demo."""
    st.markdown("**💬 Try asking:**")
    
    cols = st.columns(2)
    for i, question in enumerate(SUGGESTED_QUESTIONS[:6]):
        with cols[i % 2]:
            if st.button(f"→ {question}", key=f"sq_{i}", use_container_width=True):
                return question
    return None


def render_chat_message(role, content, sources=None):
    """Render a single chat message."""
    if role == "user":
        st.markdown(
            f'<div style="background:#2a2a2a; border-radius:8px; padding:12px 16px; '
            f'margin:8px 0; border-left:3px solid #d4af37;">'
            f'<strong style="color:#d4af37;">You</strong><br>'
            f'<span style="color:#f5f5f5;">{content}</span></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div style="background:#1a1a1a; border-radius:8px; padding:12px 16px; '
            f'margin:8px 0; border-left:3px solid #00d4ff;">'
            f'<strong style="color:#00d4ff;">⚛️ NuclearGuide</strong><br>'
            f'<span style="color:#f5f5f5;">{content}</span>',
            unsafe_allow_html=True
        )
        
        if sources:
            sources_text = " · ".join([s.replace(".txt", "").replace("_", " ").title() for s in sources])
            st.markdown(
                f'<div style="margin-top:8px; font-size:12px; color:#b0b0b0;">'
                f'📚 Sources: {sources_text}</div></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown('</div>', unsafe_allow_html=True)


def render_chatbot(chain):
    """Full chatbot UI. Pass in the RAG chain."""
    render_chat_header()
    
    # Suggested questions
    clicked_question = render_suggested_questions()
    
    # Display chat history
    st.markdown("---")
    for msg in st.session_state.messages:
        render_chat_message(
            msg["role"],
            msg["content"],
            msg.get("sources")
        )
    
    # Chat input
    user_input = st.chat_input("Ask about nuclear energy, radiation, or Armenia's energy future...")
    
    # Handle input (either typed or clicked suggested question)
    question = clicked_question or user_input
    
    if question and chain:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": question})
        render_chat_message("user", question)
        
        # Get answer from RAG chain
        with st.spinner("Searching knowledge base..."):
            result = chain.invoke({"question": question})
            answer = result["answer"]
            sources = list(set([
                doc.metadata.get("source", "Knowledge Base")
                for doc in result.get("source_documents", [])
            ]))
        
        # Add assistant message to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })
        render_chat_message("assistant", answer, sources)
        st.rerun()
    
    elif question and not chain:
        st.error("⚠️ AI model not loaded. Check your OpenAI API key in the .env file.")
```

---

## 8. Main App — app.py

```python
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()  # Load OPENAI_API_KEY from .env

# ─── Page config (must be first Streamlit call) ──────────────────
st.set_page_config(
    page_title="HackAtom Armenia 2025",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Dark theme override ─────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f0f0f; color: #f5f5f5; }
    .stSidebar { background-color: #1a1a1a; }
    .stButton > button {
        background: transparent;
        color: #d4af37;
        border: 1px solid #d4af37;
        border-radius: 8px;
        font-size: 13px;
        text-align: left;
    }
    .stButton > button:hover { background: #d4af3722; }
    .stTextInput > div > input { background: #1a1a1a; color: #f5f5f5; }
    div[data-testid="stChatInput"] textarea { background: #1a1a1a; color: #f5f5f5; }
    h1, h2, h3 { color: #d4af37 !important; }
</style>
""", unsafe_allow_html=True)


# ─── Initialize RAG system (cached — runs only once) ─────────────
@st.cache_resource
def load_rag_system():
    """Load FAISS index and build chain. Cached so it only runs once."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return None
    
    try:
        from rag.ingestion import load_or_build_index
        from rag.chain import build_rag_chain
        
        vector_store = load_or_build_index()
        chain = build_rag_chain(vector_store)
        return chain
    except Exception as e:
        st.error(f"Failed to load AI: {e}")
        return None


# ─── Navigation ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("# ⚛️ HackAtom 2025")
    st.markdown("*Armenia's Nuclear Future*")
    st.markdown("---")
    
    page = st.radio(
        "Navigate:",
        ["🤖 AI Assistant", "📊 Energy Data", "☢️ Radiation Reality", "🏥 Nuclear Applications"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
    <small style="color:#b0b0b0;">
    Data sources:<br>
    • IAEA (iaea.org)<br>
    • Armenian Energy Ministry<br>
    • Our World in Data<br>
    • WHO Radiation Safety
    </small>
    """, unsafe_allow_html=True)


# ─── Load AI chain ───────────────────────────────────────────────
chain = load_rag_system()


# ─── Page routing ────────────────────────────────────────────────
if page == "🤖 AI Assistant":
    from components.chatbot_ui import render_chatbot, init_chat_state
    init_chat_state()
    render_chatbot(chain)

elif page == "📊 Energy Data":
    from components.energy_charts import render_armenia_energy_mix, render_co2_chart, render_safety_chart
    st.title("Armenia's Energy Landscape")
    render_armenia_energy_mix()
    st.markdown("---")
    render_safety_chart()
    st.markdown("---")
    render_co2_chart()

elif page == "☢️ Radiation Reality":
    from components.energy_charts import render_radiation_chart
    st.title("Radiation: Facts vs Fear")
    render_radiation_chart()

elif page == "🏥 Nuclear Applications":
    st.title("Nuclear Technology Beyond Energy")
    # Render the non-energy applications card grid
    from data.charts_data import NUCLEAR_MEDICINE_DATA
    
    apps = [
        {"icon": "🏥", "title": "Cancer Detection", "desc": "PET scans detect cancer with 95%+ accuracy at early stages. Armenia has high oncology rates but limited diagnostic access.", "stat": "40M procedures/year globally"},
        {"icon": "⚕️", "title": "Thyroid Cancer Cure", "desc": "Iodine-131 therapy cures differentiated thyroid cancer in over 95% of cases. Safe, targeted, no surgery needed.", "stat": "95% cure rate"},
        {"icon": "🌾", "title": "Food Safety", "desc": "Gamma irradiation eliminates Salmonella and E.coli from food without making it radioactive. Used in 60+ countries.", "stat": "WHO approved"},
        {"icon": "🌱", "title": "Better Crops", "desc": "Radiation mutation breeding created 3,200+ new crop varieties — disease-resistant wheat and rice that feed millions.", "stat": "3,200+ new varieties"},
        {"icon": "🔧", "title": "Industrial NDT", "desc": "X-ray and gamma inspection of welds and pipelines detects invisible defects. Used in aerospace, oil & gas, construction.", "stat": "No cutting required"},
        {"icon": "🚀", "title": "Space Exploration", "desc": "Radioisotope generators power Voyager and New Horizons. Without nuclear, deep space exploration is impossible.", "stat": "Only option past Mars"},
    ]
    
    cols = st.columns(3)
    for i, app in enumerate(apps):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:#1a1a1a; border:1px solid #333; border-radius:12px;
                        padding:1.2rem; margin-bottom:1rem; min-height:200px;">
                <div style="font-size:2rem; margin-bottom:0.5rem;">{app['icon']}</div>
                <h4 style="color:#d4af37; margin:0 0 0.5rem;">{app['title']}</h4>
                <p style="color:#b0b0b0; font-size:13px; margin-bottom:0.75rem;">{app['desc']}</p>
                <div style="background:#d4af3722; border:1px solid #d4af3755; border-radius:6px;
                            padding:6px 10px; font-size:12px; color:#d4af37; font-weight:600;">
                    📊 {app['stat']}
                </div>
            </div>
            """, unsafe_allow_html=True)
```

---

## 9. Environment Setup — .env file

Create this file in the root. **Never commit it to GitHub.**

```
OPENAI_API_KEY=your_openai_api_key_here
```

Add to `.gitignore`:
```
.env
data/faiss_index/
__pycache__/
*.pyc
```

---

## 10. How to Run

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your OpenAI API key to .env

# 4. Build the FAISS index (run once)
python -c "from rag.ingestion import load_or_build_index; load_or_build_index()"

# 5. Run the app
streamlit run app.py
```

---

## 11. Google Antigravity IDE Agent — How to Use It

Use the Antigravity agent to accelerate each step. Here are exact prompts:

| Task | Paste this into Antigravity agent |
|------|-----------------------------------|
| Scaffold project | "Create a Python project structure for a Streamlit RAG chatbot with LangChain and FAISS. Show me the folder structure and requirements.txt" |
| Debug FAISS | "I'm getting this error with FAISS.load_local: [paste error]. How do I fix it?" |
| Add a chart | "Add a Plotly stacked bar chart to my Streamlit app showing Armenia's energy mix over time (2010, 2015, 2020, 2023)" |
| Style a component | "Make this Streamlit component match a dark theme with gold (#d4af37) accents. Current code: [paste code]" |
| Test the chain | "Write a test script that sends 5 questions to my LangChain RAG chain and prints the answers + source documents" |

---

## 12. Pitch Notes for Jury Demo

**When demoing the chatbot:**
1. Ask: *"Is nuclear safe for Armenia?"* — show that it cites IAEA sources
2. Ask: *"How does Metsamor compare to Chernobyl?"* — show nuanced, factual answer
3. Ask: *"What happens to electricity prices without nuclear?"* — show Armenian-specific data

**When demoing the charts:**
1. Show radiation chart first — "a banana gives more radiation than living near a nuclear plant"
2. Show deaths-per-TWh chart — nuclear is statistically safer than solar
3. Show Armenia energy mix — without Metsamor, 40% of electricity disappears

**Closing line:** *"This isn't a prototype. Point this at any country's energy documents, and it becomes their nuclear policy assistant."*
