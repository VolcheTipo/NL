rules = [
    {
        "conditions": [("light", "high"), ("time", "day")],
        "output": "min"
    },
    {
        "conditions": [("light", "low"), ("time", "night")],
        "output": "max"
    },
    {
        "conditions": [("light", "medium"), ("time", "evening")],
        "output": "medium"
    },
    {
        "conditions": [("light", "low"), ("time", "morning")],
        "output": "medium"
    },
    {
        "conditions": [("light", "medium"), ("time", "night")],
        "output": "high"
    }
]

# Лингвистическая переменная «Освещенность» (lux)
light_vars = {
    'low': lambda x: decreasing_linear(x, 0, 300),  # низкая: от 0 до 300 люкс
    'medium': lambda x: triangular(x, 200, 500, 800),  # средняя: треугольная 200–500–800
    'high': lambda x: increasing_linear(x, 700, 1000)  # высокая: от 700 до 1000 люкс
}


# Лингвистическая переменная «Время суток» (часы)
def night_func(h):
    # ночное время: от 0–6 и от 18–24
    return max(decreasing_linear(h, 0, 6), increasing_linear(h, 18, 24))


time_vars = {
    'morning': lambda h: triangular(h, 5, 8, 11),  # утро: треугольник 5–8–11
    'day': lambda h: triangular(h, 10, 14, 18),  # день: 10–14–18
    'evening': lambda h: triangular(h, 17, 19, 21),  # вечер: 17–19–21
    'night': night_func  # ночь: 0–6 и 18–24
}

# Лингвистическая переменная «Яркость света» (0–100%)
output_vars = {
    'min': lambda x: decreasing_linear(x, 0, 30),  # минимальная яркость
    'medium': lambda x: triangular(x, 20, 50, 80),  # средняя
    'high': lambda x: triangular(x, 60, 75, 90),  # высокая
    'max': lambda x: increasing_linear(x, 70, 100)  # максимальная
}

def triangular(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x < c:
        return (c - x) / (c - b)
    else:
        return 0.0


def increasing_linear(x, a, b):
    if x <= a:
        return 0.0
    elif x >= b:
        return 1.0
    else:
        return (x - a) / (b - a)


def decreasing_linear(x, a, b):
    if x <= a:
        return 1.0
    elif x >= b:
        return 0.0
    else:
        return (b - x) / (b - a)


def defuzzify(output_memberships, output_variable, output_range=(0, 100), resolution=1000):
    min_val, max_val = output_range
    step = (max_val - min_val) / resolution

    numerator = 0.0 #числитель , зн. вых. перем.
    denominator = 0.0 #знаменатель, сум.степ. принадл.

    for i in range(resolution + 1):
        x = min_val + i * step
        mu = 0.0
        for term, degree in output_memberships.items():
            mu_term = output_variable[term](x)
            mu = max(mu, min(degree, mu_term))  # агрегирование max(min)

        numerator += x * mu
        denominator += mu

    if denominator == 0:
        return 0.0
    return numerator / denominator



def fuzzify(value, var_terms):
    """
    value     — численное значение (lux или час)
    var_terms — словарь вида {терм: функция_принадлежности}
    Возвращает словарь {терм: степень_принадлежности}
    """
    return {term: func(value) for term, func in var_terms.items()}

#словарь степ. для актив.
def apply_rules(lux, hour):
    # 1) фаззификация
    light_deg = fuzzify(lux, light_vars)
    time_deg = fuzzify(hour, time_vars)

    # 2) активация базы правил
    output_activations = {}
    for rule in rules:
        # собираем степени истинности каждого условия
        degrees = []
        for var_name, term in rule['conditions']:
            deg = light_deg[term] if var_name == 'light' else time_deg[term]
            degrees.append(deg)
        activation = min(degrees)  # конъюнкция через min

        if activation > 0:
            out_term = rule['output']
            # агрегируем через max, если выходной терм уже активирован
            output_activations[out_term] = max(output_activations.get(out_term, 0), activation)

    return output_activations

#числ. знач. ярк.
def calculate_brightness(lux, hour):
    """
    lux  — уровень естественного света (0…1000)
    hour — текущее время (0…24)
    return: четкое значение яркости лампы (0…100%)
    """
    # 1. Активация правил
    activations = apply_rules(lux, hour)

    # 2. Дефаззификация центроидом (мцт)
    return defuzzify(activations, output_vars, output_range=(0, 100), resolution=1000)


if __name__ == '__main__':
    # Тёмная ночь (20 lux) в 23:00 → ожидаем близко к 100%
    print(f"Brightness @20 lux, 23h: {calculate_brightness(20, 23):.1f}%")

    # Яркий день (900 lux) в 14:00 → яркость минимальна
    print(f"Brightness @900 lux, 14h: {calculate_brightness(900, 14):.1f}%")
