import tkinter as tk
from imageApp import ImageApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()


# from PIL import Image
# import time
#
#
#
# def decodeSkipCommentsEmptyLines(file):
#     while True:
#         line = file.readline().decode("ansi").strip()
#         cleaned_line = line.split('#')[0].strip()
#         if cleaned_line:
#             return cleaned_line
#
#
# def readBinaryDataInChunks(file, chunk_size=4096):
#     while True:
#         chunk = file.read(chunk_size)
#         if not chunk:
#             break
#         for byte in chunk:
#             yield int(byte)
#
# start_time = time.time()
# with open("D:/zapisy_programow_python/grafikaKomputerowa/ps2/obrazy/ppm-test-08-p6-big.ppm", "rb") as ppm_file:
#     parameters = [decodeSkipCommentsEmptyLines(ppm_file)]
#     while len(parameters) < 4:
#         line = decodeSkipCommentsEmptyLines(ppm_file)
#         lineValues = map(int, line.split())
#         parameters.extend(lineValues)
#     print(parameters)
#
#     int_values = list(readBinaryDataInChunks(ppm_file))
#
# print(f"Len = {len(int_values)}")
#
# image = Image.frombytes("RGB", (parameters[1], parameters[2]), bytes(int_values))
# image.save("outputXD.jpg")
#
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Czas wykonania funkcji: {execution_time} sekundy")
