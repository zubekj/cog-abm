import sys
import logging
import cPickle

from time import time

sys.path.append('../')
sys.path.append('../../')

from cog_simulations.cog_abm.extras.tools import get_progressbar


def compose(fun_out, fun_in):

    def composition(*args, **kwargs):
        return fun_out(fun_in(*args, **kwargs))

    return composition


def avg(n_list):
    return [math.fsum(n_list)/len(n_list)]


def v_min(n_list):
    return [min(n_list)]


def v_max(n_list):
    return [max(n_list)]

cc_computed = {}


def count_category(agents, params, it):

    global cc_computed
    try:
        stimuli = params['environments']['global'].stimuli
    except KeyError:
        stimuli = params['STIMULI']

    def number_of_categories(agent):
        agents_set = {}
        for s in stimuli:
            agents_set[agent.sense_and_classify(s)] = 1
        return len(agents_set)

    tmp_r = cc_computed.get(it, None)
    if tmp_r is None:
        tmp_r = [number_of_categories(a) for a in agents]
        cc_computed[it] = tmp_r

    return tmp_r


from cog_simulations.steels.metrics import *

# def avg_cc(agents, params, it):
#       return [float(sum(count_category(agents, params, it))) / len(agents)]
fun_map =\
    {
        'cc': count_category,
        'it': lambda ag, par, it: [it],
        'DSA': lambda ag, par, it: map(ds_a, ag),
        'DS': lambda ag, par, it: [ds(ag, it)],
        'CSA': lambda ag, par, it: map(cs_a, ag),
        'CS': lambda ag, par, it: [cs(ag, it)],
        'cv': lambda ag, par, it: [cv(ag, it)]
    }

pref_fun_map =\
    {
        'avg': avg,
        'min': v_min,
        'max': v_max
    }


def gen_res(results, params, functions):
    start_time = time()
    logging.info("Calculating stats...")

    pb = get_progressbar()
    ret_v = [[x for f in functions for x in f(agents, params, it)]
             for it, agents in pb(results)]

    logging.info("Calculating stats finished. Total time: "+str(time()-start_time))
    return ret_v


def main():

    import optparse

    usage = "%prog [-c] [-v] -f FILE statistic1 statistic2 ...\n" + \
            "where statistic in {"+";".join(fun_map.keys())+"}"
    options = optparse.OptionParser(usage=usage)

    options.add_option('-v', '--verbose', dest='verbose', action='count',
                       help="increase verbosity (specify multiple times for more)")

    options.add_option('-c', '--chart', action="store_true", dest='chart',
                       help="specifies output to be a chart")

    options.add_option('-f', '--file', action="store", dest='file', type="string",
                       help="input file with results. THIS OPTION IS NECESSARY!")

    options.add_option('--x_label', action="store", dest='x_label', type="string",
                       help="Label of x-axis")

    options.add_option('--y_label', action="store", dest='y_label', type="string",
                       help="Label of y-axis")

    opts, args = options.parse_args()

    if len(args) == 0:
        options.error("No argument given!")

    if opts.file is None or opts.file == "":
        options.error("No or wrong file specified (option -f)")

    if opts.chart and len(args) < 2:
        options.error("Can't draw a chart with one dimension data")

    log_level = logging.INFO  # logging.DEBUG # default logging.WARNING

    if opts.verbose == 1:
        log_level = logging.INFO

    elif opts.verbose >= 2:
        log_level = logging.DEBUG

    # Set up basic configuration, out to std err with a reasonable default format.
    logging.basicConfig(level=log_level)

    f = open("../../results_of_simulation/" + opts.file)
    res, params = cPickle.load(f)
    f.close()

    funcs = []
    for arg in args:
        ind = arg.find("_")
        fun = None
        if ind != -1:
            p_fun = pref_fun_map.get(arg[0:ind])

            m_fun = fun_map.get(arg[ind+1:len(arg)])

            if p_fun is not None and m_fun is not None:
                fun = compose(p_fun, m_fun)

        if fun is None:
            fun = fun_map.get(arg, None)

        if fun is not None:
            funcs.append(fun)
        else:
            logging.warning("Unrecognized option %s - ignoring", arg)

    wyn = gen_res(res, params, funcs)

    if opts.chart is not None:
        from cog_simulations.presenter.charts import wykres
        data = []
        map(lambda y: data.append((y[0], y[1:])), wyn)
        wykres(data, opts.xlabel, opts.ylabel)

    else:
        for r in wyn:
            print "\t".join(imap(str, r))


if __name__ == "__main__":
    main()
