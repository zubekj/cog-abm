import pandas as pd

ts = pd.read_csv("top_shift_results_final.csv", index_col=[0, 1])
ts.index.names = ["Topology", "Iteration"]

for g in ts.index.levels[0]:
    ts.loc[g].to_csv("top_shift_{0}.csv".format(g))

es = pd.read_csv("env_shift_results_final.csv", index_col=[0, 1])
es.index.names = ["Topology", "Iteration"]

for g in es.index.levels[0]:
    es.loc[g].to_csv("env_shift_{0}.csv".format(g))

es = pd.read_csv("env_shift_gauss_results_final.csv", index_col=[0, 1])
es.index.names = ["Topology", "Iteration"]

for g in es.index.levels[0]:
    es.loc[g].to_csv("env_shift_gauss_{0}.csv".format(g))


with open("top_shift_mason.tikz", "w") as f:
    f.write("\\begin{tikzpicture}\n")
    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "xlabel=Iterations, "\
            "x label style={at={(axis description cs:0.5,0.03)}, anchor=north}, "\
            "y label style={at={(axis description cs:0.05,.5)} }, "\
            "legend style={\n"\
            "at={(1.05, 1.0)}, anchor=north west},"\
            "ylabel=Mean LCS]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos"]:
            f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    for g in ["max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    f.write("\\draw[dashed] (axis cs:10000,0) -- (axis cs:10000,1);\n")
    f.write("\\end{axis}\n")

    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "at={(0, -.41\\linewidth)}, xlabel=Iterations,"\
            "x label style={at={(axis description cs:0.5,0.03)}, anchor=north}, "\
            "y label style={at={(axis description cs:0.05,.5)} }, "\
            "legend style={\n"\
            "at={(0, -0.2)}, anchor=north west}, ylabel=Mean GCS]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos"]:
            f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    f.write("\\draw[dashed] (axis cs:10000,0) -- (axis cs:10000,1);\n")
    f.write("\\end{axis}\n")
    f.write("\\end{tikzpicture}\n")


with open("top_shift_hub.tikz", "w") as f:
    f.write("\\begin{tikzpicture}\n")
    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "xlabel=Iterations, "\
            "x label style={at={(axis description cs:0.5,0.03)}, anchor=north}, "\
            "y label style={at={(axis description cs:0.05,.5)} }, "\
            "legend style={\n"\
            "at={(1.05, 1.0)}, anchor=north west},"\
            "ylabel=Mean LCS]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    f.write("\\draw[dashed] (axis cs:10000,0) -- (axis cs:10000,1);\n")
    f.write("\\end{axis}\n")

    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "at={(0, -.41\\linewidth)}, xlabel=Iterations,"\
            "x label style={at={(axis description cs:0.5,0.03)}, anchor=north}, "\
            "y label style={at={(axis description cs:0.05,.5)} }, "\
            "legend style={\n"\
            "at={(0, -0.2)}, anchor=north west}, ylabel=Mean GCS]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/top_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    f.write("\\draw[dashed] (axis cs:10000,0) -- (axis cs:10000,1);\n")
    f.write("\\end{axis}\n")
    f.write("\\end{tikzpicture}\n")


with open("env_shift.tikz", "w") as f:
    f.write("\\begin{tikzpicture}\n")
    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "xlabel=Iterations, "\
            "x label style={at={(axis description cs:0.5,0.03)}, anchor=north}, "\
            "y label style={at={(axis description cs:0.05,.5)} }, "\
            "legend style={\n"\
            "at={(1.05, 1.0)}, anchor=north west},"\
            "ylabel=Mean LCS]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/env_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos", "max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
            f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/env_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/env_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    f.write("\\draw[dashed] (axis cs:10000,0) -- (axis cs:10000,1);\n")
    f.write("\\end{axis}\n")

    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "at={(0, -.41\\linewidth)}, xlabel=Iterations,"\
            "x label style={at={(axis description cs:0.5,0.03)}, anchor=north}, "\
            "y label style={at={(axis description cs:0.05,.5)} }, "\
            "legend style={\n"\
            "at={(0, -0.2)}, anchor=north west}, ylabel=Mean GCS]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/env_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos", "max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
            f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/env_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/env_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    f.write("\\draw[dashed] (axis cs:10000,0) -- (axis cs:10000,1);\n")
    f.write("\\end{axis}\n")
    f.write("\\end{tikzpicture}\n")


with open("env_shift_gauss.tikz", "w") as f:
    f.write("\\begin{tikzpicture}\n")
    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "xlabel=Iterations, "\
            "x label style={at={(axis description cs:0.5,0.03)}, anchor=north}, "\
            "y label style={at={(axis description cs:0.05,.5)} }, "\
            "legend style={\n"\
            "at={(1.05, 1.0)}, anchor=north west},"\
            "ylabel=Mean LCS]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/env_shift_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos", "max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
            f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/env_shift_gauss_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CSA_mean] "\
                    "{{simulation_results/env_shift_gauss_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")
            f.write("\\addlegendentry{{{0}}}\n".format(label))

    f.write("\\draw[dashed] (axis cs:10000,0) -- (axis cs:10000,1);\n")
    f.write("\\end{axis}\n")

    f.write("\\begin{axis}[width=.7\\linewidth, height=.45\\linewidth, ymax=0.9,"\
            "at={(0, -.41\\linewidth)}, xlabel=Iterations,"\
            "x label style={at={(axis description cs:0.5,0.03)}, anchor=north}, "\
            "y label style={at={(axis description cs:0.05,.5)} }, "\
            "legend style={\n"\
            "at={(0, -0.2)}, anchor=north west}, ylabel=Mean GCS]\n")

    for g in ["clique"]:
            f.write("\\addplot +[mark=none, dotted, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/env_shift_gauss_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["max_avg_bet", "max_avg_clust", "max_max_bet", "min_max_clos", "max_var_cons", "min_avg_bet", "min_avg_clust", "max_max_clos"]:
            f.write("\\addplot +[mark=none, dashed, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/env_shift_gauss_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    for g in ["hub", "hub_hearer", "hub_speaker"]:
            f.write("\\addplot +[mark=none, solid, thick] table[col sep=comma, x=Iteration, "\
                    "y=CLA_mean] "\
                    "{{simulation_results/env_shift_gauss_{0}.csv}};\n".format(g))
            label = g.replace("_", " ")

    f.write("\\draw[dashed] (axis cs:10000,0) -- (axis cs:10000,1);\n")
    f.write("\\end{axis}\n")
    f.write("\\end{tikzpicture}\n")
