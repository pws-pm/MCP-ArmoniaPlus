import numpy as np
import json
import argparse
from scipy import signal

# Common sample rates for audio processing
SAMPLE_RATES = {
    "standard": 48000,
    "high": 96000,
    "ultra": 192000
}

def generate_highpass_filter(taps, cutoff_freq, fs=48000, window='hamming'):
    """Generate a linear phase FIR high-pass filter"""
    # Convert Hz to normalized frequency
    nyq = 0.5 * fs
    normalized_cutoff = cutoff_freq / nyq
    
    # Ensure odd number of taps for high-pass filter
    if taps % 2 == 0:
        taps += 1
        
    b = signal.firwin(taps, normalized_cutoff, pass_zero=False, window=window)
    return b

def generate_lowpass_filter(taps, cutoff_freq, fs=48000, window='hamming'):
    """Generate a linear phase FIR low-pass filter"""
    # Convert Hz to normalized frequency
    nyq = 0.5 * fs
    normalized_cutoff = cutoff_freq / nyq
    
    b = signal.firwin(taps, normalized_cutoff, window=window)
    return b

def generate_bandpass_filter(taps, low_freq, high_freq, fs=48000, window='hamming'):
    """Generate a linear phase FIR band-pass filter"""
    # Convert Hz to normalized frequency
    nyq = 0.5 * fs
    normalized_low = low_freq / nyq
    normalized_high = high_freq / nyq
    
    # Ensure odd number of taps
    if taps % 2 == 0:
        taps += 1
        
    b = signal.firwin(taps, [normalized_low, normalized_high], pass_zero=False, window=window)
    return b

def generate_bandstop_filter(taps, low_freq, high_freq, fs=48000, window='hamming'):
    """Generate a linear phase FIR band-stop filter"""
    # Convert Hz to normalized frequency
    nyq = 0.5 * fs
    normalized_low = low_freq / nyq
    normalized_high = high_freq / nyq
    
    # Ensure odd number of taps
    if taps % 2 == 0:
        taps += 1
        
    b = signal.firwin(taps, [normalized_low, normalized_high], pass_zero=True, window=window)
    return b

def generate_peaking_eq(taps, center_freq, q, gain_db, fs=48000):
    """Generate a FIR peaking EQ filter by approximating IIR to FIR"""
    # Design 2nd-order IIR peaking filter (biquad)
    b_iir, a_iir = signal.iirpeak(center_freq / (0.5 * fs), q, gain_db)
    
    # Convert IIR to FIR using impulse response method
    # Ensure odd number of taps
    if taps % 2 == 0:
        taps += 1
    
    impulse = np.zeros(taps)
    impulse[0] = 1.0
    h_iir = signal.lfilter(b_iir, a_iir, impulse)
    
    # Apply window to improve frequency response
    h_windowed = h_iir * signal.windows.hamming(taps)
    
    # Normalize
    h_windowed = h_windowed / np.sum(np.abs(h_windowed))
    
    return h_windowed

def generate_shelving_filter(taps, cutoff_freq, gain_db, high_shelf=True, fs=48000):
    """Generate a FIR shelving filter using custom design technique"""
    # Compute normalized frequency
    nyq = 0.5 * fs
    normalized_cutoff = cutoff_freq / nyq
    
    # Create a halfband filter first (0dB to gain_db transition)
    if high_shelf:
        # For high shelf, start with lowpass filter
        halfband = generate_lowpass_filter(taps, cutoff_freq, fs)
        # Invert to get highpass
        highpass = -halfband
        highpass[taps//2] += 1.0  # Add impulse to make it allpass + highpass
        
        # Scale the filter to achieve the desired gain
        gain_linear = 10**(gain_db / 20.0)
        shelf_filter = highpass * (gain_linear - 1.0)
        shelf_filter[taps//2] += 1.0  # Add impulse to make it a shelf
    else:
        # For low shelf, use a lowpass filter directly
        lowpass = generate_lowpass_filter(taps, cutoff_freq, fs)
        
        # Scale the filter to achieve the desired gain
        gain_linear = 10**(gain_db / 20.0)
        shelf_filter = lowpass * (gain_linear - 1.0)
        shelf_filter[taps//2] += 1.0  # Add impulse to make it a shelf
    
    # Apply window to smooth response
    shelf_filter = shelf_filter * signal.windows.hamming(taps)
    
    return shelf_filter

def combine_filters(filters, weights=None):
    """Combine multiple filters by weighted summation
    
    Args:
        filters: List of filter coefficient arrays
        weights: List of weights for each filter (default: equal weights)
    
    Returns:
        Combined filter coefficients
    """
    if not filters:
        return None
    
    # Get the shortest filter length
    min_length = min(len(f) for f in filters)
    
    # Truncate all filters to the shortest length
    filters_truncated = [f[:min_length] for f in filters]
    
    # If no weights provided, use equal weights
    if weights is None:
        weights = [1.0] * len(filters)
    
    # Normalize weights
    weights = np.array(weights) / sum(weights)
    
    # Combine filters
    combined = np.zeros(min_length)
    for i, f in enumerate(filters_truncated):
        combined += weights[i] * f
    
    return combined

def parse_filter_spec(spec, taps=127, fs=48000):
    """Parse a filter specification and generate the corresponding filter
    
    Args:
        spec: Filter specification string (e.g., "hp:1000", "ls:500,-3")
        taps: Number of filter taps
        fs: Sample rate in Hz
    
    Returns:
        Filter coefficients
    """
    parts = spec.split(':')
    if len(parts) != 2:
        raise ValueError(f"Invalid filter specification: {spec}")
    
    filter_type = parts[0].lower()
    params = parts[1].split(',')
    
    if filter_type == "hp" or filter_type == "highpass":
        cutoff = float(params[0])
        return generate_highpass_filter(taps, cutoff, fs)
    
    elif filter_type == "lp" or filter_type == "lowpass":
        cutoff = float(params[0])
        return generate_lowpass_filter(taps, cutoff, fs)
    
    elif filter_type == "bp" or filter_type == "bandpass":
        if len(params) != 2:
            raise ValueError(f"Bandpass filter requires two frequencies: {spec}")
        low = float(params[0])
        high = float(params[1])
        return generate_bandpass_filter(taps, low, high, fs)
    
    elif filter_type == "bs" or filter_type == "bandstop" or filter_type == "notch":
        if len(params) != 2:
            raise ValueError(f"Bandstop filter requires two frequencies: {spec}")
        low = float(params[0])
        high = float(params[1])
        return generate_bandstop_filter(taps, low, high, fs)
    
    elif filter_type == "peak" or filter_type == "peaking":
        if len(params) != 3:
            raise ValueError(f"Peaking filter requires frequency, Q, and gain: {spec}")
        freq = float(params[0])
        q = float(params[1])
        gain = float(params[2])
        return generate_peaking_eq(taps, freq, q, gain, fs)
    
    elif filter_type == "hs" or filter_type == "highshelf":
        if len(params) != 2:
            raise ValueError(f"High shelf filter requires frequency and gain: {spec}")
        freq = float(params[0])
        gain = float(params[1])
        return generate_shelving_filter(taps, freq, gain, high_shelf=True, fs=fs)
    
    elif filter_type == "ls" or filter_type == "lowshelf":
        if len(params) != 2:
            raise ValueError(f"Low shelf filter requires frequency and gain: {spec}")
        freq = float(params[0])
        gain = float(params[1])
        return generate_shelving_filter(taps, freq, gain, high_shelf=False, fs=fs)
    
    else:
        raise ValueError(f"Unknown filter type: {filter_type}")

def visualize_filter(filter_coeffs, fs=48000, title="Filter Response"):
    """Visualize the filter frequency response"""
    try:
        import matplotlib.pyplot as plt
        
        # Calculate frequency response
        w, h = signal.freqz(filter_coeffs)
        
        # Convert to frequency and magnitude in dB
        freqs = w * fs / (2 * np.pi)
        mag_db = 20 * np.log10(np.abs(h))
        
        # Calculate phase response
        phase = np.unwrap(np.angle(h))
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Plot magnitude response
        ax1.semilogx(freqs, mag_db)
        ax1.set_title(f'{title} - Magnitude Response')
        ax1.set_xlabel('Frequency (Hz)')
        ax1.set_ylabel('Magnitude (dB)')
        ax1.set_xlim(20, fs/2)
        ax1.grid(True)
        
        # Plot phase response
        ax2.semilogx(freqs, phase)
        ax2.set_title('Phase Response')
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Phase (rad)')
        ax2.set_xlim(20, fs/2)
        ax2.grid(True)
        
        plt.tight_layout()
        plt.show()
    except ImportError:
        print("Matplotlib not installed. Cannot visualize filter.")
        print("Install with: pip install matplotlib")

def check_device_compatibility(filter_list):
    """Check if filter size is compatible with device and truncate if needed"""
    DEVICE_MAX_TAPS = 2048  # Maximum number of taps supported by ArmoníaPlus
    
    if len(filter_list) > DEVICE_MAX_TAPS:
        print(f"Warning: Filter size ({len(filter_list)} taps) exceeds ArmoníaPlus maximum ({DEVICE_MAX_TAPS}).")
        print(f"Filter will be truncated to {DEVICE_MAX_TAPS} taps for device application.")
        # Center tap is most important for FIR filters
        center = len(filter_list) // 2
        start = center - (DEVICE_MAX_TAPS // 2)
        end = start + DEVICE_MAX_TAPS
        return filter_list[start:end]
    return filter_list

def main():
    parser = argparse.ArgumentParser(description="Generate FIR filters based on specifications")
    parser.add_argument("--taps", type=int, default=1023, help="Number of filter taps (odd number recommended)")
    parser.add_argument("--fs", type=int, default=48000, help="Sample rate in Hz")
    parser.add_argument("--filters", type=str, nargs='+', required=True, 
                        help="Filter specifications (e.g., 'hp:1000', 'ls:500,-3')")
    parser.add_argument("--weights", type=float, nargs='+', 
                        help="Weights for combining filters (default: equal weights)")
    parser.add_argument("--visualize", action="store_true", help="Visualize the filter response")
    parser.add_argument("--device-id", type=str, help="Armonia device ID to apply filter to")
    parser.add_argument("--channel", type=int, help="Armonia device channel to apply filter to")
    parser.add_argument("--output", type=str, help="Output filter coefficients to a file")
    parser.add_argument("--truncate", action="store_true", help="Truncate filter to device-compatible size if needed")
    
    args = parser.parse_args()
    
    # Ensure odd number of taps for consistent phase response
    if args.taps % 2 == 0:
        args.taps += 1
        print(f"Adjusted taps to odd number: {args.taps}")
    
    # Parse filter specifications and generate filters
    filters = []
    for spec in args.filters:
        try:
            f = parse_filter_spec(spec, args.taps, args.fs)
            filters.append(f)
            print(f"Generated filter: {spec}")
        except ValueError as e:
            print(f"Error: {e}")
    
    if not filters:
        print("No valid filters specified")
        return
    
    # Combine filters if there are multiple
    if len(filters) > 1:
        combined_filter = combine_filters(filters, args.weights)
        print(f"Combined {len(filters)} filters")
    else:
        combined_filter = filters[0]
    
    # Convert to list for JSON serialization
    filter_list = combined_filter.tolist()
    
    # Print summary
    print(f"\nGenerated {len(filter_list)} filter coefficients")
    
    # Visualize filter only if explicitly requested
    if args.visualize:
        title = " + ".join(args.filters)
        visualize_filter(combined_filter, args.fs, title)
    
    # For device application, check compatibility and possibly truncate
    device_filter_list = filter_list
    if args.device_id is not None and args.channel is not None and args.truncate:
        device_filter_list = check_device_compatibility(filter_list)
    
    # Output coefficients in a format ready to copy-paste
    print("\nFilter coefficients for function call:")
    print(str(device_filter_list).replace(' ', ''))
    
    # Save to file if requested
    if args.output:
        try:
            with open(args.output, 'w') as f:
                json.dump(filter_list, f)
            print(f"Saved filter coefficients to {args.output}")
        except Exception as e:
            print(f"Failed to save to file: {e}")
    
    # Apply filter to device if specified
    if args.device_id is not None and args.channel is not None:
        try:
            # Try to import the necessary modules for Armonia
            import requests
            from dotenv import load_dotenv
            import os
            
            load_dotenv()
            
            # Get the API base URL from environment variables
            base_url = os.getenv("MCP_ARMONIA_API_URL", "http://localhost:8000/api")
            
            # Make the API request to apply the filter
            url = f"{base_url}/armonia/set_output_eq_fir"
            payload = {
                "device_id": args.device_id,
                "channel": args.channel,
                "values": device_filter_list
            }
            
            # Check if filter is too large for ArmoníaPlus API
            if len(device_filter_list) > 2048:
                print("Error: Filter too large for ArmoníaPlus API (maximum 2048 taps).")
                print("Use --truncate to automatically resize the filter for device compatibility.")
                return
            
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f"Successfully applied filter to device {args.device_id}, channel {args.channel}")
            else:
                print(f"Failed to apply filter: {response.text}")
        except ImportError:
            print("Required packages for Armonia API not installed. Cannot apply filter to device.")
            print("Install with: pip install requests python-dotenv")

if __name__ == "__main__":
    main() 