# import tkinter as tk
# from imageApp import ImageApp
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ImageApp(root)
#     root.mainloop()


# from PIL import Image
# import time
# start_time = time.time()
# def skip_comments_and_read_next_line(file):
#     while True:
#         line = file.readline().decode("ansi").strip()
#         cleaned_line = line.split('#')[0].strip()
#         if cleaned_line:
#             return cleaned_line
#
#
# with open("D:/zapisy_programow_python/grafikaKomputerowa/ps2/obrazy/ppm-test-08-p6-big.ppm", "rb") as ppm_file:
#     parameters = []
#     parameters.append(skip_comments_and_read_next_line(ppm_file))
#     while(len(parameters) < 4):
#         line = skip_comments_and_read_next_line(ppm_file)
#         lineValues = map(int, line.split())
#         parameters.extend(lineValues)
#     print(parameters)
#
#     binary_data = ppm_file.read()
#
#     # print(binary_data)
#
#     int_values = []
#     for byte in binary_data:
#         int_value = int(byte)
#         int_values.append(int_value)
#
#     # for value in int_values:
#     #     print(value)
#     print(f"Len = {len(int_values)}")
#
# image = Image.frombytes("RGB", (parameters[1], parameters[2]), binary_data)
# image.save("outputXD.jpg")
#
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Czas wykonania funkcji: {execution_time} sekundy")



from PIL import Image
import time

start_time = time.time()

def skip_comments_and_read_next_line(file):
    while True:
        line = file.readline().decode("ansi").strip()
        cleaned_line = line.split('#')[0].strip()
        if cleaned_line:
            return cleaned_line

def read_binary_data_in_chunks(file, chunk_size=4096):
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        for byte in chunk:
            yield int(byte)

with open("D:/zapisy_programow_python/grafikaKomputerowa/ps2/obrazy/ppm-test-08-p6-big.ppm", "rb") as ppm_file:
    parameters = []
    parameters.append(skip_comments_and_read_next_line(ppm_file))
    while len(parameters) < 4:
        line = skip_comments_and_read_next_line(ppm_file)
        lineValues = map(int, line.split())
        parameters.extend(lineValues)
    print(parameters)

    int_values = list(read_binary_data_in_chunks(ppm_file))

print(f"Len = {len(int_values)}")

image = Image.frombytes("RGB", (parameters[1], parameters[2]), bytes(int_values))
image.save("outputXD.jpg")

end_time = time.time()
execution_time = end_time - start_time
print(f"Czas wykonania funkcji: {execution_time} sekundy")



























# dziala dla wszystkich oprocz duzego
# def skip_comments_and_read_next_line(file):
#     while True:
#         line = file.readline().decode("ansi").strip()
#         if not line.startswith("#"):
#             return line
# with open("D:/zapisy_programow_python/grafikaKomputerowa/ps2/obrazy/ppm-test-03-p6.ppm", "rb") as ppm_file:
#     header = skip_comments_and_read_next_line(ppm_file)
#     if header != "P6":
#         raise ValueError("Not a PPM P6 file")
#
#     print(f"header = {header}")
#
#     dimensions = skip_comments_and_read_next_line(ppm_file)
#     width, height = map(int, dimensions.split())
#
#     print(f"Dimensions = {width} {height} razem = {width*height}*3={width*height*3}")
#
#     max_color = skip_comments_and_read_next_line(ppm_file)
#     max_color = int(max_color)
#
#     print(f"Max color = {max_color}")
#
#     binary_data = ppm_file.read()
#
#     # print(binary_data)
#
#     int_values = []
#     for byte in binary_data:
#         int_value = int(byte)
#         int_values.append(int_value)
#
#     # for value in int_values:
#     #     print(value)
#     print(f"Len = {len(int_values)}")
#
# image = Image.frombytes("RGB", (width, height), binary_data)
# image.save("output.jpg")
