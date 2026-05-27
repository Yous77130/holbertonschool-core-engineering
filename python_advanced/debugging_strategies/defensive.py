#!/usr/bin/env python3
"""
Lab: Defensive debugging and validation.
Goal: compute average score from user-provided text.
"""


def parse_scores_csv(scores_text):
    """Parse comma-separated scores into a list of ints."""
    if not scores_text or not scores_text.strip():
        raise ValueError("scores_text must not be empty")
    parts = scores_text.split(",")
    scores = []
    for part in parts:
        part = part.strip()
        if not part.isdigit():
            raise ValueError("invalid score token: {!r}".format(part))
        scores.append(int(part))
    return scores


def average_score(scores):
    """Return arithmetic mean of a non-empty score list."""
    if not scores:
        raise ValueError("scores list must not be empty")
    return sum(scores) / len(scores)


def score_band(avg):
    """Classify average score into a textual band."""
    if not isinstance(avg, (int, float)):
        raise TypeError("avg must be a number")
    if avg >= 90:
        return "A"
    if avg >= 80:
        return "B"
    if avg >= 70:
        return "C"
    if avg >= 60:
        return "D"
    return "F"


def evaluate_scores(scores_text):
    """Return (average, band) from comma-separated score text."""
    scores = parse_scores_csv(scores_text)
    avg = round(average_score(scores), 2)
    return avg, score_band(avg)


def main():
    """Main function."""
    valid_text = "90,85,78,100"
    try:
        avg, band = evaluate_scores(valid_text)
        print("Average:", avg)
        print("Band:", band)
    except ValueError as e:
        print("Error:", e)

    invalid_text = "90,85,invalid,100"
    try:
        avg, band = evaluate_scores(invalid_text)
        print("Average:", avg)
        print("Band:", band)
    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
