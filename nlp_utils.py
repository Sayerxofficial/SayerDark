def analyze_text(text):
    # Simple text analysis
    text = text.lower()
    if any(word in text for word in ['urgent', 'important', 'critical']):
        return {'label': 'IMPORTANT', 'score': 0.9}
    elif any(word in text for word in ['new', 'fresh', 'latest']):
        return {'label': 'NEW', 'score': 0.8}
    else:
        return {'label': 'NORMAL', 'score': 0.5}
