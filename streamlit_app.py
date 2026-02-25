"""
Streamlit Dashboard: Water Restructuring Frequency Sweep
Interactive exploration of 528 Hz + other frequencies
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import sys
from pathlib import Path

# Add conductor_agent to path
_pkg_dir = str(Path(__file__).resolve().parent.parent)
if _pkg_dir not in sys.path:
    sys.path.insert(0, _pkg_dir)

from water_restructuring.frequency_sweep import (
    WaterRestructuringAnalyzer,
    FrequencyType
)

st.set_page_config(
    page_title="💧 Water Restructuring - Frequency Sweep",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💧 H₂O Restructuring: Schauberger Vortex + Cymatics")
st.markdown("""
Explore how different frequencies reshape water molecule coherence.
**Golden ratio φ spiral vortex** + **528 Hz cymatic drive** (+ others!)
""")

# Sidebar controls
st.sidebar.header("⚙️ Configuration")

analysis_type = st.sidebar.radio(
    "Select Analysis Mode",
    ["Single Frequency", "Preset Sweep", "Custom Range Sweep"]
)

n_particles = st.sidebar.slider(
    "Number of Water Molecules",
    min_value=50,
    max_value=500,
    value=100,
    step=10
)

spacing = st.sidebar.slider(
    "Hexagonal Lattice Spacing",
    min_value=0.3,
    max_value=1.5,
    value=0.65,
    step=0.05
)

spiral_strength = st.sidebar.slider(
    "Vortex Spiral Strength",
    min_value=0.05,
    max_value=0.5,
    value=0.15,
    step=0.02
)

seed = st.sidebar.number_input(
    "Random Seed (reproducibility)",
    value=42,
    step=1
)

# Initialize analyzer
analyzer = WaterRestructuringAnalyzer(n_particles=int(n_particles), seed=int(seed))

# ==================== SINGLE FREQUENCY ====================
if analysis_type == "Single Frequency":
    st.header("🎯 Single Frequency Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        freq_choice = st.selectbox(
            "Select Frequency",
            [(f.name.replace("HZ_", "").replace("_", " "), f.value) for f in FrequencyType],
            format_func=lambda x: f"{x[0]} ({x[1]:.0f} Hz)"
        )
        frequency = freq_choice[1]
    
    with col2:
        custom_freq = st.checkbox("Use Custom Frequency?")
        if custom_freq:
            frequency = st.number_input("Enter frequency (Hz)", value=528.0, step=1.0)
    
    if st.button("🚀 Analyze Frequency", key="single_analyze"):
        with st.spinner("Analyzing..."):
            result = analyzer.analyze_frequency(
                frequency,
                spacing=spacing,
                spiral_strength=spiral_strength
            )
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Frequency", f"{result.frequency:.1f} Hz", delta="🎵")
        with col2:
            st.metric("Before Coherence", f"{result.coherence_before:.3f}", delta="🌀")
        with col3:
            st.metric("After Coherence", f"{result.coherence_after:.3f}", 
                     delta=f"+{result.coherence_after - result.coherence_before:.3f}")
        with col4:
            st.metric("Improvement", f"+{result.improvement_percent:.1f}%", 
                     delta="📈")
        
        st.metric("Resonance Amplitude", f"{result.resonance_amplitude:.3f}")
        
        # Visualization
        fig, axs = plt.subplots(1, 3, figsize=(18, 6))
        
        # Before
        axs[0].scatter(result.particle_positions_before[:, 0], 
                      result.particle_positions_before[:, 1],
                      c='blue', s=40, alpha=0.7, edgecolors='navy', linewidth=0.5)
        axs[0].set_title(f'Before: Random Distribution\nCoherence {result.coherence_before:.3f}',
                        fontsize=12, fontweight='bold')
        axs[0].set_xlim(0, 10)
        axs[0].set_ylim(0, 10)
        axs[0].set_aspect('equal')
        axs[0].grid(True, alpha=0.2)
        axs[0].set_xlabel('X')
        axs[0].set_ylabel('Y')
        
        # After
        axs[1].scatter(result.particle_positions_after[:, 0], 
                      result.particle_positions_after[:, 1],
                      c='lime', s=40, alpha=0.8, edgecolors='darkgreen', linewidth=0.5)
        center = np.array([5.0, 5.0])
        circle = Circle(center, 1.0, fill=False, edgecolor='purple', linewidth=2, linestyle='--', alpha=0.5)
        axs[1].add_patch(circle)
        axs[1].set_title(f'After: φ-Vortex Hex Lattice @ {frequency:.0f} Hz\nCoherence {result.coherence_after:.3f} (+{result.improvement_percent:.1f}%)',
                        fontsize=12, fontweight='bold')
        axs[1].set_xlim(0, 10)
        axs[1].set_ylim(0, 10)
        axs[1].set_aspect('equal')
        axs[1].grid(True, alpha=0.2)
        axs[1].set_xlabel('X')
        axs[1].set_ylabel('Y')
        
        # Waveform
        t, wave = analyzer.generate_cymatics_waveform(frequency, duration_ms=10.0, samples=200)
        axs[2].plot(t * 1000, wave, 'purple', linewidth=2.5, label='Cymatic Drive')
        axs[2].fill_between(t * 1000, wave, alpha=0.2, color='purple')
        axs[2].set_title(f'{frequency:.0f} Hz Cymatic Waveform\n(φ-Exponential Decay × Cos)',
                        fontsize=12, fontweight='bold')
        axs[2].set_xlabel('Time (ms)')
        axs[2].set_ylabel('Amplitude')
        axs[2].grid(True, alpha=0.3)
        axs[2].legend(loc='upper right')
        
        plt.suptitle('H₂O Restructuring: Schauberger Vortex + Cymatics',
                    fontsize=16, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        st.pyplot(fig)
        st.success(f"✅ Analysis complete! {result.improvement_percent:.1f}% coherence improvement.")

# ==================== PRESET SWEEP ====================
elif analysis_type == "Preset Sweep":
    st.header("🔍 Preset Frequency Sweep")
    st.markdown(f"""
    Testing all standard healing frequencies:
    - **432 Hz** (Tuning/Root)
    - **528 Hz** (Love/DNA)
    - **639 Hz** (Heart Harmony)
    - **741 Hz** (Throat/Expression)
    - **852 Hz** (Third Eye)
    """)
    
    if st.button("🚀 Run Preset Sweep", key="preset_sweep"):
        with st.spinner("Sweeping frequencies..."):
            sweep_results = analyzer.sweep_preset_frequencies()
        
        # Peak results
        st.subheader("📊 Peak Frequency")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Peak Frequency", f"{sweep_results.peak_frequency:.0f} Hz", delta="🎯")
        with col2:
            st.metric("Max Improvement", f"+{sweep_results.peak_improvement:.1f}%", delta="🚀")
        with col3:
            peak_coherence = sweep_results.coherence_after[
                sweep_results.frequencies.index(sweep_results.peak_frequency)
            ]
            st.metric("Peak Coherence", f"{peak_coherence:.3f}", delta="💧")
        
        # Table
        st.subheader("📈 Detailed Results")
        results_data = {
            "Frequency (Hz)": [f"{f:.0f}" for f in sweep_results.frequencies],
            "Before Coherence": [f"{c:.4f}" for c in sweep_results.coherence_before],
            "After Coherence": [f"{c:.4f}" for c in sweep_results.coherence_after],
            "Improvement (%)": [f"{i:.2f}%" for i in sweep_results.improvements]
        }
        st.dataframe(results_data, use_container_width=True)
        
        # Visualization
        fig, axs = plt.subplots(1, 2, figsize=(14, 5))
        
        # Coherence comparison
        x_pos = np.arange(len(sweep_results.frequencies))
        width = 0.35
        axs[0].bar(x_pos - width/2, sweep_results.coherence_before, width, 
                  label='Before (Random)', color='steelblue', alpha=0.8)
        axs[0].bar(x_pos + width/2, sweep_results.coherence_after, width,
                  label=f'After (Vortex)', color='lime', alpha=0.8)
        axs[0].set_xlabel('Frequency (Hz)', fontweight='bold')
        axs[0].set_ylabel('Coherence', fontweight='bold')
        axs[0].set_title('Coherence: Before vs After', fontsize=12, fontweight='bold')
        axs[0].set_xticks(x_pos)
        axs[0].set_xticklabels([f"{f:.0f}" for f in sweep_results.frequencies], rotation=45)
        axs[0].legend()
        axs[0].grid(True, alpha=0.2, axis='y')
        
        # Improvement %
        colors = ['gold' if f == sweep_results.peak_frequency else 'coral' 
                 for f in sweep_results.frequencies]
        axs[1].bar(x_pos, sweep_results.improvements, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        axs[1].set_xlabel('Frequency (Hz)', fontweight='bold')
        axs[1].set_ylabel('Improvement (%)', fontweight='bold')
        axs[1].set_title('Coherence Improvement by Frequency', fontsize=12, fontweight='bold')
        axs[1].set_xticks(x_pos)
        axs[1].set_xticklabels([f"{f:.0f}" for f in sweep_results.frequencies], rotation=45)
        axs[1].grid(True, alpha=0.2, axis='y')
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.success(f"✅ Sweep complete! Peak: {sweep_results.peak_frequency:.0f} Hz @ +{sweep_results.peak_improvement:.1f}%")

# ==================== CUSTOM RANGE SWEEP ====================
elif analysis_type == "Custom Range Sweep":
    st.header("📊 Custom Frequency Range Sweep")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        start_freq = st.number_input("Start Frequency (Hz)", value=400.0, step=10.0)
    with col2:
        end_freq = st.number_input("End Frequency (Hz)", value=900.0, step=10.0)
    with col3:
        sweep_steps = st.number_input("Number of Steps", value=20, step=1)
    
    if st.button("🚀 Run Custom Sweep", key="custom_sweep"):
        with st.spinner(f"Sweeping {start_freq:.0f} - {end_freq:.0f} Hz..."):
            sweep_results = analyzer.sweep_frequency_range(
                start_hz=start_freq,
                end_hz=end_freq,
                steps=int(sweep_steps)
            )
        
        # Peak results
        st.subheader("📊 Peak Frequency")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Peak Frequency", f"{sweep_results.peak_frequency:.0f} Hz", delta="🎯")
        with col2:
            st.metric("Max Improvement", f"+{sweep_results.peak_improvement:.1f}%", delta="🚀")
        with col3:
            peak_idx = sweep_results.frequencies.index(sweep_results.peak_frequency)
            peak_coherence = sweep_results.coherence_after[peak_idx]
            st.metric("Peak Coherence", f"{peak_coherence:.3f}", delta="💧")
        
        # Visualization
        fig, axs = plt.subplots(1, 2, figsize=(14, 5))
        
        # Line plot: Coherence
        axs[0].plot(sweep_results.frequencies, sweep_results.coherence_before,
                   marker='o', label='Before (Random)', color='steelblue', linewidth=2, markersize=4)
        axs[0].plot(sweep_results.frequencies, sweep_results.coherence_after,
                   marker='s', label='After (Vortex)', color='lime', linewidth=2, markersize=4)
        peak_idx = sweep_results.frequencies.index(sweep_results.peak_frequency)
        axs[0].plot(sweep_results.peak_frequency, sweep_results.coherence_after[peak_idx],
                   marker='*', markersize=20, color='gold', label='Peak', zorder=5)
        axs[0].set_xlabel('Frequency (Hz)', fontweight='bold')
        axs[0].set_ylabel('Coherence', fontweight='bold')
        axs[0].set_title('Coherence Across Frequency Range', fontsize=12, fontweight='bold')
        axs[0].legend()
        axs[0].grid(True, alpha=0.3)
        
        # Improvement curve
        axs[1].fill_between(sweep_results.frequencies, sweep_results.improvements,
                           alpha=0.3, color='orange')
        axs[1].plot(sweep_results.frequencies, sweep_results.improvements,
                   marker='o', color='darkorange', linewidth=2.5, markersize=5)
        axs[1].plot(sweep_results.peak_frequency, sweep_results.peak_improvement,
                   marker='*', markersize=20, color='gold', label='Peak', zorder=5)
        axs[1].set_xlabel('Frequency (Hz)', fontweight='bold')
        axs[1].set_ylabel('Improvement (%)', fontweight='bold')
        axs[1].set_title('Coherence Improvement Curve', fontsize=12, fontweight='bold')
        axs[1].legend()
        axs[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        st.success(f"✅ Sweep complete! Optimal frequency: {sweep_results.peak_frequency:.0f} Hz @ +{sweep_results.peak_improvement:.1f}%")

# Footer
st.markdown("""
---
**💡 How it works:**
1. Random particles = incoherent, chaotic (low coherence)
2. Hexagonal vortex lattice = structured arrangement
3. Golden ratio φ spiral imparts resonant curl
4. Cymatic frequency amplifies coherence via resonance matching
5. Coherence = inverse of mean pairwise distance (closer = more organized)

**🔬 Tuning Parameters:**
- **Spacing:** Hex lattice density (tighter = stronger structure)
- **Spiral Strength:** Vortex perturbation amplitude (more = deeper curl)
- **Frequency:** Drive oscillation (resonance peaks near 432, 528, 639 Hz)

**🎯 Next Steps:**
- Find your optimal frequency (usually 528 Hz for coherence)
- Tweak spacing/spiral for your application
- Scale to 3D ice lattice with H-bonds (Ih structure)
- Real fluid dynamics simulation (Navier-Stokes + vortex field)
""")
