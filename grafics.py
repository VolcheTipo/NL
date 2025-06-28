import numpy as np
import matplotlib.pyplot as plt

# --- Функции принадлежности ---
def triangular(x, a, b, c):
    return np.maximum(np.minimum((x - a) / (b - a), (c - x) / (c - b)), 0)

def increasing_linear(x, a, b):
    return np.clip((x - a) / (b - a), 0, 1)

def decreasing_linear(x, a, b):
    return np.clip((b - x) / (b - a), 0, 1)

# --- Освещенность (0–1000 люкс) ---
x_lux = np.linspace(0, 1000, 1000)
lux_low = decreasing_linear(x_lux, 0, 300)
lux_med = triangular(x_lux, 200, 500, 800)
lux_high = increasing_linear(x_lux, 700, 1000)

plt.figure(figsize=(8, 4))
plt.plot(x_lux, lux_low, label='Low')
plt.plot(x_lux, lux_med, label='Medium')
plt.plot(x_lux, lux_high, label='High')
plt.title("Освещенность (Lux)")
plt.xlabel("Люкс")
plt.ylabel("μ")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# --- Время суток (0–24 часов) ---
x_hour = np.linspace(0, 24, 1000)
time_morning = triangular(x_hour, 5, 8, 11)
time_day = triangular(x_hour, 10, 14, 18)
time_evening = triangular(x_hour, 17, 19, 21)
time_night = np.maximum(decreasing_linear(x_hour, 0, 6), increasing_linear(x_hour, 18, 24))

plt.figure(figsize=(8, 4))
plt.plot(x_hour, time_morning, label='Morning')
plt.plot(x_hour, time_day, label='Day')
plt.plot(x_hour, time_evening, label='Evening')
plt.plot(x_hour, time_night, label='Night')
plt.title("Время суток")
plt.xlabel("Часы")
plt.ylabel("μ")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# --- Яркость света (0–100%) ---
x_brightness = np.linspace(0, 100, 1000)
brightness_min = decreasing_linear(x_brightness, 0, 30)
brightness_med = triangular(x_brightness, 20, 50, 80)
brightness_high = triangular(x_brightness, 60, 75, 90)
brightness_max = increasing_linear(x_brightness, 70, 100)

plt.figure(figsize=(8, 4))
plt.plot(x_brightness, brightness_min, label='Min')
plt.plot(x_brightness, brightness_med, label='Medium')
plt.plot(x_brightness, brightness_high, label='High')
plt.plot(x_brightness, brightness_max, label='Max')
plt.title("Яркость освещения (%)")
plt.xlabel("Яркость (%)")
plt.ylabel("μ")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()