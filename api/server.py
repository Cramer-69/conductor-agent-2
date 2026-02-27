"""
FastAPI server for voice-enabled conductor agent.
Provides REST API and web interface for mobile access.
"""

import os
import sys
import uuid
from pathlib import Path

# Add conductor_agent directory to sys.path so bare internal imports work
_pkg_dir = str(Path(__file__).resolve().parent.parent)
if _pkg_dir not in sys.path:
    sys.path.insert(0, _pkg_dir)
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from conductor.agent import ConductorAgent
from voice.voice_processor import get_voice_processor
from utils.logger import logger
from config.settings import settings

# Initialize FastAPI app
app = FastAPI(
    title="Conductor Voice Agent",
    description="Voice-enabled AI assistant with persistent memory",
    version="1.0.0"
)

# Add CORS middleware for mobile access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for mobile
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services (lazy initialization to avoid startup crashes)
conductor = None
voice_processor = None

def get_conductor():
    """Lazy initialization of conductor agent."""
    global conductor
    if conductor is None:
        # Use minimal conductor in cloud environments (no ChromaDB)
        is_cloud = os.getenv("RENDER") or os.getenv("RAILWAY") or os.getenv("HEROKU")
        
        try:
            if is_cloud:
                from conductor.minimal import MinimalConductor
                conductor = MinimalConductor()
                logger.info("Using minimal conductor (cloud mode - no memory)")
            else:
                conductor = ConductorAgent()
                logger.info("Using full conductor (local mode - with memory)")
        except Exception as e:
            logger.error(f"Failed to initialize conductor: {e}")
            # Ultimate fallback - minimal conductor
            try:
                from conductor.minimal import MinimalConductor
                conductor = MinimalConductor()
                logger.info("Fallback to minimal conductor due to error")
            except:
                raise ValueError(f"Could not initialize any conductor: {e}")
    return conductor

def get_voice_processor_instance():
    """Lazy initialization of voice processor."""
    global voice_processor
    if voice_processor is None:
        voice_processor = get_voice_processor()
    return voice_processor

# Create temp directory for audio files
TEMP_DIR = Path("temp_audio")
TEMP_DIR.mkdir(exist_ok=True)


# Request/Response Models
class ChatRequest(BaseModel):
    query: str
    platform_filter: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    sources: list
    audio_url: Optional[str] = None


class VoiceSettings(BaseModel):
    voice: str = "nova"


# In-memory voice settings (could be persisted later)
current_voice_settings = VoiceSettings()


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main web interface."""
    static_dir = Path(__file__).parent / "static"
    index_file = static_dir / "index.html"
    
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return """
        <html>
            <body>
                <h1>Conductor Voice Agent</h1>
                <p>Web interface will be available soon.</p>
                <p>API is running. Try POST /api/chat</p>
            </body>
        </html>
        """


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "conductor-voice-agent",
        "version": "1.0.0"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Text-based chat endpoint.
    
    Args:
        request: Chat request with query and optional platform filter
        
    Returns:
        Chat response with answer and sources
    """
    try:
        logger.info(f"Chat request: {request.query[:100]}...")
        
        result = get_conductor().chat(
            query=request.query,
            platform_filter=request.platform_filter
        )
        
        return ChatResponse(
            response=result['response'],
            sources=result['sources']
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/voice-chat")
async def voice_chat(audio: UploadFile = File(...)):
    """
    Voice-based chat endpoint.
    Accepts audio input, transcribes it, generates response, and returns audio.
    
    Args:
        audio: Audio file (webm, mp3, wav, etc.)
        
    Returns:
        JSON with transcription, response text, and URL to audio response
    """
    try:
        # Save uploaded audio temporarily
        audio_id = str(uuid.uuid4())
        input_path = TEMP_DIR / f"input_{audio_id}.webm"
        
        with open(input_path, "wb") as f:
            content = await audio.read()
            f.write(content)
        
        logger.info(f"Received audio file: {input_path}")
        
        # Transcribe audio to text
        vp = get_voice_processor_instance()
        transcription = await vp.transcribe_audio(input_path)
        logger.info(f"Transcription: {transcription}")
        
        # Get response from conductor
        result = get_conductor().chat(query=transcription)
        response_text = result['response']
        
        # Synthesize speech from response
        output_path = TEMP_DIR / f"output_{audio_id}.mp3"
        await vp.synthesize_speech(
            text=response_text,
            output_path=output_path,
            voice=current_voice_settings.voice
        )
        
        # Clean up input file
        input_path.unlink()
        
        return {
            "transcription": transcription,
            "response": response_text,
            "sources": result['sources'],
            "audio_url": f"/api/audio/{output_path.name}"
        }
        
    except Exception as e:
        logger.error(f"Error in voice chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/audio/{filename}")
async def get_audio(filename: str):
    """
    Serve generated audio file.
    
    Args:
        filename: Name of audio file
        
    Returns:
        Audio file
    """
    file_path = TEMP_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        file_path,
        media_type="audio/mpeg",
        filename=filename
    )


@app.post("/api/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    """
    Transcribe audio to text only.
    
    Args:
        audio: Audio file
        
    Returns:
        Transcribed text
    """
    try:
        # Save temporarily
        audio_id = str(uuid.uuid4())
        temp_path = TEMP_DIR / f"temp_{audio_id}.webm"
        
        with open(temp_path, "wb") as f:
            content = await audio.read()
            f.write(content)
        
        # Transcribe
        transcription = await get_voice_processor_instance().transcribe_audio(temp_path)
        
        # Clean up
        temp_path.unlink()
        
        return {"transcription": transcription}
        
    except Exception as e:
        logger.error(f"Error in transcribe endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/synthesize")
async def synthesize(text: str, voice: Optional[str] = None):
    """
    Synthesize speech from text.
    
    Args:
        text: Text to convert to speech
        voice: Optional voice to use
        
    Returns:
        URL to audio file
    """
    try:
        audio_id = str(uuid.uuid4())
        output_path = TEMP_DIR / f"synth_{audio_id}.mp3"
        
        await get_voice_processor_instance().synthesize_speech(
            text=text,
            output_path=output_path,
            voice=voice or current_voice_settings.voice
        )
        
        return {"audio_url": f"/api/audio/{output_path.name}"}
        
    except Exception as e:
        logger.error(f"Error in synthesize endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/voices")
async def get_voices():
    """Get available TTS voices."""
    return {"voices": get_voice_processor_instance().get_available_voices()}


@app.post("/api/settings/voice")
async def set_voice(settings: VoiceSettings):
    """Update voice settings."""
    current_voice_settings.voice = settings.voice
    return {"voice": current_voice_settings.voice}


@app.get("/api/settings/voice")
async def get_voice():
    """Get current voice settings."""
    return {"voice": current_voice_settings.voice}


# ==================== WATER RESTRUCTURING ENDPOINTS ====================

from water_restructuring.frequency_sweep import (
    WaterRestructuringAnalyzer,
    FrequencyType
)

class FrequencySweepRequest(BaseModel):
    """Request for frequency sweep analysis."""
    n_particles: int = 100
    spacing: float = 0.65
    spiral_strength: float = 0.15
    seed: int = 42
    sweep_type: str = "preset"  # "preset", "single", or "range"
    frequency: Optional[float] = None  # For single frequency
    start_hz: Optional[float] = 400.0  # For range sweep
    end_hz: Optional[float] = 900.0    # For range sweep
    steps: Optional[int] = 20          # For range sweep


class FrequencySweepResponse(BaseModel):
    """Response from frequency sweep analysis."""
    sweep_type: str
    frequencies: List[float]
    coherence_before: List[float]
    coherence_after: List[float]
    improvements: List[float]
    peak_frequency: float
    peak_improvement: float
    peak_coherence: float


@app.post("/api/water/analyze-frequency", response_model=dict)
async def analyze_single_frequency(request: FrequencySweepRequest):
    """
    Analyze water restructuring at a single frequency.
    
    Args:
        request: Frequency sweep parameters
        
    Returns:
        Analysis results with before/after coherence and visualizations
    """
    try:
        analyzer = WaterRestructuringAnalyzer(
            n_particles=request.n_particles,
            seed=request.seed
        )
        
        frequency = request.frequency or 528.0
        result = analyzer.analyze_frequency(
            frequency=frequency,
            spacing=request.spacing,
            spiral_strength=request.spiral_strength
        )
        
        return {
            "frequency": result.frequency,
            "coherence_before": float(result.coherence_before),
            "coherence_after": float(result.coherence_after),
            "improvement_percent": float(result.improvement_percent),
            "resonance_amplitude": float(result.resonance_amplitude),
            "particles_before": result.particle_positions_before.tolist(),
            "particles_after": result.particle_positions_after.tolist()
        }
        
    except Exception as e:
        logger.error(f"Error in water frequency analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/water/sweep-preset", response_model=FrequencySweepResponse)
async def sweep_preset_frequencies(request: FrequencySweepRequest):
    """
    Run frequency sweep across all preset healing frequencies.
    
    Args:
        request: Sweep parameters
        
    Returns:
        Sweep results with all frequencies tested
    """
    try:
        analyzer = WaterRestructuringAnalyzer(
            n_particles=request.n_particles,
            seed=request.seed
        )
        
        sweep_results = analyzer.sweep_preset_frequencies()
        
        return FrequencySweepResponse(
            sweep_type="preset",
            frequencies=sweep_results.frequencies,
            coherence_before=sweep_results.coherence_before,
            coherence_after=sweep_results.coherence_after,
            improvements=sweep_results.improvements,
            peak_frequency=sweep_results.peak_frequency,
            peak_improvement=sweep_results.peak_improvement,
            peak_coherence=sweep_results.coherence_after[
                sweep_results.frequencies.index(sweep_results.peak_frequency)
            ]
        )
        
    except Exception as e:
        logger.error(f"Error in water preset sweep: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/water/sweep-range", response_model=FrequencySweepResponse)
async def sweep_frequency_range(request: FrequencySweepRequest):
    """
    Run frequency sweep across a custom frequency range.
    
    Args:
        request: Sweep parameters with start_hz, end_hz, steps
        
    Returns:
        Sweep results with all frequencies tested
    """
    try:
        analyzer = WaterRestructuringAnalyzer(
            n_particles=request.n_particles,
            seed=request.seed
        )
        
        sweep_results = analyzer.sweep_frequency_range(
            start_hz=request.start_hz or 400.0,
            end_hz=request.end_hz or 900.0,
            steps=request.steps or 20
        )
        
        return FrequencySweepResponse(
            sweep_type="range",
            frequencies=sweep_results.frequencies,
            coherence_before=sweep_results.coherence_before,
            coherence_after=sweep_results.coherence_after,
            improvements=sweep_results.improvements,
            peak_frequency=sweep_results.peak_frequency,
            peak_improvement=sweep_results.peak_improvement,
            peak_coherence=sweep_results.coherence_after[
                sweep_results.frequencies.index(sweep_results.peak_frequency)
            ]
        )
        
    except Exception as e:
        logger.error(f"Error in water range sweep: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/water/frequencies")
async def get_preset_frequencies():
    """Get list of preset healing frequencies."""
    from water_restructuring.frequency_sweep import FrequencyType
    
    return {
        "preset_frequencies": [
            {
                "name": f.name.replace("HZ_", "").replace("_", " "),
                "frequency": f.value
            }
            for f in FrequencyType
        ]
    }


# Mount static files (will create later)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"Starting Conductor Voice Agent on port {port}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
