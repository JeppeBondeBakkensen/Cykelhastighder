def time_of_day_label(hour: int) -> str:
    if 6 <= hour < 7:
        return "Tidlig morgen"
    elif 7 <= hour < 8:
        return "Morgen"
    elif 8 <= hour < 10:
        return "Rush hour"
    elif 10 <= hour < 12:
        return "Formiddag"
    elif 12 <= hour < 14:
        return "Middag"
    elif 14 <= hour < 16:
        return "Eftermiddag"
    else:
        return "Aften"

# consistent colours for legend
COLORS = {
    "Tidlig morgen": "darkorange",
    "Morgen": "tab:blue",
    "Rush hour": "tab:green",
    "Formiddag": "tomato",
    "Middag": "cornflowerblue",
    "Eftermiddag": "blueviolet",
    "Aften": "gold"
}

