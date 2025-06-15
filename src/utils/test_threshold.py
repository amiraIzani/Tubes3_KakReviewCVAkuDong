# A script to test and find the optimal Levenshtein similarity threshold.

# --- Import only what you need ---
# You need to make sure Python can find this module.
# You might need to adjust the path or run with `python -m test_threshold`.
from algorithms.levenshtein import calculate_levenshtein_similarity

TEST_CASES = {
    "python": [("python", True), ("pyhton", True), ("pyton", True), ("phython", True), ("java", False)],
    "experience": [("experience", True), ("experence", True), ("exprience", True), ("expert", False)],
    "software": [("software", True), ("softare", True), ("softwares", True), ("hardware", False)],
}

# Thresholds to evaluate
THRESHOLDS_TO_TEST = [0.70, 0.75, 0.80, 0.85, 0.90, 0.95]

def run_test():
    best_f1 = 0
    best_threshold = None
    
    for threshold in THRESHOLDS_TO_TEST:
        # Initialize counters for true positives, false positives, false negatives, true negatives
        tp = fp = fn = tn = 0
        for correct, variations in TEST_CASES.items():
            for variation, should_match in variations:
                # Calculate similarity (assumed to be a float between 0 and 1, where 1 is identical)
                sim = calculate_levenshtein_similarity(correct, variation)
                is_match = sim >= threshold
                # Update counters based on match outcome and ground truth
                if is_match and should_match:
                    tp += 1
                elif is_match and not should_match:
                    fp += 1
                elif not is_match and should_match:
                    fn += 1
                else:
                    tn += 1
        
        # Calculate metrics with safeguards for zero denominators
        precision = tp / (tp + fp) if tp + fp > 0 else 1  # No positive predictions -> precision undefined, set to 1
        recall = tp / (tp + fn) if tp + fn > 0 else 0      # No true positives -> recall 0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
        
        # Display results for current threshold
        print(f"Threshold {threshold:.2f}: TP={tp}, FP={fp}, FN={fn}, TN={tn}, "
              f"Precision={precision:.2f}, Recall={recall:.2f}, F1={f1:.2f}")
        
        # Track the best threshold based on F1-score
        if f1 > best_f1:
            best_f1 = f1
            best_threshold = threshold
    
    # Report the optimal threshold
    print(f"\nBest Threshold: {best_threshold:.2f} with F1={best_f1:.2f}")

if __name__ == "__main__":
    run_test()