import requests
from bs4 import BeautifulSoup

def google_scholar_results(query, year):
    url = f'https://scholar.google.com/scholar?q={query}&hl=en&as_sdt=0%2C22&lookup=0&as_ylo={year}&as_yhi={year}'

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Bad response code: {response.status_code}.")
        print(response.headers)
        print(f"URL: '{url}'")
        input("Press enter to continue...")
        return google_scholar_results(query, year)

    soup = BeautifulSoup(response.text, 'html.parser')

    results = soup.find('div', id='gs_ab_md')

    if results.text == "":
        return 0
    elif results:
        try:
            words = results.text.split()
            if words[0].lower() == "about":
                words = words[1:]
            return int(words[0].replace(",", ""))
        except Exception as e:
            print(results.text)
            raise e
    else:
        raise ValueError


# print(google_scholar_results(
#     'aircraft "multidisciplinary design optimization"',
#     1992,
# ))

if __name__ == '__main__':
    queries = [
        r'"aircraft+design"',
        r'"aircraft+design"++"multidisciplinary design optimization"+OR+"MDO"+OR+"MDAO"',
        r'"aircraft+design"++"optimization"+OR+"MDO"+OR+"MDAO"',
        # r'"aircraft+design"++"optimization"'
    ]
    years = range(1980, 2023)

    import pandas as pd

    df = pd.DataFrame(index=years, columns=queries, dtype=int)

    try:
        with open("mdo_citation_counts.csv", "r") as f:
            df = pd.read_csv(f, index_col=0)
    except FileNotFoundError:
        pass

    for query in queries:
        for year in years:
            if pd.isna(df.loc[year, query]):
                df.loc[year, query] = google_scholar_results(query, year)
                print(f"{query}, {year}: {df.loc[year, query]:.0f}")
                with open("mdo_citation_counts.csv", "w+") as f:
                    df.to_csv(f)

    import matplotlib.pyplot as plt
    import aerosandbox.tools.pretty_plots as p

    fig, ax = plt.subplots(figsize=(6,3.2))

    # for query in
    x = df.index

    y_mdo = df.iloc[:, 1] / df.iloc[:, 0]
    y_opt = df.iloc[:, 2] / df.iloc[:, 0]

    plt.plot(x, y_mdo, label="MDO, specifically", color="C1")
    plt.plot(x, y_opt, label="MDO, or optimization more broadly", color="C0")
    plt.fill_between(x, 0, y_mdo, alpha=0.3, color="C1")
    plt.fill_between(x, 0, y_opt, alpha=0.3, color="C0")

    plt.annotate(
        text="MDO, specifically",
        xy=(x[-1], y_mdo.iloc[-1]),
        xytext=(5, 0),
        textcoords="offset points",
        color="C1",
        va="center",
    )
    plt.annotate(
        text="Either MDO or\noptimization\nmore broadly",
        xy=(x[-1], y_opt.iloc[-1]),
        xytext=(5, 0),
        textcoords="offset points",
        color="C0",
        va="center",
    )

    plt.xlim(x[0], x[-1])
    plt.ylim(bottom=0)

    # percent formatter
    from matplotlib.ticker import PercentFormatter
    ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))

    p.show_plot(
        "Percentage of Aircraft Design\npublications that mention...",
        "Publication Date",
        savefig="mdo_citation_counts.pdf",
        savefig_transparent=False,
        legend=False,
    )
