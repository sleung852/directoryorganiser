import os
import argparse
#from tqdm import tqdm

class DirectoryOrganiser:

	def __init__(self, directory=None):
		if directory is None:
			self.directory = os.getcwd()
		else:
			self.directory = directory
		self.files_list = []
		self.file_ext_dict = {}
		self.file_map_dict = {
				'Images': ['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif', 'jfif'],
				'Microsoft Files': ['doc', 'docx', 'docm', 'xlsx', 'xls','csv', 'ppt', 'pptx'],
				'PDFs': ['pdf'],
				'Programs': ['py', 'ipynb'],
				'Others': []
			}
		print("DirectoryOrganiser is initialised!")
		#print(self.directory)

	def directory_report_by_extensions(self):

		for file in os.listdir(self.directory):
			if not os.path.isdir(file):
				self.files_list.append(file)
		
		for file_name in self.files_list:
			if not os.path.isdir(file_name):
				file_ext = file_name.split('.')[-1]
				if file_ext not in self.file_ext_dict.keys():
					self.file_ext_dict[file_ext] = 1
				else:
					self.file_ext_dict[file_ext] += 1

		for file_ext, count in self.file_ext_dict.items():
			print("{} | {}".format(file_ext, count))

		print("")

	def check_folders_exist(self):
		report_bool = False

		for folder_name in self.file_map_dict.keys():
			file_dir = os.path.join(self.directory, folder_name)
			if not os.path.isdir(file_dir):
				os.mkdir(file_dir)
				report_bool = True

		if report_bool:
			print("Folders have been created.")
		else:
			print("Folders already existed.")

	def organise_directory_by_extensions(self, test_mode=False):

		self.check_folders_exist()

		if len(self.files_list) == 0:
			self.directory_report_by_extensions()

		for file_name in self.files_list:
			file_ext = file_name.split('.')[-1]
			cur_loc = os.path.join(self.directory, file_name)
			other_bools = True
			error_list = []
			try:
				for folder, exts in self.file_map_dict.items():
					if file_ext in exts:
						new_loc = os.path.join(self.directory, folder, file_name)
						if test_mode:
							print("moving {} from {} to {}\n".format(file_name, cur_loc, new_loc))
						else:
							os.rename(cur_loc, new_loc)
						print ("Successfully moved {}".format(file_name))
						other_bools = False
						break
				if other_bools:
					new_loc = os.path.join(self.directory, "Others", file_name)
					if test_mode:
						print("moving {} from {} to {}\n".format(file_name, cur_loc, new_loc))
					else:
						os.rename(cur_loc, new_loc)
			except:
				error_list.append(file_name)

		print('\nDone!\n')
		if len(error_list) > 0:
			print("However the Organiser is unable to re-arrange the following files:")
			for file in error_list:
				print(file)


parser = argparse.ArgumentParser(description='Order the target directory files and sort them into different folders depending on their extensions')
parser.add_argument('--directory', metavar='directory', type=str, nargs=1,
                    help='customised directory - else default current working directory')
args = parser.parse_args()

if args.directory is None:
	do = DirectoryOrganiser(args.directory)
else:
	do = DirectoryOrganiser(args.directory[0])

do.organise_directory_by_extensions()