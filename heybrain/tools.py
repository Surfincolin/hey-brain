# tools.py
# A helper file to keep the reuseable methods.
import numpy as np
from neurodsp import filt
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

def plot_all_channels(ch_data, size=(12,8)):
    """plot all eeg channels, overlapping each other
    """
    figure(figsize=size)
    for ch in ch_data:
        plt.plot(ch)