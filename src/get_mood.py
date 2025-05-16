def map_valence_arousal_to_mood(valence, arousal):
    neutral_radius = 0.05  # ακτίνα για neutral
    
    # Υπολογισμός απόστασης από το κέντρο (0,0)
    distance = (valence**2 + arousal**2)**0.5
    
    # Αν είμαστε κοντά στο κέντρο -> Neutral
    if distance <= neutral_radius:
        return "Neutral / Ambiguous"
    
    # Διαχωριστικά όρια (μηδενικά) για valence και arousal
    valence_pos = valence > 0
    valence_neg = valence < 0
    arousal_pos = arousal > 0
    arousal_neg = arousal < 0

    # 8 moods με βάση τεταρτημόρια (και midpoints)
    if valence_pos and arousal_pos:
        # Πάνω δεξιά τεταρτημόριο
        if valence > arousal:
            return "Happy"
        else:
            return "Excited"
    elif valence_pos and arousal_neg:
        # Κάτω δεξιά τεταρτημόριο
        if valence > -arousal:
            return "Relaxed"
        else:
            return "Calm"
    elif valence_neg and arousal_pos:
        # Πάνω αριστερά τεταρτημόριο
        if -valence > arousal:
            return "Depressed"
        else:
            return "Angry"
    elif valence_neg and arousal_neg:
        # Κάτω αριστερά τεταρτημόριο
        if -valence > -arousal:
            return "Sad"
        else:
            return "Tense"
    else:
        # Σε περίπτωση που valence ή arousal είναι ακριβώς 0
        return "Neutral / Ambiguous"
