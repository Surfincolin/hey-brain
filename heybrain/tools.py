# tools.py
# A helper file to keep the reuseable methods.
import numpy as np
from neurodsp import filt
from sklearn.decomposition import FastICA
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def assemble_sort_raw_data(raw_data):
    """Assembles, sorts and resets time
        of chunked brainflow data,
        assumes the time channel is 22
    """
    sequenced_data = []
    for chunk in raw_data:
        if len(sequenced_data) == 0:
            sequenced_data = chunk
        else:
            sequenced_data = np.concatenate((sequenced_data, chunk), axis=1)
        
    # sort by the time ch, 22 (brainflow)
    sorted_data = sequenced_data[:,sequenced_data[22].argsort()]
    sorted_data[22] = sorted_data[22] - min(sorted_data[22])

    return sorted_data

def get_event_list(sorted_data, ignored = []):
    """Extracts event information from
        sorted brainflow data, uses
        time ch 22 and label ch 23

        ignored: list of labels to ignore.
    """
    event_list = []
    for i in range(sorted_data.shape[1]):
        e_label = int(sorted_data[23][i])
        e_time = sorted_data[22][i]
        # 0 is no event
        if e_label != 0 and e_label not in ignored:
            # epoch start, start in epoch, label
            event_list.append([e_time, 0, e_label])
        
    return event_list

def filter_eeg(ch_datas, fs, f_range):
    """Filters each channel of the data with a 
    bandpass and notch filter (60Hz).

    f_range: tuple, (lower freq limit, upper freq limit)
    """
    pwr_f_range=(58,62)
    filtered = []
    for ch in ch_datas:
        # Standard bandpass
        sig_filt = filt.filter_signal(sig=ch,
                                    fs=fs,
                                    pass_type='bandpass',
                                    f_range=f_range,
                                    filter_type='iir',
                                    butterworth_order=2)

        # tests the bandstop
        test_filt = filt.filter_signal(sig=sig_filt,
                                    fs=fs,
                                    pass_type='bandstop',
                                    f_range=pwr_f_range,
                                    n_seconds=1)

        # find edges
        num_nans = sum(np.isnan(test_filt))
        #buffer edges
        sig_filt = np.concatenate(([0]*(num_nans//2), sig_filt, [0]*(num_nans//2)))
        # actual bandstop
        sig_filt = filt.filter_signal(sig=sig_filt,
                                    fs=fs,
                                    pass_type='bandstop',
                                    f_range=pwr_f_range,
                                    n_seconds=1)
        # remove any edge artifacts
        sig_filt = sig_filt[~np.isnan(sig_filt)]
        
        filtered.append(sig_filt)
    
    return np.array(filtered)

def plot_all_channels(ch_data, size=(12,8), fs=250):
    """plot all eeg channels, overlapping each other
    """
    samples = len(ch_data[0])
    time = int(samples/fs) * 1000
    t_ax = np.linspace(0, time, samples)

    # figure(figsize=size)
    fig, ax = plt.subplots(1, figsize=size)
    for ch in ch_data:
        ax.plot(t_ax,ch)



def center_channels(data):
    centered = []
    for ch in data:
        centered.append(ch - ch.mean())
    
    return np.array(centered)

def get_channel_threshold_count(channel, threshold):
    abs_ch = abs(channel)
    return np.sum(np.where(abs_ch > threshold))

def get_theshold_greatest(ch_data, threshold=0.05):
    max_ch = None
    cur_max = 0
    for i, ch in enumerate(ch_data):
        count = get_channel_threshold_count(ch, threshold)
        if count > cur_max:
            cur_max = count
            max_ch = i
            
    if max_ch == None:
        print('Warning: no channel data above threshold. Return 0 channel')
        
    return max_ch

class ICAFilter:
    """Get ICA mixing and unmixing matrices.
        Uses sklearn FastICA
    """
    def __init__(self, ch_data_segment, threshold=0.05, n_components=5, iter_limit=200, component_thr=None):
        self.analysis_epoch = ch_data_segment
        self.threshold = component_thr if component_thr is not None else threshold
        self.iter_limit = iter_limit
        
        if len(ch_data_segment) < n_components:
            n_components = len(ch_data_segment)
            
        self.n_components = n_components
        
    def fit(self):
        """When using sklearn FastICA, data should be shaped as (samples x channels)
            That is also the format of it's transform option. This ICAFilter favors
            a format of (channels x samples). Along with mixing matrices, you will
            see the occasional '.T' to transpose the data.
        """
        self.ica  = FastICA(n_components=self.n_components, max_iter=self.iter_limit)
        transformed = self.ica.fit_transform(self.analysis_epoch.T)
        unmixing = self.ica.components_
        thesh = np.ones((self.analysis_epoch.shape[0], 1)) * self.threshold
        # print(unmixing.shape)
        # print(thesh.shape)
        thresh_transform = max(abs(np.dot(unmixing, thesh)[:,0]))
        print('comp. thresh:', thresh_transform)
        # print(thresh_transform)
        # print(transformed.shape)
        # filter_ch = get_theshold_greatest(transformed.T, thresh_transform)
        for comp in transformed.T:
            std = np.std(comp)
            u = np.mean(comp)
            comp = (comp - u)/ std

        # filter_ch = transformed.T
        # filter channel by modifying mix and unmix matrices
        mixing = self.ica.mixing_
        # print(filter_ch)
        # print(mixing.shape)
        # mixing[:,filter_ch] = 0
        self.cleaning_matrix = np.dot(mixing, unmixing)
        
    def clean(self, ch_data):
        return np.dot(self.cleaning_matrix, ch_data)

    def plot_components(self):
        fig, ax = plt.subplots(2)
        fig.suptitle('Components')
        transformed = np.dot(self.ica.components_, self.analysis_epoch).T
        for sig in transformed.T:
            ax[0].plot(sig)

        for comp in transformed.T:
            std = np.std(comp)
            u = np.mean(comp)
            comp = (comp - u)/ std

        for sig in transformed.T:
            ax[1].plot(sig)

        plt.tight_layout()
        plt.show()