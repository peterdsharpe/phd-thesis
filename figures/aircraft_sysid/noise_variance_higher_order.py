from common import *
from aerosandbox.tools.statistics import time_series_uncertainty_quantification as tsuq
from aerosandbox.tools.code_benchmarking import Timer

def synthesize_data_and_reconstruct_noise_variance(freq_signal, freq_sample, order=1):
    """
    Generates a synthetic dataset with known noise properties, and then reconstructs the noise variance using the
    specified-order method described above.

    The signal is assumed to be a sinusoid with some frequency, and the noise is assumed to be independent,
    homoscedastic, and normally-distributed.

    Args:
        freq_signal: Frequency of the underlying true signal [Hz]
        freq_sample: Data sample rate from the sensor [Hz]
        order: Order of the estimator to use [int]

    Returns: The true noise stanard deviation and the reconstructed (estimated) noise standard deviation.
    """
    ##### Synthetic Data Generation #####
    t = np.arange(0, 1, 1 / freq_sample)

    true_data = np.sin(2 * np.pi * freq_signal * t)

    true_noise_standard_deviation = 0.1
    noise = np.random.normal(size=len(true_data)) * true_noise_standard_deviation

    sensor_data = true_data + noise

    ##### Noise Variance Reconstruction #####
    estimated_noise_standard_deviation = tsuq.estimate_noise_standard_deviation(
        sensor_data,
        estimator_order=order
    )

    return true_noise_standard_deviation, estimated_noise_standard_deviation


fig, ax = plt.subplots(figsize=(8, 4))

freq_sample = 100000
freq_signals = freq_sample / np.logspace(0, 3, 1000)
orders = [1, 2, 3, 4, 8, 16, 64, 512]

colors = p.sns.color_palette('rainbow', n_colors=len(orders))

from tqdm import tqdm

for i, order in tqdm(enumerate(orders)):
    true, estimated = np.vectorize(synthesize_data_and_reconstruct_noise_variance)(
        freq_signal=freq_signals,
        freq_sample=freq_sample,
        order=order,
    )
    ratio = freq_sample / freq_signals
    error = np.abs(true - estimated) / true

    index_noise_floor = np.argwhere(
        # (np.arange(len(error)) > np.argmax(error)) & (error < 2 * np.median(error[-50:]))
        (np.arange(len(error)) > np.argmax(error)) & (error < freq_sample ** -0.5)
    )[0][0]

    c = p.adjust_lightness(colors[i], 0.6)

    # print(order)
    # print(np.mean(estimated[index_noise_floor+1:]), np.std(estimated[index_noise_floor+1:]))

    ax.loglog(
        ratio[:index_noise_floor + 1],
        error[:index_noise_floor + 1],
        label=f"{order}",
        alpha=0.8, color=c, linewidth=1,
        zorder=4 + len(orders) - i,
    )
    ax.loglog(
        ratio[index_noise_floor:],
        error[index_noise_floor:],
        alpha=0.1, color=c, linewidth=1,
        zorder=3,
    )

plt.xlim(left=2, right=(freq_sample / freq_signals)[-1])
plt.ylim(bottom=freq_sample ** -0.5 / 10)

plt.annotate(
    text="Nyquist Freq.,\n$\mathrm{Ratio}=2$",
    xy=(0, 0),
    xytext=(0, -20),
    xycoords="axes fraction",
    textcoords="offset points",
    ha="center",
    va="top",
    alpha=0.6,
    fontsize=8,
    arrowprops=dict(
        arrowstyle="simple",
        # connectionstyle="arc3,rad=0.2",
        linewidth=0,
        alpha=0.5,
        facecolor="k",
    ),
)
p.hline(
    y=freq_sample ** -0.5,
    text="Minimum Possible Estimator Error",
    text_kwargs=dict(
        fontsize=10
    ),
    text_ha="center",
    text_va="top",
    color="k",
    linestyle="--",
    alpha=0.5,
    zorder=2,
)

# plt.annotate(
#     text="For readability, lines are faded once they hit the theoretical\nminimum-possible estimator error, roughly $\\epsilon \\approx N^{-0.5}$",
#     xy=(0.02, 0.02),
#     xycoords="axes fraction",
#     ha="left",
#     va="bottom",
#     fontsize=9
# )

plt.legend(
    title="Estimator Order",
    ncols=2,
)
p.show_plot(
    # title="Performance of Higher-Order Data-Driven Noise Estimators",
    xlabel=r"Ratio of $\frac{\mathrm{Sample\ Frequency}}{\mathrm{Underlying\ Signal\ Frequency}}$",
    ylabel="Relative Error\nof Estimator\n\n" + r"$\epsilon = \left| \frac{ \sigma_{\mathrm{estimated}} - \sigma_{\mathrm{true}} }{\sigma_{\mathrm{true}}}\right|$",
    legend=False,
    # dpi=300,
    savefig="noise_variance_higher_order.pdf",
)
