import csv
import numpy as np
import matplotlib.pyplot as plt


def read_csv(csv_filename):
    csv_file = open(csv_filename)
    csv_data = csv.reader(csv_file, delimiter=',')
    data = [float(value) for value in csv_data.next()]
    return np.array(data)


def read_timestamp():
    label_filename = 'utt1.lab'
    label_file = open(label_filename)
    label_timestamp = []
    for line in label_file:
        data = line.split()
        start, end = int(data[0]), int(data[1]) # unit is 10^7 s
        # append [start_time, end_time]
        label_timestamp.append({'start' :   start,
                                'end'   :   end})
    label_file.close()

    return label_timestamp


def read_mcep(mcep_filename):
    mcep_file = open(mcep_filename)
    mcep = {'static-mean'       :   [],
            'delta-mean'        :   [],
            'delta-delta-mean'  :   [],
            'static-var'        :   [],
            'delta-var'         :   [],
            'delta-delta-var'   :   []}
    for line in mcep_file:
        line = line.split()
        if len(line) != 1:  # if it's not the line for state
            data = [float(x) for x in line]
            mcep['static-mean'].append(data[0])
            mcep['delta-mean'].append(data[1])
            mcep['delta-delta-mean'].append(data[2])
            mcep['static-var'].append(data[3])
            mcep['delta-var'].append(data[4])
            mcep['delta-delta-var'].append(data[5])
    mcep_file.close()

    # convert data to numpy array
    for data_name in mcep.keys():
        mcep[data_name] = np.array(mcep[data_name])

    return mcep


def read_dur(dur_filename):
    dur_file = open(dur_filename)
    dur = {'state-means'        :   [],
           'state-variances'    :   []}
    for line in dur_file:
        line = line.split()
        if len(line) != 1:  # if it's not the line for state
            data = [float(x) for x in line]
            dur['state-means'].append(data[0:5])
            dur['state-variances'].append(data[5:10])
    dur_file.close()

    # convert data to numpy array
    for data_name in dur.keys():
        dur[data_name] = np.array(dur[data_name])

    return dur


def repeat_expt(expt, dur_state_mean, state_num):
    expt_repeated = []
    for i, data in enumerate(expt):
        row = i / state_num
        col = i - row * state_num
        expt_repeated += [data] * dur_state_mean[row, col]

    return np.array(expt_repeated)


def mix_vectors(vectors):
    vector_num = len(vectors)
    mixed = []
    for i in range(len(vectors[0])):
        mixed += [vectors[j][i] for j in range(vector_num)]

    return np.array(mixed)


def gen_traj(mcep_filename, dur_filename):
    print 'generating trajectory using mel-cepstrum and duration expert ...'

    # read mean and var form the mel-cepstrum expert file
    mcep = read_mcep(mcep_filename)

    # read mean and var form the duration expert file
    dur = read_dur(dur_filename)

    state_num = 5   # number of states
    dur_state_mean = np.around(dur['state-means']).astype(int) # convert duration to int

    # repeat expt according to dur
    static_mean = repeat_expt(mcep['static-mean'], dur_state_mean, state_num)
    delta_mean = repeat_expt(mcep['delta-mean'], dur_state_mean, state_num)
    delta_delta_mean = repeat_expt(mcep['delta-delta-mean'], dur_state_mean, state_num)

    static_var = repeat_expt(mcep['static-var'], dur_state_mean, state_num)
    delta_var = repeat_expt(mcep['delta-var'], dur_state_mean, state_num)
    delta_delta_var = repeat_expt(mcep['delta-delta-var'], dur_state_mean, state_num)

    # generate mixed vectors (page 17, lecture 2)
    mean_bar = mix_vectors([static_mean, delta_mean, delta_delta_mean])
    var_bar = mix_vectors([static_var, delta_var, delta_delta_var])
    cov_bar = np.diag(var_bar)

    # generate W (page 17, lecture 2)
    w = [[+0.000000, +0.000000, +1.000000, +0.000000, +0.000000],
         [-0.200000, -0.100000, +0.000000, +0.100000, +0.200000],
         [+0.285714, -0.142857, -0.285714, -0.142857, +0.285714]]
    w = np.array(w)

    W = np.zeros([mean_bar.shape[0],    # initialise W with extra spaces
                 static_mean.shape[0] + (w.shape[1] / 2) * 2])
    for row in range(0, W.shape[0], 3):
        col = row / 3
        W[row:row+3, col:col+5] = w
    W = W[:, 2:-2]  # cut off extra spaces

    # calculate mean_q (red part, page 19, lecture 2)
    cov_bar_inv = np.linalg.inv(cov_bar)
    mean_q = np.linalg.inv(W.T.dot(cov_bar_inv).dot(W)).dot(W.T).dot(cov_bar_inv).dot(mean_bar)
    cov_q = np.linalg.inv(W.T.dot(cov_bar_inv).dot(W))

    return mean_q, cov_q, mean_bar, cov_bar, W


def plot_trajs(trajs, traj_names, traj_filename=None):
    plt.figure(figsize=(16,8))
    traj_plts = []
    for i in range(len(trajs)):
        traj_plt, = plt.plot(trajs[i])
        traj_plts.append(traj_plt)

    plt.title('Trajectory generated using mcep and dur')
    plt.xlabel('Frame')
    plt.ylabel('MFCC')
    plt.legend(traj_plts, traj_names)

    if traj_filename != None:
        plt.savefig(traj_filename)
    plt.show()


def read_gv(gv_filename):
    gv_file = open(gv_filename)
    gv_raw = []
    for line in gv_file:
        gv_raw.append(float(line))
    l = len(gv_raw)
    gv = {'mean'    :   gv_raw[0:l/2],
          'var'     :   gv_raw[l/2:]}
    gv_file.close()

    return gv


def add_gv_expert(mean_q, mean_bar, cov_bar, W, gv_filename, iteration):
    print 'adding global variance expert to the trajctory ...'

    C = mean_q.copy()
    M = mean_bar            # mixed mean of static, delta, delta-delta
    cov_bar_inv = np.linalg.inv(cov_bar)

    gv = read_gv(gv_filename)
    gv_mean, gv_var = gv['mean'][3], gv['var'][3]

    T = float(C.shape[0])   # length of frame
    w = 1 / (2 * T)         # weight controlling a balance between the two probabilities
    p_v = 1 / gv_var        # the corresponding entry in the precision matrix
    alpha = 0.15

    for i in range(iteration):
        # variance and mean of c
        c_bar, v_C  = np.mean(C), np.var(C)
        v_prime = -2 / T * p_v * (v_C - gv_mean) * (C - c_bar)
        delta_C = w * (-W.T.dot(cov_bar_inv).dot(W).dot(C) + W.T.dot(cov_bar_inv).dot(M)) + v_prime
        C += alpha * delta_C
        if i % 10 == 0:
            print '{i} iterations finished'.format(i=i+1)

    return C


def apply_gv_constriant(mean_q, cov_q, lmd):
    print 'applying lagrange multiplers to the trajectory ...'

    mu = mean_q.copy()
    P = np.linalg.inv(cov_q)
    b = P.dot(mu)
    T = float(mu.shape[0])  # length of frame
    J = np.eye(T) - 1.0 / float(T) * np.ones([T, T])

    in_bracket = P - lmd * J
    if np.all(np.linalg.eigvals(in_bracket) > 0):
        c_hat = np.dot(np.linalg.inv(in_bracket), b)
    else:
        print 'P - lambda * J must be positive definite.'
        c_hat = None

    return c_hat


def main():
    # preparation for plotting
    trajs = []
    traj_names = []

    # original
    origin = read_csv('mcep_original.csv')
    trajs.append(origin)
    traj_names.append('original')

    # 3.3.1
    mean_q, cov_q, mean_bar, cov_bar, W = gen_traj('expts/utt1.cmp.expt', 'expts/utt1.dur.expt')
    trajs.append(mean_q)
    traj_names.append('syn')

    # 3.3.2 (a)
    C = add_gv_expert(mean_q, mean_bar, cov_bar, W, 'expts/utt1.gv.expt', 250)
    trajs.append(C)
    traj_names.append('syn-gv-expert')
    
    # 3.3.2 (b)
    lmd = 7 # lambda
    c_hat = apply_gv_constriant(mean_q, cov_q, lmd)
    if c_hat != None:
        trajs.append(c_hat)
        traj_names.append('syn-gv-constriant')

    # plot all trajctories
    plot_trajs(trajs, traj_names, 'utt1_traj_dim-4.png')


if __name__ == '__main__':
    main()
