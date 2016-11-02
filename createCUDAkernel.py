#This code is used for converting kernels. The rest of the 
#code for this application will have the same extension as
#before

import os

#it will be used for creating a folder to put the files
cuda_path = "./CUDA_Files/"

#dictonary for substituitions on the kernel
subs_cl = {'__global':' ',
            'get_global_id(0)': 'blockIdx * blockDim + threadIdx',
            '__kernel':'__global__'}

#dictonary for changes on the main aplication
subs_main  = {'clReleaseMemObject': 'cudaFree'}

#asks for target file, has to be opencl
opencl_name = input("Whats the OpenCL  kernel file name? ")
main_name = input("Whats the C/C++ file name? ")

#checks if the name is indeed a .cl file
splited_name_cl = opencl_name.split(".")
splited_name_main = main_name.split(".")

#this part of the code checks the extensions of the files
if not((splited_name_cl[1] == "cl")):
    print(opencl_name + " is not a valid name. Exiting... ")
    exit()

if not((splited_name_main[1] == "c" or splited_name_main[1] == "cpp")):
    print(main_name + "is not a valid name. Exiting... ")
    exit()

#i'm doing separated try/except in order to find the problems
#use with open for a more secure method
try:
    opencl_data = open(opencl_name, 'r') 

#if something wrong happen, exit the code
except:
    print ("Not possible to open the opencl kernel. Exiting...")
    exit()

#try to open the main data to read
try:
    main_data = open(main_name, 'r')

except:
    print ("Not possible to open the main file to read. Exiting... ")
    exit()


#if everything works, try to create the cuda file and directory
cuda_name = ".".join([splited_name_cl[0], "cu"])
os.mkdir("CUDA_Files")

#creating the main file to be the resulting one
main_cuda_name = splited_name_main[0]+"_cuda."+splited_name_main[1]

#try to create the file to be the main converted file
try:
    main_data_write = open(cuda_path + main_cuda_name, "w")

except:
    print("Not possible to create main cuda file. Exiting... ")
    exit()
    
#try to create the file to be the cuda kernel
try:
    cuda_data = open(cuda_path + cuda_name, "w")

except:
    print ("Not possible to create the kernel file...")
    exit()

#replacing the dict items
for line in opencl_data:
    for key, value in subs_cl.items():
        line = line.replace(key,value)
    cuda_data.write(line)

#replacing the words on the main code
for line in main_data:
    for key, value in subs_main.items():
        line = line.replace(key,value)
    main_data_write.write(line)


#closes everything
main_data.close()
opencl_data.close()
cuda_data.close()
main_data_write.close()
