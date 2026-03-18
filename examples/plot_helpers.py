import numpy as np
import matplotlib.pyplot as plt


DEFAULT_STYLE = {
	"font.size": 10,
	"axes.titlesize": 12,
	"axes.labelsize": 10,
	"xtick.labelsize": 9,
	"ytick.labelsize": 9,
}


def setup_plot_style():
	"""Apply common plot styling used across example notebooks."""
	plt.rcParams.update(DEFAULT_STYLE)


def plot_waveform(ax, x, fs, title="waveform", xlabel="time (sec)", ylabel="amplitude"):
	"""Plot a full waveform against time."""
	t = np.arange(x.size) / float(fs)
	ax.plot(t, x)
	ax.set_title(title)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_xlim([0, x.size / float(fs)])


def plot_stft_mag_phase(
	axes,
	mX,
	pX,
	fs,
	N,
	H,
	max_plot_freq=5000.0,
	mag_title="magnitude spectrogram (dB)",
	phase_title="phase difference spectrogram",
):
	"""Plot STFT magnitude and phase-difference spectrograms."""
	num_frames = mX.shape[0]
	frame_time = H * np.arange(num_frames) / float(fs)
	n_bins = int(N * max_plot_freq / fs) + 1
	bin_freq = fs * np.arange(n_bins) / N

	axes[0].pcolormesh(frame_time, bin_freq, np.transpose(mX[:, :n_bins]), shading="auto")
	axes[0].set_xlabel("time (sec)")
	axes[0].set_ylabel("frequency (Hz)")
	axes[0].set_title(mag_title)
	axes[0].autoscale(tight=True)

	phase_diff = np.diff(pX[:, :n_bins], axis=1)
	axes[1].pcolormesh(frame_time, bin_freq[:-1], np.transpose(phase_diff), shading="auto")
	axes[1].set_xlabel("time (sec)")
	axes[1].set_ylabel("frequency (Hz)")
	axes[1].set_title(phase_title)
	axes[1].autoscale(tight=True)


def plot_dft_frame_analysis(
	axes,
	x_frame,
	w_frame,
	mX,
	pX,
	y_frame,
	fs,
	N,
	time_axis=None,
	frame_time=None,
):
	"""Plot time-domain windowed frame, DFT magnitude/phase, and synthesized frame."""
	if time_axis is None:
		if frame_time is None:
			frame_time = 0.0
		time_axis = frame_time + (np.arange(x_frame.size) / float(fs))

	freq_axis = fs * np.arange(mX.size) / float(N)

	axes[0].plot(time_axis, x_frame * w_frame)
	axes[0].set_title("windowed frame in time domain")
	axes[0].set_xlabel("time (sec)")
	axes[0].set_ylabel("amplitude")

	axes[1].plot(freq_axis, mX, color="tab:red")
	axes[1].set_title("magnitude spectrum from dftAnal (dB)")
	axes[1].set_xlabel("frequency (Hz)")
	axes[1].set_ylabel("magnitude (dB)")

	axes[2].plot(freq_axis, pX, color="tab:green")
	axes[2].set_title("phase spectrum from dftAnal (rad)")
	axes[2].set_xlabel("frequency (Hz)")
	axes[2].set_ylabel("phase (rad)")

	axes[3].plot(time_axis, y_frame, color="tab:orange")
	axes[3].set_title("generated frame from dftSynth")
	axes[3].set_xlabel("time (sec)")
	axes[3].set_ylabel("amplitude")


def plot_spectrogram(
	ax,
	mX,
	fs,
	N,
	H,
	time_offset=0.0,
	max_plot_freq=5000.0,
	title="spectrogram",
	xlabel="time (sec)",
	ylabel="frequency (Hz)",
	cmap=None,
):
	"""Plot a magnitude spectrogram up to a maximum frequency."""
	num_frames = mX.shape[0]
	frame_time = time_offset + H * np.arange(num_frames) / float(fs)
	n_bins = int(N * max_plot_freq / fs) + 1
	bin_freq = fs * np.arange(n_bins) / N

	kwargs = {"shading": "auto"}
	if cmap is not None:
		kwargs["cmap"] = cmap

	ax.pcolormesh(frame_time, bin_freq, np.transpose(mX[:, :n_bins]), **kwargs)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_title(title)
	ax.autoscale(tight=True)


def plot_spectrogram_with_tracks(
	ax,
	mX,
	tracks,
	fs,
	N,
	H,
	time_offset=0.0,
	max_plot_freq=5000.0,
	title="spectrogram + tracks",
	track_color="k",
	track_linewidth=0.8,
	track_alpha=1.0,
	cmap=None,
):
	"""Plot a spectrogram with overlaid frequency tracks."""
	plot_spectrogram(ax, mX, fs, N, H, time_offset=time_offset, max_plot_freq=max_plot_freq, title=title, cmap=cmap)

	track_times = time_offset + H * np.arange(tracks.shape[0]) / float(fs)
	tracks_plot = np.array(tracks, copy=True)
	tracks_plot[tracks_plot <= 0] = np.nan
	tracks_plot[tracks_plot > max_plot_freq] = np.nan
	ax.plot(track_times, tracks_plot, color=track_color, linewidth=track_linewidth, alpha=track_alpha)


def plot_frequency_tracks(
	ax,
	tracks,
	fs,
	H,
	time_offset=0.0,
	title="frequency tracks",
	xlabel="time (sec)",
	ylabel="frequency (Hz)",
	max_freq=None,
	linewidth=0.8,
	color=None,
	alpha=1.0,
):
	"""Plot one or more frequency tracks over time."""
	frame_time = time_offset + H * np.arange(tracks.shape[0]) / float(fs)
	tracks_plot = np.array(tracks, copy=True)
	tracks_plot[tracks_plot <= 0] = np.nan
	if max_freq is not None:
		tracks_plot[tracks_plot > max_freq] = np.nan

	plot_kwargs = {"linewidth": linewidth, "alpha": alpha}
	if color is not None:
		plot_kwargs["color"] = color

	ax.plot(frame_time, tracks_plot, **plot_kwargs)
	ax.set_title(title)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	if max_freq is not None:
		ax.set_ylim([0, max_freq])


def plot_spectrum(ax, freqs, values, title="spectrum", xlabel="frequency (Hz)", ylabel="magnitude (dB)", color=None, linewidth=1.5, label=None, linestyle="-"):
	"""Plot a single spectrum or curve against frequency."""
	plot_kwargs = {"linewidth": linewidth, "linestyle": linestyle}
	if color is not None:
		plot_kwargs["color"] = color
	if label is not None:
		plot_kwargs["label"] = label

	ax.plot(freqs, values, **plot_kwargs)
	ax.set_title(title)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)


def plot_spectrum_series(
	ax,
	freqs,
	series,
	title="spectrum comparison",
	xlabel="frequency (Hz)",
	ylabel="magnitude (dB)",
	legend=True,
	grid_alpha=0.25,
):
	"""Plot multiple spectra or curves on a shared axis."""
	for item in series:
		plot_kwargs = {
			"linewidth": item.get("linewidth", 1.5),
			"linestyle": item.get("linestyle", "-"),
		}
		if "color" in item:
			plot_kwargs["color"] = item["color"]
		if "label" in item:
			plot_kwargs["label"] = item["label"]
		if "marker" in item:
			plot_kwargs["marker"] = item["marker"]
		if "markersize" in item:
			plot_kwargs["markersize"] = item["markersize"]
		if "alpha" in item:
			plot_kwargs["alpha"] = item["alpha"]
		if "mew" in item:
			plot_kwargs["mew"] = item["mew"]

		ax.plot(item.get("x", freqs), item["y"], **plot_kwargs)

	ax.set_title(title)
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	if legend:
		ax.legend(loc="best")
	if grid_alpha is not None:
		ax.grid(alpha=grid_alpha)
