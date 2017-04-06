import pandas as pd

def generate_plot(outfile, ylabels, plot_files, plot_styles, plot_labels=None):
    with open(outfile, "w") as f:
        f.write("\\begin{tikzpicture}\n")
        f.write("\\definecolor{color0}{rgb}{0.917647058823529,0.917647058823529,0.949019607843137}")
        f.write("""
                \\definecolor{Dark27qual0}{RGB}{27,158,119}
                \\definecolor{Dark27qual1}{RGB}{217,95,2}
                \\definecolor{Dark27qual2}{RGB}{117,112,179}
                \\definecolor{Dark27qual3}{RGB}{231,41,138}
                \\definecolor{Dark27qual4}{RGB}{102,166,30}
                \\definecolor{Dark27qual5}{RGB}{230,171,2}
                \\definecolor{Dark27qual6}{RGB}{166,118,29}
                """)
        f.write("\\begin{axis}[width=.53\\linewidth, height=.35\\linewidth, ymax=0.9,"\
                "at={(0, 0)}, xlabel=Iters per node, "\
                "axis background/.style={fill=color0},"\
                "grid=both, grid style={white},"\
                "axis line style={white},"\
                "every tick/.style={white},"\
                "legend columns=3,\n"\
                "legend style={\n"\
                "at={(0, -0.3)}, anchor=north west}," +\
                "ylabel={0}]\n".format(ylabels[0]))

        if plot_labels is not None:
            for plot, style, label in zip(plot_files, plot_styles, plot_labels):
                f.write("\\addplot +[mark=none, thick, {0}]"\
                        "table[col sep=comma, x=it, y=GG_mean] "\
                        "{{simulation_results/{1}}};\n".format(style, plot))
                f.write("\\addlegendentry{{{0}}}\n".format(label))
        else:
            for plot, style in zip(plot_files, plot_styles):
                f.write("\\addplot +[mark=none, thick, {0}]"\
                        "table[col sep=comma, x=it, y=GG_mean] "\
                        "{{simulation_results/{1}}};\n".format(style, plot))

        f.write("\\draw[dashed] (axis cs:650,-0.1) -- (axis cs:650,1);\n")
        f.write("\\end{axis}\n")

        f.write("\\begin{axis}[width=.53\\linewidth, height=.35\\linewidth, ymax=0.9,"\
                "at={(0.5\\linewidth, 0)}, xlabel=Iters per node,"\
                "axis background/.style={fill=color0},"\
                "grid=both, grid style={white},"\
                "axis line style={white},"\
                "every tick/.style={white}," +\
                "ylabel={0}]\n".format(ylabels[1]))

        for plot, style in zip(plot_files, plot_styles):
            f.write("\\addplot +[mark=none, thick, {0}]"\
                    "table[col sep=comma, x=it, y=CL_mean] "\
                    "{{simulation_results/{1}}};\n".format(style, plot))

        f.write("\\draw[dashed] (axis cs:650,-0.1) -- (axis cs:650,1);\n")
        f.write("\\end{axis}\n")
        f.write("\\end{tikzpicture}\n")


if __name__ == "__main__":

    ts = pd.read_csv("ext_top_shift_results_vi.csv")

    network_sizes = []
    for n1, g1 in ts.groupby("network_size"):
        for n2, g2 in g1.groupby("network"):
            mean_values = g2.groupby("it").mean()
            mean_values.index = mean_values.index / int(n1)
            mean_values.to_csv("ext_top_shift_{0}_{1}.csv".format(n2, n1))
        network_sizes.append(n1)

    ts = pd.read_csv("ext_env_shift_results_vi.csv")

    network_sizes = []
    for n1, g1 in ts.groupby("network_size"):
        for n2, g2 in g1.groupby("network"):
            mean_values = g2.groupby("it").mean()
            mean_values.index = mean_values.index / int(n1)
            mean_values.to_csv("ext_env_shift_{0}_{1}.csv".format(n2, n1))
        network_sizes.append(n1)

    networks = ["clique", "max_avg_bet", "min_avg_bet", "hub", "hub_speaker",
                "hub_hearer"]
    labels = ["fully connected", "max avg bet", "min avg bet", "star",
              "star hearer", "star speaker"]
    styles = ["dotted, color=Dark27qual0", "dashed, color=Dark27qual1",
              "dashed, color=Dark27qual2", "solid, color=Dark27qual3",
              "solid, color=Dark27qual4", "solid, color=Dark27qual5"]
    ylabels = ["CS\\textsubscript{L}", "CS\\textsubscript{G}"]

    plot_files8 = ["ext_top_shift_{0}_8.csv".format(n) for n in networks]
    generate_plot("ext_top_shift_8.tikz", ylabels, plot_files8, styles)

    plot_files12 = ["ext_top_shift_{0}_12.csv".format(n) for n in networks]
    generate_plot("ext_top_shift_12.tikz", ylabels, plot_files12, styles)

    plot_files24 = ["ext_top_shift_{0}_24.csv".format(n) for n in networks]
    generate_plot("ext_top_shift_24.tikz", ylabels, plot_files24, styles)

    plot_files32 = ["ext_top_shift_{0}_32.csv".format(n) for n in networks]
    generate_plot("ext_top_shift_32.tikz", ylabels, plot_files32, styles)

    plot_files48 = ["ext_top_shift_{0}_48.csv".format(n) for n in networks]
    generate_plot("ext_top_shift_48.tikz", ylabels, plot_files48, styles,
                  labels)
