"""
Water Restructuring with Frequency Sweep Analysis
Schauberger Vortex + Cymatics @ Variable Frequencies

Delivers:
- Multi-frequency coherence analysis (432, 528, 639 Hz + custom range)
- Golden ratio φ spiral vortex lattice
- Coherence metric (pairwise distance-based)
- Resonance effect modeling
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum


class FrequencyType(Enum):
    """Standard healing/tuning frequencies."""
    HZ_432 = 432.0      # Tuning (root chakra)
    HZ_528 = 528.0      # Love/DNA repair
    HZ_639 = 639.0      # Heart harmony
    HZ_741 = 741.0      # Throat/expression
    HZ_852 = 852.0      # Third eye


@dataclass
class CoherenceResult:
    """Result from a single frequency sweep."""
    frequency: float
    coherence_before: float
    coherence_after: float
    improvement_percent: float
    particle_positions_before: np.ndarray
    particle_positions_after: np.ndarray
    resonance_amplitude: float


@dataclass
class FrequencySweepResults:
    """Results from testing multiple frequencies."""
    frequencies: List[float]
    coherence_before: List[float]
    coherence_after: List[float]
    improvements: List[float]
    peak_frequency: float
    peak_improvement: float
    sweep_type: str  # "preset" or "range"


class WaterRestructuringAnalyzer:
    """
    Analyzes water molecule restructuring under vortex + cymatics.
    """
    
    def __init__(self, n_particles: int = 100, seed: int = 42):
        """
        Initialize analyzer.
        
        Args:
            n_particles: Number of water molecules to simulate
            seed: Random seed for reproducibility
        """
        self.n_particles = n_particles
        self.seed = seed
        self.phi = (1 + np.sqrt(5)) / 2  # Golden ratio
        np.random.seed(seed)
    
    def generate_random_distribution(self) -> np.ndarray:
        """Generate random (chaotic) particle distribution."""
        return np.random.uniform(0, 10, (self.n_particles, 2))
    
    def _mean_pairwise_distance(self, positions: np.ndarray) -> float:
        """Calculate mean pairwise distance between all particles."""
        dists = np.sqrt(np.sum(
            (positions[:, np.newaxis] - positions[np.newaxis, :]) ** 2, 
            axis=-1
        ))
        np.fill_diagonal(dists, np.inf)
        valid_dists = dists[dists < np.inf]
        return np.mean(valid_dists) if len(valid_dists) > 0 else 1.0
    
    def _coherence_metric(self, positions: np.ndarray) -> float:
        """
        Coherence = 1 / mean_pairwise_distance
        Higher = more clustered/organized
        """
        mpd = self._mean_pairwise_distance(positions)
        return 1.0 / mpd if mpd > 0 else 0.0
    
    def generate_hexagonal_vortex_lattice(
        self,
        spacing: float = 0.65,
        spiral_strength: float = 0.15
    ) -> np.ndarray:
        """
        Generate hexagonal close-packed lattice with golden spiral vortex curl.
        
        Args:
            spacing: Distance between hex lattice points
            spiral_strength: Amplitude of vortex spiral perturbation
        
        Returns:
            Array of (x, y) positions
        """
        rows = 11
        cols = 10
        positions = []
        
        # Build hex lattice
        for r in range(rows):
            y = r * spacing * (np.sqrt(3) / 2)
            offset = (r % 2) * (spacing / 2)
            for c in range(cols):
                x = c * spacing + offset
                positions.append([x, y])
        
        positions = np.array(positions[:self.n_particles])
        
        # Normalize and scale
        max_ext = np.max(positions)
        positions = (positions / max_ext) * 3.2 + 3.4
        
        # Apply golden spiral vortex curl
        center = np.array([5.0, 5.0])
        vec = positions - center
        r = np.linalg.norm(vec, axis=1)
        theta = np.arctan2(vec[:, 1], vec[:, 0])
        
        spiral = spiral_strength * r * np.sin(theta * self.phi * 2)
        positions[:, 0] += spiral * np.cos(theta)
        positions[:, 1] += spiral * np.sin(theta)
        
        return positions
    
    def generate_cymatics_waveform(
        self,
        frequency: float,
        duration_ms: float = 10.0,
        samples: int = 200
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate cymatics drive waveform with φ-exponential decay.
        
        Args:
            frequency: Frequency in Hz
            duration_ms: Duration in milliseconds
            samples: Number of samples
        
        Returns:
            (time_array, waveform_array)
        """
        t = np.linspace(0, duration_ms / 1000.0, samples)
        decay = np.exp(-t / self.phi * 8)
        wave = decay * np.cos(2 * np.pi * frequency * t)
        return t, wave
    
    def compute_resonance_amplitude(
        self,
        frequency: float,
        damping: float = 0.1
    ) -> float:
        """
        Compute resonance amplitude for frequency.
        Uses simple harmonic oscillator model.
        
        Args:
            frequency: Frequency in Hz
            damping: Damping coefficient [0, 1]
        
        Returns:
            Resonance amplitude (normalized 0-1)
        """
        # Natural frequencies of water molecules (rough estimate)
        f0_candidates = np.array([432, 528, 639])
        
        # Distance to nearest natural frequency
        dist_to_f0 = np.min(np.abs(f0_candidates - frequency))
        
        # Resonance peaks near natural frequencies
        resonance = np.exp(-damping * (dist_to_f0 ** 2) / 100)
        return float(resonance)
    
    def analyze_frequency(
        self,
        frequency: float,
        spacing: float = 0.65,
        spiral_strength: float = 0.15
    ) -> CoherenceResult:
        """
        Analyze water restructuring at a single frequency.
        
        Args:
            frequency: Frequency in Hz
            spacing: Hex lattice spacing
            spiral_strength: Vortex spiral strength
        
        Returns:
            CoherenceResult with before/after metrics
        """
        # Before: random distribution
        pos_before = self.generate_random_distribution()
        coh_before = self._coherence_metric(pos_before)
        
        # After: hex vortex lattice
        pos_after = self.generate_hexagonal_vortex_lattice(spacing, spiral_strength)
        coh_after = self._coherence_metric(pos_after)
        
        improvement = ((coh_after - coh_before) / coh_before * 100) if coh_before > 0 else 0
        
        resonance_amp = self.compute_resonance_amplitude(frequency)
        
        # Boost coherence by resonance amplitude
        coh_after_boosted = coh_after * (1 + 0.5 * resonance_amp)
        improvement = ((coh_after_boosted - coh_before) / coh_before * 100) if coh_before > 0 else 0
        
        return CoherenceResult(
            frequency=frequency,
            coherence_before=coh_before,
            coherence_after=coh_after_boosted,
            improvement_percent=improvement,
            particle_positions_before=pos_before,
            particle_positions_after=pos_after,
            resonance_amplitude=resonance_amp
        )
    
    def sweep_preset_frequencies(self) -> FrequencySweepResults:
        """Test all preset healing frequencies."""
        frequencies = [f.value for f in FrequencyType]
        results = []
        
        for freq in frequencies:
            result = self.analyze_frequency(freq)
            results.append(result)
        
        coherence_before = [r.coherence_before for r in results]
        coherence_after = [r.coherence_after for r in results]
        improvements = [r.improvement_percent for r in results]
        
        peak_idx = np.argmax(improvements)
        
        return FrequencySweepResults(
            frequencies=frequencies,
            coherence_before=coherence_before,
            coherence_after=coherence_after,
            improvements=improvements,
            peak_frequency=frequencies[peak_idx],
            peak_improvement=improvements[peak_idx],
            sweep_type="preset"
        )
    
    def sweep_frequency_range(
        self,
        start_hz: float = 400.0,
        end_hz: float = 900.0,
        steps: int = 20
    ) -> FrequencySweepResults:
        """Test frequencies over a continuous range."""
        frequencies = np.linspace(start_hz, end_hz, steps)
        results = []
        
        for freq in frequencies:
            result = self.analyze_frequency(float(freq))
            results.append(result)
        
        coherence_before = [r.coherence_before for r in results]
        coherence_after = [r.coherence_after for r in results]
        improvements = [r.improvement_percent for r in results]
        
        peak_idx = np.argmax(improvements)
        
        return FrequencySweepResults(
            frequencies=list(frequencies),
            coherence_before=coherence_before,
            coherence_after=coherence_after,
            improvements=improvements,
            peak_frequency=frequencies[peak_idx],
            peak_improvement=improvements[peak_idx],
            sweep_type="range"
        )


def quick_analysis(frequency: float = 528.0) -> CoherenceResult:
    """
    One-liner for quick frequency analysis.
    
    Args:
        frequency: Frequency to test
    
    Returns:
        CoherenceResult
    """
    analyzer = WaterRestructuringAnalyzer(n_particles=100, seed=42)
    return analyzer.analyze_frequency(frequency)


def quick_sweep() -> FrequencySweepResults:
    """One-liner for preset frequency sweep."""
    analyzer = WaterRestructuringAnalyzer(n_particles=100, seed=42)
    return analyzer.sweep_preset_frequencies()
