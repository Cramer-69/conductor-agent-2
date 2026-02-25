# 💧 Water Restructuring with Frequency Sweep Analysis

A sophisticated simulation of water molecule restructuring using Schauberger vortex dynamics and cymatics (frequency-driven resonance). Tunable frequency sweep reveals optimal coherence across the spectrum.

## 🎯 What It Does

**Before:** Random Brownian motion → Coherence **0.19** (chaotic)  
**After:** Structured φ-vortex hexagonal lattice → Coherence **0.44** (+132% improvement)

The system models:
- **Hexagonal close-pack lattice** — geometrically optimal particle arrangement
- **Golden ratio φ spiral vortex** — coherent rotational field imparting natural organization
- **Cymatics resonance** — frequency-driven amplification of coherence (peak at 528 Hz for "DNA repair")
- **Coherence metric** — inverse of mean pairwise distance (lower distance = higher coherence)

## 📁 Project Structure

```
water_restructuring/
├── __init__.py                 # Module exports
└── frequency_sweep.py          # Core analysis engine
    ├── WaterRestructuringAnalyzer   (main class)
    ├── CoherenceResult              (single frequency result)
    ├── FrequencySweepResults        (sweep batch results)
    ├── FrequencyType                (preset frequencies enum)
    └── quick_analysis() & quick_sweep() (convenience functions)

streamlit_app.py                # Interactive dashboard
                                # Modes: Single Freq | Preset Sweep | Custom Range

api/server.py                   # FastAPI integration
                                # Endpoints: /api/water/*
```

## ⚡ Quick Start

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Run Interactive Streamlit Dashboard**
```bash
streamlit run streamlit_app.py
```
Opens at `http://localhost:8501` with three modes:
- **Single Frequency** — Analyze one frequency (preset or custom)
- **Preset Sweep** — Test 432, 528, 639, 741, 852 Hz
- **Custom Range** — Sweep 400-900 Hz with tunable resolution

### 3. **Use Python API Directly**
```python
from water_restructuring import WaterRestructuringAnalyzer

analyzer = WaterRestructuringAnalyzer(n_particles=100, seed=42)

# Single frequency
result = analyzer.analyze_frequency(frequency=528.0)
print(f"Improvement: {result.improvement_percent:.1f}%")

# Preset sweep (432, 528, 639, 741, 852 Hz)
sweep = analyzer.sweep_preset_frequencies()
print(f"Peak: {sweep.peak_frequency:.0f} Hz @ +{sweep.peak_improvement:.1f}%")

# Custom range (400-900 Hz, 50 steps)
sweep = analyzer.sweep_frequency_range(start_hz=400, end_hz=900, steps=50)
```

### 4. **Access via REST API**
```bash
# Single frequency
curl -X POST http://localhost:8000/api/water/analyze-frequency \
  -H "Content-Type: application/json" \
  -d '{"frequency": 528.0, "n_particles": 100}'

# Preset sweep
curl -X POST http://localhost:8000/api/water/sweep-preset \
  -H "Content-Type: application/json" \
  -d '{"n_particles": 100}'

# Custom range
curl -X POST http://localhost:8000/api/water/sweep-range \
  -H "Content-Type: application/json" \
  -d '{"start_hz": 400, "end_hz": 900, "steps": 30}'

# Get preset frequencies
curl http://localhost:8000/api/water/frequencies
```

## 🔬 Physics Model

### Coherence Metric
```
Coherence(positions) = 1 / mean_pairwise_distance(all_particles)
```
- **Chaotic (low coherence):** Particles far apart, random distribution
- **Organized (high coherence):** Particles clustered close together
- **Typical range:** 0.1 - 0.5 (normalized by domain size)

### Hexagonal Lattice
- Close-packed geometry from rows of offset hexagonal positions
- Natural structure for 2D crystalline organization
- Spacing parameter controls tightness (0.3 - 1.5)

### Golden Spiral Vortex
- Perturbation applied as: `spiral(r, θ) = strength × r × sin(θ × φ × 2)`
- φ ≈ 1.618 (golden ratio) creates fractal self-similar curl
- Imparts natural rotational coherence field

### Resonance Amplification
```
resonance(f) = exp(-damping × (distance_to_f0)² / 100)
```
Natural frequencies (f₀) ≈ 432, 528, 639 Hz  
→ Frequencies near f₀ get **50% coherence boost**  
→ 528 Hz typically peaks (biological resonance)

### Cymatics Waveform
```
amplitude(t) = exp(-t / φ × 8) × cos(2π × f × t)
```
- Exponential decay (φ-scaled) for realistic energy dissipation
- Frequency-dependent oscillation drives particle reorganization
- Visualization shows how drive couples to structure

## 📊 Key Parameters

| Parameter | Range | Default | Effect |
|-----------|-------|---------|--------|
| **n_particles** | 50-500 | 100 | More particles = finer resolution |
| **spacing** | 0.3-1.5 | 0.65 | Hex lattice density (tight→loose) |
| **spiral_strength** | 0.05-0.5 | 0.15 | Vortex curl amplitude |
| **start_hz** | 100-2000 | 400 | Range sweep lower bound |
| **end_hz** | 100-2000 | 900 | Range sweep upper bound |
| **steps** | 5-100 | 20 | Frequency resolution in sweep |
| **seed** | int | 42 | Random reproducibility |

## 🎨 Visualization Output

Each analysis generates 3 plots:

1. **Before (Blue, Random)**
   - Typical coherence: 0.15 - 0.25
   - Scattered particle distribution
   
2. **After (Lime Green, Vortex Lattice)**
   - Enhanced coherence: 0.30 - 0.50
   - Structured hexagonal + spiral pattern
   - Purple circle shows vortex center

3. **Waveform (Purple)**
   - 528 Hz (or selected frequency) cymatic drive
   - Exponential decay envelope
   - Shows resonant oscillation duration

## 🧪 Experimental Modes

### Preset Frequencies (Healing/Tuning)
- **432 Hz** — Tuning frequency (root chakra alignment)
- **528 Hz** — Love/DNA repair (Solfeggio scale)
- **639 Hz** — Heart harmony & relationships
- **741 Hz** — Throat chakra & expression
- **852 Hz** — Third eye awakening & clarity

### Custom Range Sweep
Test any frequencies (single or broad range) to:
- Find resonance peaks in your domain
- Explore frequency-coherence relationship
- Discover optimal tuning for specific applications

## 📈 Expected Results

**Typical coherence improvements:**
- Random → Hex lattice alone: **+50-80%**
- Hex + vortex spiral: **+100-150%**
- Resonant frequency peak: **+150-200%** (528 Hz usually wins)

**Peak improvements:**
- 432 Hz: typically +80-120%
- **528 Hz: typically +130-180%** ⭐ (strongest)
- 639 Hz: typically +90-140%
- Custom sweeps can reveal higher peaks

## 🚀 Future Enhancements

1. **Dynamic Animation** — Real-time particle motion under field
2. **3D Ice Lattice** — Hexagonal close-pack Ih structure with H-bonds
3. **Frequency Optimization** — Auto-find peak coherence
4. **Temporal Evolution** — Show coherence growth over time
5. **FluidDynamics** — Navier-Stokes + vortex force field

## 📝 Usage Examples

### Example 1: Find Best Frequency
```python
from water_restructuring import WaterRestructuringAnalyzer

analyzer = WaterRestructuringAnalyzer(n_particles=150)
sweep = analyzer.sweep_preset_frequencies()

print(f"Best frequency: {sweep.peak_frequency:.0f} Hz")
print(f"Improvement: {sweep.peak_improvement:.1f}%")
print(f"Achieved coherence: {max(sweep.coherence_after):.4f}")
```

### Example 2: Optimize Lattice Parameters
```python
results = []
for spacing in [0.5, 0.65, 0.8]:
    for spiral in [0.1, 0.15, 0.2]:
        result = analyzer.analyze_frequency(
            528.0,
            spacing=spacing,
            spiral_strength=spiral
        )
        results.append((spacing, spiral, result.improvement_percent))

# Find best combo
best = max(results, key=lambda x: x[2])
print(f"Optimal: spacing={best[0]}, spiral={best[1]}, improvement={best[2]:.1f}%")
```

### Example 3: Full Sweep with Custom Range
```python
sweep = analyzer.sweep_frequency_range(
    start_hz=500,
    end_hz=700,
    steps=50
)

import matplotlib.pyplot as plt
plt.plot(sweep.frequencies, sweep.improvements)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Improvement (%)")
plt.title(f"Peak: {sweep.peak_frequency:.0f} Hz @ {sweep.peak_improvement:.1f}%")
plt.show()
```

## 🔐 API Responses

### Single Frequency Response
```json
{
  "frequency": 528.0,
  "coherence_before": 0.1847,
  "coherence_after": 0.4402,
  "improvement_percent": 138.3,
  "resonance_amplitude": 0.954,
  "particles_before": [[x, y], ...],
  "particles_after": [[x, y], ...]
}
```

### Sweep Response
```json
{
  "sweep_type": "preset",
  "frequencies": [432, 528, 639, 741, 852],
  "coherence_before": [0.19, 0.19, 0.19, 0.19, 0.19],
  "coherence_after": [0.39, 0.44, 0.41, 0.38, 0.36],
  "improvements": [105.2, 132.1, 115.8, 98.5, 89.3],
  "peak_frequency": 528.0,
  "peak_improvement": 132.1,
  "peak_coherence": 0.440
}
```

## 📚 References & Theory

**Schauberger Vortex Dynamics**
- Natural water organization via golden ratio spirals
- Implosion = coherence/levitation (vs explosion/dispersion)

**Cymatics & Frequency Resonance**
- Visible sound patterns in media (water, sand, etc.)
- Solfeggio frequencies linked to biological harmonic alignment

**Coherence Metrics**
- Phase alignment and organization measures
- Inverse pairwise distance as proxy for clustering

---

**Status:** ✅ MVP complete (132% baseline improvement)  
**Next:** Dynamic animation + 3D lattice + frequency sweep dashboard  
**Daily gain:** +1 physical realism touch per iteration

*Built with golden ratio φ, 528 Hz resonance, and love* 💧✨
