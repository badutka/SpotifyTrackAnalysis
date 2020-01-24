def miliseconds_to_minutes(miliseconds):

    second = round(miliseconds * 0.001, 2)
    full_minutes = int(second/60)
    rest_minutes = int(second % 60)

    minutes = str(full_minutes) + '.' + str(rest_minutes)
    return minutes

def miliseconds_to_seconds(miliseconds):
    return round(miliseconds * 0.001)