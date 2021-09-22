import os
import csv
import argparse
import PySimpleGUI as sg

def split_files(source, lines_limit):
	print("Splitting csv file...")
	total_lines = 0
	total_files = 0

	with open(source) as csv_file:
		header = csv_file.readline()
		total_files = 1

		output_folder = create_output_folder(source)
		file = start_new_csv_file(output_folder, header, total_files)

		for line_number, row in enumerate(csv_file):
			if (line_number % lines_limit == 0 and not line_number == 0):
				file.close()
				total_files += 1
				file = start_new_csv_file(output_folder, header, total_files)
				
			file.write(row)
			total_lines += 1
		file.close()

		print(f"{total_lines} rows split into {total_files} files.")

def start_new_csv_file(output_folder, header, current_file):
	file = open(f"{output_folder}/splitted{current_file}.csv", "w+")
	file.write(header)
	return file

def create_output_folder(source):
	folder_path = source.split(".csv")[0]
	os.makedirs(folder_path, exist_ok=True)
	return folder_path

def create_gui():
	layout = [
		[sg.Text("File"), sg.Input(size=(15,0), key="file"), sg.FileBrowse(button_text="Select",file_types=(("Csv Files", "*.csv"),))],
		[sg.Text("Rows per file"), sg.Input(size=(5,0), default_text="1000", key="lines_limit")],
		[sg.Button("Split!")]
	]

	window = sg.Window("CSV Splitter").layout(layout)
	return window

def read_gui(window):
	button, values = window.Read()
	file = values["file"]
	lines_limit = int(values["lines_limit"])
	return file, lines_limit

if __name__ == '__main__':
	window = create_gui()
	file, lines_limit = read_gui(window)
	split_files(file,lines_limit)
