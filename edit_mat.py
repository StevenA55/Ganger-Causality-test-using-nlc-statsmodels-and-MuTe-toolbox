'''
This code edits a .mat file to rename its content to 'data'. It is used for the MuTe toolbox
'''
import scipy.io

file = 'SUJETO_5655.mat'
# Load the .mat file
mat = scipy.io.loadmat(file, simplify_cells=True)

# Check the content
print(mat.keys())  # To view the keys (variables) in the file

# Rename the variable 'Matriz' to 'data'
if 'Matriz' in mat:
    mat['data'] = mat['Matriz']
    del mat['Matriz']  # Remove the original variable

# Save the file with the new variable name
scipy.io.savemat(file, mat)