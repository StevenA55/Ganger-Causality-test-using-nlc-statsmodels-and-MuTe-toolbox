'''
This code evaluates GC using the nlc library, creates an 8x8 matrix, and saves it.

'''

import numpy as np
import scipy.io
import nonlincausality as nlc
def nonlincausality_f(bands,file):

    band_names = list(bands.keys())
    data = np.column_stack(list(bands.values()))

    train_size = int(len(data) * 0.6)
    val_size = int(len(data) * 0.2)

    data_train = data[:train_size]    
    data_val = data[train_size:train_size + val_size]  
    data_test = data[train_size + val_size:] 
    p_nlc = []
    all_results = {}
    # Change these lines according to what you need.
    lags = 15
    neurons_range = range(2, 25, 5)
    #
    for i in range (1):
        for j in range (2):  
            if i != j:

                signal_key = f'{band_names[i]} -> {band_names[j]}'
                all_results[signal_key] = {}
                
                min_p_value = float('inf')
                best_neurons = None
                best_lag = None
                
                X_train = data_train[:, j]  
                Y_train = data_train[:, i] 
                X_val = data_val[:, j]
                Y_val = data_val[:, i]
                X_test = data_test[:, j]
                Y_test = data_test[:, i]

                train_data = np.column_stack([X_train, Y_train])
                val_data = np.column_stack([X_val, Y_val])
                test_data = np.column_stack([X_test, Y_test])
                
                z_indices = [k for k in range(len(band_names)) if k != i and k != j]
                Z_train = data_train[:, z_indices] 
                Z_val = data_val[:, z_indices]
                Z_test = data_test[:, z_indices]

                for n_neurons in neurons_range:
                    
                    neuron_key = f'neurons_{n_neurons}'
                    all_results[signal_key][neuron_key] = {}
                    result = nlc.nonlincausalityNN(
                        x=train_data,  
                        maxlag=lags,  
                        NN_config=['d', 'dr', 'd', 'dr'],  
                        NN_neurons=[n_neurons, 0.05, n_neurons, 0.05],  
                        x_test=test_data,  
                        run=1, 
                        z=Z_train,
                        z_test=Z_test,
                        epochs_num=[50, 50], 
                        learning_rate=[0.0001, 0.00001],  
                        batch_size_num=128,  
                        x_val=val_data,
                        z_val=Z_val,
                        reg_alpha=None,  
                        callbacks=None,  
                        verbose=False,  
                        plot=False
                    )
                    for lag in range(1, lags + 1):
                        if lag in result:
                            all_results[signal_key][neuron_key][f'lag_{lag}'] = result[lag]
                            current_p_value = result[lag].p_value
                            
                        if current_p_value < min_p_value:
                            min_p_value = current_p_value
                            best_neurons = n_neurons
                            best_lag = lag
                p_nlc.append((f'{band_names[i]} -> {band_names[j]}-{file}',f'neurons:{best_neurons}',f'lag:{best_lag}', min_p_value))   
                print(f"Completed {signal_key}")
            else:
                min_p_value = 1.0
                best_neurons = 0
                best_lag = 0
                p_nlc.append((f'{band_names[i]} -> {band_names[j]}',f'neurons:{best_neurons}',f'lag:{best_lag}', min_p_value))
    print(f"{file} done")        
    return all_results, p_nlc
def matrix_nlc(p_nlc):
    h = 0
    p_matrix_nlc = np.zeros((8, 8))
    for i in range(8):
       for j in range(8):
        p_matrix_nlc[i,j] = p_nlc[h][3]
        h = h+1
    
    return p_matrix_nlc

def save_mat(mat_path, p_matrix_nlc):
    scipy.io.savemat(mat_path, {'matrix_nlc': p_matrix_nlc})
    return
    