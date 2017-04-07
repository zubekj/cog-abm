import pandas as pd

def generate_plot(outfile, ylabels, plot_files, plot_styles, plot_labels=None,
                  columns=["GG_mean", "CL_mean"]):
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
                        "table[col sep=comma, x index=0, y={1}] "\
                        "{{simulation_results/{2}}};\n".format(style, columns[0],
                                                               plot))
                f.write("\\addlegendentry{{{0}}}\n".format(label))
        else:
            for plot, style in zip(plot_files, plot_styles):
                f.write("\\addplot +[mark=none, thick, {0}]"\
                        "table[col sep=comma, x index=0, y={1}] "\
                        "{{simulation_results/{2}}};\n".format(style, columns[0],
                                                               plot))

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
                    "table[col sep=comma, x index=0, y={1}] "\
                    "{{simulation_results/{2}}};\n".format(style, columns[1],
                                                           plot))

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

    ts = pd.read_csv("top_shift_results_final.csv")
    ts.columns = ["network", "it", "DG_CL_mean", "DG_CL_avar", "GG_mean",
                  "GG_avar", "CL_mean", "CL_avar", "DS_mean", "DS_avar"]
    ts["it"] /= 16
    for n1, g1 in ts.groupby("network"):
        g1.iloc[:,1:].to_csv("ext_top_shift_{0}_16.csv".format(n1), index=False)

    ts = pd.read_csv("env_shift_gauss_results_final.csv")
    ts.columns = ["network", "it", "DG_CL_mean", "DG_CL_avar", "GG_mean",
                  "GG_avar", "CL_mean", "CL_avar", "DS_mean", "DS_avar"]
    ts["it"] /= 16
    for n1, g1 in ts.groupby("network"):
        g1.iloc[:,1:].to_csv("ext_env_shift_{0}_16.csv".format(n1), index=False)


    networks = ["clique", "max_avg_bet", "min_avg_bet", "hub", "hub_speaker",
                "hub_hearer"]
    labels = ["fully connected", "max avg bet", "min avg bet", "star",
              "star hearer", "star speaker"]
    styles = ["dotted, color=Dark27qual0", "dashed, color=Dark27qual1",
              "dashed, color=Dark27qual2", "solid, color=Dark27qual3",
              "solid, color=Dark27qual4", "solid, color=Dark27qual5"]
    ylabels_top_shift = ["CS\\textsubscript{L}", "CS\\textsubscript{G}"]
    ylabels_env_shift = ["CS\\textsubscript{A}", "CS\\textsubscript{B}"]

    plot_files8 = ["ext_top_shift_{0}_8.csv".format(n) for n in networks]
    generate_plot("ext_top_shift_8.tikz", ylabels_top_shift, plot_files8,
                  styles)

    plot_files12 = ["ext_top_shift_{0}_12.csv".format(n) for n in networks]
    generate_plot("ext_top_shift_12.tikz", ylabels_top_shift, plot_files12,
                  styles)

    plot_files24 = ["ext_top_shift_{0}_24.csv".format(n) for n in networks]
    generate_plot("ext_top_shift_24.tikz", ylabels_top_shift, plot_files24,
                  styles)

    plot_files32 = ["ext_top_shift_{0}_32.csv".format(n) for n in networks]
    generate_plot("ext_top_shift_32.tikz", ylabels_top_shift, plot_files32,
                  styles)

    plot_files48 = ["ext_top_shift_{0}_48.csv".format(n) for n in networks]
    generate_plot("ext_top_shift_48.tikz", ylabels_top_shift, plot_files48,
                  styles, labels)

    plot_files8 = ["ext_env_shift_{0}_8.csv".format(n) for n in networks]
    generate_plot("ext_env_shift_8.tikz", ylabels_env_shift, plot_files8,
                  styles)

    plot_files12 = ["ext_env_shift_{0}_12.csv".format(n) for n in networks]
    generate_plot("ext_env_shift_12.tikz", ylabels_env_shift, plot_files12,
                  styles)

    plot_files24 = ["ext_env_shift_{0}_24.csv".format(n) for n in networks]
    generate_plot("ext_env_shift_24.tikz", ylabels_env_shift, plot_files24,
                  styles)

    plot_files32 = ["ext_env_shift_{0}_32.csv".format(n) for n in networks]
    generate_plot("ext_env_shift_32.tikz", ylabels_env_shift, plot_files32,
                  styles)

    plot_files48 = ["ext_env_shift_{0}_48.csv".format(n) for n in networks]
    generate_plot("ext_env_shift_48.tikz", ylabels_env_shift, plot_files48,
                  styles, labels)

    networks = ["clique", "max_avg_bet", "min_avg_bet", "hub", "hub_speaker",
                "hub_hearer", "max_avg_clust", "max_max_bet", "min_max_clos",
                "max_var_cons", "min_avg_clust", "max_max_clos"]
    labels = ["fully connected", "max avg bet", "min avg bet", "star",
              "star hearer", "star speaker", "max avg clust", "max max bet",
              "min max clos", "max var cons", "min avg clust",
              "max max clos"]
    styles = ["dotted, color=Dark27qual0", "dashed, color=Dark27qual1",
              "dashed, color=Dark27qual2", "solid, color=Dark27qual3",
              "solid, color=Dark27qual4", "solid, color=Dark27qual5",
              "dashed, color=Dark27qual0",
              "dashed, color=Dark27qual3",
              "dashed, color=Dark27qual4",
              "dashed, color=Dark27qual5",
              "dashed, color=Dark27qual6",
              "dashed, color=black",
              ]

    plot_files16 = ["ext_top_shift_{0}_16.csv".format(n) for n in networks]
    generate_plot("ext_top_shift_16.tikz", ylabels_top_shift, plot_files16,
                  styles, labels)

    plot_files16 = ["ext_env_shift_{0}_16.csv".format(n) for n in networks]
    generate_plot("ext_env_shift_16.tikz", ylabels_env_shift, plot_files16,
                  styles, labels)
