"""
The Nuclear Hub — FastAPI Backend
Phase 3 & 4: RAG Pipeline Integration & Final API
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI

# ── Load environment variables from .env ──────────────────────────────────────
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("⚠️  WARNING: OPENAI_API_KEY not found in .env — RAG pipeline will not work.")

# ── Initialize AI Clients ─────────────────────────────────────────────────────
# We use the native ChromaDB client and official OpenAI client to avoid any 
# heavy/buggy wrapper dependencies (like local torch).

# 1. OpenAI Client for generating chat completions
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# 2. ChromaDB Persistent Client & Collection for document retrieval
try:
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=OPENAI_API_KEY,
        model_name="text-embedding-3-small"
    )
    # Get the collection we populated in Phase 2
    collection = chroma_client.get_collection(
        name="nuclear_hub",
        embedding_function=openai_ef
    )
    db_status = "active"
except Exception as e:
    print(f"⚠️  WARNING: Failed to connect to ChromaDB: {e}")
    collection = None
    db_status = f"error: {str(e)}"

# ── Prompts ───────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are NuclearGuide, an expert AI assistant for the HackAtom 2026 National Stage.
You specialize in nuclear energy, radiation safety, and Armenia's energy future.

Your knowledge strictly comes from the provided context (IAEA documents and verified Armenian energy statistics).
Always answer based on the provided context. If the context doesn't contain the answer,
say "I don't have specific data on that, but here's what I know generally:" and give
a brief, objective general answer.

COMMUNICATION STYLE:
- Be clear, confident, and educational — never fearmongering.
- Use specific numbers and comparisons (e.g., "less radiation than a banana") when available in the context.
- Always relate answers to Armenia's specific situation when relevant.
- Keep answers concise: 3-5 sentences unless a detailed explanation is required.
- If you cite statistics, mention the source (e.g., IAEA, Armenian energy ministry).

NEVER:
- Claim nuclear energy has zero risks (it has very low, strictly managed risks).
- Dismiss safety concerns without addressing them with facts.
- Give medical advice or specific radiation safety procedures.
"""

RAG_PROMPT_TEMPLATE = """Use the following context from our knowledge base to answer the question.

CONTEXT FROM KNOWLEDGE BASE:
{context}

---
QUESTION: {question}

Provide a clear, accurate answer. If the context contains specific statistics or facts
relevant to the question, use them. Keep the answer focused and helpful.
"""

# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="The Nuclear Hub API",
    description="AI & Data backend for The Nuclear Hub — HackAtom 2026 National Stage",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ── CORS — allow all origins so Davit's frontend is never blocked ─────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────────────────────
# Pydantic Schemas
# ─────────────────────────────────────────────────────────────────────────────

class MythbusterRequest(BaseModel):
    query: str

    class Config:
        json_schema_extra = {
            "example": {
                "query": "Is nuclear energy safe for Armenia?"
            }
        }

class MythbusterResponse(BaseModel):
    answer: str
    sources: List[str] = []

    class Config:
        json_schema_extra = {
            "example": {
                "answer": "According to the IAEA safety standards...",
                "sources": ["Armenia 2022.pdf"]
            }
        }

class RadiationDataPoint(BaseModel):
    source: str
    dose_usv: float
    category: str
    context: str

class RadiationDataResponse(BaseModel):
    unit: str
    data: List[RadiationDataPoint]

class EnergySharePoint(BaseModel):
    source: str
    percentage: float
    twh: float
    color: str

class SafetyRecordPoint(BaseModel):
    source: str
    deaths_per_twh: float
    color: str

class CarbonFootprintPoint(BaseModel):
    source: str
    grams_co2_per_kwh: float
    color: str

class EnergySafetyResponse(BaseModel):
    armenia_mix: List[EnergySharePoint]
    safety_records: List[SafetyRecordPoint]
    carbon_footprints: List[CarbonFootprintPoint]

class MedicalAppPoint(BaseModel):
    application: str
    annual_procedures_millions: float
    success_rate_pct: float
    context: str

class BeyondEnergyResponse(BaseModel):
    medical_apps: List[MedicalAppPoint]
    agricultural_facts: List[str]
    space_facts: List[str]


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    """Health check — confirms the API is alive."""
    return {
        "status": "ok",
        "service": "The Nuclear Hub API",
        "version": "1.0.0",
        "phase": "3/4 — Full RAG Integration",
        "docs": "/docs",
    }


@app.get("/api/health", tags=["Health"])
def health_check():
    """Detailed health check including DB and AI client status."""
    return {
        "status": "ok",
        "openai_key_loaded": bool(OPENAI_API_KEY),
        "chroma_db_status": db_status,
        "rag_pipeline": "active" if db_status == "active" and OPENAI_API_KEY else "inactive",
    }


@app.post("/api/mythbuster", response_model=MythbusterResponse, tags=["RAG Chatbot"])
def mythbuster(request: MythbusterRequest):
    """
    Nuclear Myth-Buster chatbot endpoint.

    Retrieves context from the local ChromaDB vector store based on the user's query,
    and generates an answer using OpenAI's gpt-4o-mini grounded in that context.
    """
    if not collection or not openai_client:
        raise HTTPException(status_code=500, detail="RAG Pipeline is not properly initialized. Check API keys and Database.")

    try:
        # 1. Retrieve the top 4 most relevant chunks from ChromaDB
        results = collection.query(
            query_texts=[request.query],
            n_results=4
        )
        
        # 2. Extract texts and sources from the results
        retrieved_texts = results["documents"][0]
        retrieved_metadatas = results["metadatas"][0]
        
        # Build the combined context string
        context_string = "\n\n".join(retrieved_texts)
        
        # Build a unique list of source filenames to return to the frontend
        unique_sources = list(set([meta.get("source", "Unknown Document") for meta in retrieved_metadatas]))

        # 3. Call OpenAI for the chat completion
        prompt_content = RAG_PROMPT_TEMPLATE.format(context=context_string, question=request.query)
        
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3, # Low temperature for more factual, less creative answers
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_content}
            ]
        )
        
        generated_answer = response.choices[0].message.content

        # 4. Return the answer and citations
        return MythbusterResponse(
            answer=generated_answer,
            sources=unique_sources
        )

    except Exception as e:
        print(f"Error during RAG pipeline execution: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/api/radiation-data", response_model=RadiationDataResponse, tags=["Data"])
def get_radiation_data():
    """
    Returns a curated list of radiation dose data points for the interactive dashboard.
    """
    data_points = [
        RadiationDataPoint(
            source="Eating one banana",
            dose_usv=0.1,
            category="Food",
            context="Bananas contain natural potassium-40. Perfectly safe.",
        ),
        RadiationDataPoint(
            source="Dental X-ray",
            dose_usv=5.0,
            category="Medical",
            context="A standard bitewing dental X-ray exposes you to 5 μSv.",
        ),
        RadiationDataPoint(
            source="Transatlantic flight (8 hrs)",
            dose_usv=80.0,
            category="Travel",
            context="Higher altitude means less atmospheric shielding from cosmic rays.",
        ),
        RadiationDataPoint(
            source="Living near a nuclear plant (annual)",
            dose_usv=0.09,
            category="Nuclear Industry",
            context="Living within 80 km of an NPP for an entire year: 0.09 μSv — less than eating one banana.",
        ),
        RadiationDataPoint(
            source="Abdominal CT scan",
            dose_usv=8_000.0,
            category="Medical",
            context="A full abdominal CT scan delivers ~8,000 μSv (8 mSv). Still well below any health-effect threshold.",
        ),
    ]

    return RadiationDataResponse(
        unit="μSv (Microsieverts)",
        data=data_points,
    )


@app.get("/api/energy-safety", response_model=EnergySafetyResponse, tags=["Data"])
def get_energy_safety_data():
    """
    Returns data points for Armenia's energy mix, global safety comparisons, and carbon footprint comparisons.
    """
    armenia_mix = [
        EnergySharePoint(source="Nuclear (Metsamor)", percentage=40.0, twh=3.4, color="#d4af37"),
        EnergySharePoint(source="Hydropower", percentage=30.0, twh=2.55, color="#3498db"),
        EnergySharePoint(source="Natural Gas", percentage=25.0, twh=2.125, color="#f39c12"),
        EnergySharePoint(source="Solar & Wind", percentage=5.0, twh=0.425, color="#2ecc71"),
    ]

    safety_records = [
        SafetyRecordPoint(source="Coal", deaths_per_twh=24.6, color="#2c2c2c"),
        SafetyRecordPoint(source="Oil", deaths_per_twh=18.4, color="#8e44ad"),
        SafetyRecordPoint(source="Natural Gas", deaths_per_twh=2.8, color="#f39c12"),
        SafetyRecordPoint(source="Biomass", deaths_per_twh=4.6, color="#27ae60"),
        SafetyRecordPoint(source="Solar", deaths_per_twh=0.44, color="#3498db"),
        SafetyRecordPoint(source="Wind", deaths_per_twh=0.15, color="#3498db"),
        SafetyRecordPoint(source="Nuclear", deaths_per_twh=0.07, color="#d4af37"),
    ]

    carbon_footprints = [
        CarbonFootprintPoint(source="Coal", grams_co2_per_kwh=820.0, color="#2c2c2c"),
        CarbonFootprintPoint(source="Natural Gas", grams_co2_per_kwh=490.0, color="#f39c12"),
        CarbonFootprintPoint(source="Biomass", grams_co2_per_kwh=230.0, color="#27ae60"),
        CarbonFootprintPoint(source="Solar PV", grams_co2_per_kwh=48.0, color="#3498db"),
        CarbonFootprintPoint(source="Geothermal", grams_co2_per_kwh=38.0, color="#e67e22"),
        CarbonFootprintPoint(source="Nuclear", grams_co2_per_kwh=12.0, color="#d4af37"),
        CarbonFootprintPoint(source="Wind", grams_co2_per_kwh=11.0, color="#3498db"),
        CarbonFootprintPoint(source="Hydro", grams_co2_per_kwh=4.0, color="#1abc9c"),
    ]

    return EnergySafetyResponse(
        armenia_mix=armenia_mix,
        safety_records=safety_records,
        carbon_footprints=carbon_footprints
    )


@app.get("/api/beyond-energy", response_model=BeyondEnergyResponse, tags=["Data"])
def get_beyond_energy_data():
    """
    Returns data points for nuclear technology applications in medicine, agriculture, and space exploration.
    """
    medical_apps = [
        MedicalAppPoint(
            application="PET Scans (early cancer detection)",
            annual_procedures_millions=4.5,
            success_rate_pct=95.0,
            context="Enables early stage detection with over 95% accuracy. Tracer half-life is only 110 minutes.",
        ),
        MedicalAppPoint(
            application="SPECT Imaging (heart/bone diagnostics)",
            annual_procedures_millions=18.0,
            success_rate_pct=92.0,
            context="Widely used bone and organ imaging. Technetium-99m is used in 40M diagnostic procedures annually.",
        ),
        MedicalAppPoint(
            application="Iodine-131 targeted therapy (thyroid cancer)",
            annual_procedures_millions=0.8,
            success_rate_pct=95.0,
            context="Cure rates for differentiated thyroid cancer exceed 95% with targeted radioactive iodine therapy.",
        ),
        MedicalAppPoint(
            application="Brachytherapy (prostate/cervical cancer)",
            annual_procedures_millions=1.2,
            success_rate_pct=93.0,
            context="Tiny radioactive seeds placed directly near tumor sites ensure maximum radiation localized to cancer.",
        ),
    ]

    agricultural_facts = [
        "Sterile Insect Technique (SIT): Male pests are sterilized using safe doses of radiation and released. This successfully eradicated the screwworm fly from North America, saving billions in livestock losses.",
        "Food Irradiation: Exposing food to controlled ionizing radiation kills 99.9% of bacteria (Salmonella, E. coli) without making the food radioactive or reducing its nutritional value.",
        "Mutation Breeding: Exposing seeds to radiation helps generate beneficial genetic variations. Over 3,200 crop varieties (such as disease-resistant wheat and rice) have been developed this way globally."
    ]

    space_facts = [
        "Radioisotope Thermoelectric Generators (RTGs): Nuclear battery generators power deep-space missions like Voyager 1, Voyager 2, Cassini, and New Horizons.",
        "Why Nuclear? Beyond Mars, sunlight is too weak for solar panels. RTGs convert heat from decaying plutonium-238 directly into stable electrical power for decades.",
        "Longevity: Voyager 1 has been operating continuously in interstellar space since 1977, communicating across billions of miles using its RTG power source."
    ]

    return BeyondEnergyResponse(
        medical_apps=medical_apps,
        agricultural_facts=agricultural_facts,
        space_facts=space_facts
    )
