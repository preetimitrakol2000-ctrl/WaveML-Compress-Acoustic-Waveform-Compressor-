class WaveAnomalyDetector:
    def __init__(self, baseline_variance=1.5):
        self.baseline = baseline_variance
        self.threshold = 0.65

    def analyze_stream(self, data_stream, window_size=10):
        """
        Sliding Window Algorithm to discover sudden localized variance anomalies
        """
        anomalies_detected = 0
        
        for i in range(0, len(data_stream) - window_size, 2):
            window = data_stream[i : i + window_size]
            mean = sum(window) / window_size
            variance = sum((x - mean) ** 2 for x in window) / window_size
            
            # Anomaly condition: If local variance deviates significantly from the baseline wave
            if abs(variance - self.baseline) > self.threshold:
                anomalies_detected += 1
                
        return anomalies_detected
