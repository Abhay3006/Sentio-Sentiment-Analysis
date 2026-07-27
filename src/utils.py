def format_time(seconds):

    seconds = max(0, int(seconds))

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        return f"{hours} hr {minutes} min {remaining_seconds} sec"

    elif minutes > 0:
        return f"{minutes} min {remaining_seconds} sec"

    elif seconds > 0:
        return f"{remaining_seconds} sec"

    else:
        return "Finishing..."


def format_percentage(score):
    return f"{score * 100:.2f}%"