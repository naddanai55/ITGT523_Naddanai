import os
import splitfolders

directory = r"C:\Users\nparo\OneDrive\GT - Mahidol\Class\2nd\ITGT523 Computer Vision\ITGT523_Naddanai\Pokedex\7000_Labeled_Pokemon"
path = os.getcwd() 
output_path = path + "/output"
splitfolders.ratio(directory, output=output_path, seed=1337, ratio=(.8, 0.1, 0.1))