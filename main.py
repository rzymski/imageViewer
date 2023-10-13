import tkinter as tk
from imageApp import ImageApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()



# def get_values(line):
#     # Usuń komentarze i białe znaki z początku i końca linii
#     cleaned_line = line.split('#')[0].strip()
#     # Pomijaj puste linie
#     if not cleaned_line:
#         return None
#     values = cleaned_line.split()
#     return values
#
# import time
# file_name = "D:/zapisy_programow_python/grafikaKomputerowa/ps2/obrazy/ppm-test-07-p3-big.ppm"
# start_time = time.time()
# # 1
# allValues = []
# count = 0
# with open(file_name, "r") as ppm_file:
#     for line in ppm_file:
#         values = get_values(line)
#         if values:
#             allValues.extend(values)
#         count += 1
#         if count == 10:
#             break
#
# print(allValues)
#
# if allValues[0] != "P3":
#     raise ValueError("To nie jest plik PPM P3")
#
# width = allValues[0]
# height = allValues[1]
# max_color_value = allValues[2]
#
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Czas wykonania funkcji: {execution_time} sekundy")


# import time
# def get_values(text):
#     numbers = []
#     for line in text:
#         # Usuń komentarze i białe znaki z początku i końca linii
#         cleaned_line = line.split('#')[0].strip()
#         # Pomijaj puste linie
#         if not cleaned_line:
#             continue
#         # Podziel linię na pojedyncze wartości
#         values = cleaned_line.split()
#         # Dodaj każdą wartość do listy (jeśli jest liczbą)
#         for value in values:
#             try:
#                 number = float(value)
#                 numbers.append(number)
#             except ValueError:
#                 pass  # Pomijamy nieprawidłowe wartości
#     return numbers
#
# def read_ppm_p3(filename):
#     with open(filename, 'r') as ppm_file:
#         # Czytanie nagłówka
#         lines = ppm_file.readlines()
#         if lines[0] != "P3\n":
#             raise ValueError("To nie jest plik PPM P3")
#
#         values = get_values(lines[1:])
#         width = values[0]
#         height = values[1]
#         max_color_value = values[2]
#
#     return width, height, max_color_value, values[3:]
#
# if __name__ == "__main__":
#     start_time = time.time()
#     filename = "obrazy/ppm-test-07-p3-big.ppm"  # Zmień na nazwę swojego pliku PPM P3
#     width, height, max_color_value, image = read_ppm_p3(filename)
#     end_time = time.time()
#     execution_time = end_time - start_time
#     print(f"Czas wykonania funkcji: {execution_time} sekundy")
#     print(f"Szerokość: {width}")
#     print(f"Wysokość: {height}")
#     print(f"Maksymalna wartość koloru: {max_color_value}")

