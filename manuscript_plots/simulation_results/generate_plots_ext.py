import pandas as pd

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


with open("ext_top_shift_mason.tikz", "w") as f:
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
    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "xlabel=Iterations, "\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(1.05, 1.0)}, anchor=north west},"\
            "ylabel=Mean CS\\textsubscript{L}]\n")

    for i, size in enumerate(network_sizes):
        for g in ["max_avg_bet"]:
            f.write("\\addplot +[mark=none, dashed, thick, "\
                    "color=Dark27qual{2}] "\
                    "table[col sep=comma, x=it, y=GG_mean] "\
                    "{{simulation_results/ext_top_shift_{0}_{1}.csv}};\n".format(g, size, i))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0} {1}}}\n".format(label, size))

    for i, size in enumerate(network_sizes):
        for g in ["min_avg_bet"]:
            f.write("\\addplot +[mark=none, solid, thick, "\
                    "color=Dark27qual{2}] "\
                    "table[col sep=comma, x=it, y=GG_mean] "\
                    "{{simulation_results/ext_top_shift_{0}_{1}.csv}};\n".format(g, size, i))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0} {1}}}\n".format(label, size))

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")

    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "at={(0, -.41\\linewidth)}, xlabel=Iterations,"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(0, -0.2)}, anchor=north west},"\
            "ylabel=Mean CS\\textsubscript{G}]\n")

    for i, size in enumerate(network_sizes):
        for g in ["max_avg_bet"]:
            f.write("\\addplot +[mark=none, dashed, thick, "\
                    "color=Dark27qual{2}] "\
                    "table[col sep=comma, x=it, y=CL_mean] "\
                    "{{simulation_results/ext_top_shift_{0}_{1}.csv}};\n".format(g, size, i))
            label = g.replace("_", " ")
            #f.write("\\addlegendentry{{{0} {1}}}\n".format(label, size))

    for i, size in enumerate(network_sizes):
        for g in ["min_avg_bet"]:
            f.write("\\addplot +[mark=none, solid, thick, "\
                    "color=Dark27qual{2}] "\
                    "table[col sep=comma, x=it, y=CL_mean] "\
                    "{{simulation_results/ext_top_shift_{0}_{1}.csv}};\n".format(g, size, i))
            label = g.replace("_", " ")
            #f.write("\\addlegendentry{{{0} {1}}}\n".format(label, size))

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")
    f.write("\\end{tikzpicture}\n")


with open("ext_top_shift_hub.tikz", "w") as f:
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
    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "xlabel=Iterations, "\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(1.05, 1.0)}, anchor=north west},"\
            "ylabel=Mean CS\\textsubscript{L}]\n")

    for i, size in enumerate(network_sizes):
        f.write("\\addplot +[mark=none, dashed, thick, "\
                "color=Dark27qual{1}] "\
                "table[col sep=comma, x=it, y=GG_mean] "\
                "{{simulation_results/ext_top_shift_hub_speaker_{0}.csv}};\n".format(size, i))
        label = g.replace("_", " ")
        f.write("\\addlegendentry{{star hearer {0}}}\n".format(size))

    for i, size in enumerate(network_sizes):
        f.write("\\addplot +[mark=none, solid, thick, "\
                "color=Dark27qual{1}] "\
                "table[col sep=comma, x=it, y=GG_mean] "\
                "{{simulation_results/ext_top_shift_hub_hearer_{0}.csv}};\n".format(size, i))
        label = g.replace("_", " ")
        f.write("\\addlegendentry{{star speaker {0}}}\n".format(size))

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")

    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "at={(0, -.41\\linewidth)}, xlabel=Iterations,"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(0, -0.2)}, anchor=north west},"\
            "ylabel=Mean CS\\textsubscript{G}]\n")

    for i, size in enumerate(network_sizes):
        f.write("\\addplot +[mark=none, dashed, thick, "\
                "color=Dark27qual{1}] "\
                "table[col sep=comma, x=it, y=CL_mean] "\
                "{{simulation_results/ext_top_shift_hub_speaker_{0}.csv}};\n".format(size, i))
        label = g.replace("_", " ")

    for i, size in enumerate(network_sizes):
        f.write("\\addplot +[mark=none, solid, thick, "\
                "color=Dark27qual{1}] "\
                "table[col sep=comma, x=it, y=CL_mean] "\
                "{{simulation_results/ext_top_shift_hub_hearer_{0}.csv}};\n".format(size, i))
        label = g.replace("_", " ")

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")
    f.write("\\end{tikzpicture}\n")


with open("ext_env_shift_hub.tikz", "w") as f:
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
    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "xlabel=Iterations, "\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(1.05, 1.0)}, anchor=north west},"\
            "ylabel=Mean CS\\textsubscript{L}]\n")

    for i, size in enumerate(network_sizes):
        f.write("\\addplot +[mark=none, dashed, thick, "\
                "color=Dark27qual{1}] "\
                "table[col sep=comma, x=it, y=GG_mean] "\
                "{{simulation_results/ext_env_shift_hub_speaker_{0}.csv}};\n".format(size, i))
        label = g.replace("_", " ")
        f.write("\\addlegendentry{{star hearer {0}}}\n".format(size))

    for i, size in enumerate(network_sizes):
        f.write("\\addplot +[mark=none, solid, thick, "\
                "color=Dark27qual{1}] "\
                "table[col sep=comma, x=it, y=GG_mean] "\
                "{{simulation_results/ext_env_shift_hub_hearer_{0}.csv}};\n".format(size, i))
        label = g.replace("_", " ")
        f.write("\\addlegendentry{{star speaker {0}}}\n".format(size))

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")

    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "at={(0, -.41\\linewidth)}, xlabel=Iterations,"\
            "axis background/.style={fill=color0},"\
            "grid=both, grid style={white},"\
            "axis line style={white},"\
            "every tick/.style={white},"\
            "legend style={\n"\
            "at={(0, -0.2)}, anchor=north west},"\
            "ylabel=Mean CS\\textsubscript{G}]\n")

    for i, size in enumerate(network_sizes):
        f.write("\\addplot +[mark=none, dashed, thick, "\
                "color=Dark27qual{1}] "\
                "table[col sep=comma, x=it, y=CL_mean] "\
                "{{simulation_results/ext_env_shift_hub_speaker_{0}.csv}};\n".format(size, i))
        label = g.replace("_", " ")

    for i, size in enumerate(network_sizes):
        f.write("\\addplot +[mark=none, solid, thick, "\
                "color=Dark27qual{1}] "\
                "table[col sep=comma, x=it, y=CL_mean] "\
                "{{simulation_results/ext_env_shift_hub_hearer_{0}.csv}};\n".format(size, i))
        label = g.replace("_", " ")

    f.write("\\draw[dashed] (axis cs:9999,-0.1) -- (axis cs:9999,1);\n")
    f.write("\\end{axis}\n")
    f.write("\\end{tikzpicture}\n")

