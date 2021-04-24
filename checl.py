import datetime


def zodiac_serch(date_birth):
    zodiac_dates = {
        '1': 'водолей',
        '2': 'рыбы',
        '3': 'овен',
        '4': 'телец',
        '5': 'близнецы',
        '6': 'рак',
        '7': 'лев',
        '8': 'дева',
        '9': 'весы',
        '10': 'скорпион',
        '11': 'стрелец',
        '12': 'козерог',
    }

    for i in range(1, 13):
        if i == date_birth.month:
            if date_birth.day < 22:
                if i != 1:
                    return zodiac_dates[str(i - 1)]
                else:
                    return zodiac_dates['12']
            else:
                return zodiac_dates[str(i)]


def eng_zodiac(rus_zodic):
    zodiacs_name = {
        'водолей': 'aquarius',
        'рыбы': 'pisces',
        'овен': 'aries',
        'телец': 'taurus',
        'близнецы': 'gemini',
        'рак': 'cancer',
        'лев': 'leo',
        'дева': 'virgo',
        'весы': 'libra',
        'скорпион': 'scorpio',
        'стрелец': 'sagittarius',
        'козерог': 'capricorn',
    }
    return zodiacs_name[rus_zodic]


def rus_zodiac(eng_zodiac):
    zodiacs_name = {
        'aquarius': 'водолей',
        'pisces': 'рыбы',
        'aries': 'овен',
        'taurus': 'телец',
        'gemini': 'близнецы',
        'cancer': 'рак',
        'leo': 'лев',
        'virgo': 'дева',
        'libra': 'весы',
        'scorpio': 'скорпион',
        'sagittarius': 'стрелец',
        'capricorn': 'козерог',
    }
    return zodiacs_name[eng_zodiac]
