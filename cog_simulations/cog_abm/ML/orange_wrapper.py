"""
Module providing classifiers from orange library
"""

from itertools import izip

import orange
import orngSVM
import orngEnsemble
import core
import Orange

orange_learners_modules = [orange, orngSVM, orngEnsemble]
#useful methods


def create_numeric_variable(sid, meta):
    return orange.FloatVariable(sid)


def create_nominal_variable(sid, meta):
    return orange.EnumVariable(sid, values=[str(e) for e in meta.symbols])

orange_variable_map = {
    core.NumericAttribute.ID: create_numeric_variable,
    core.NominalAttribute.ID: create_nominal_variable
}


def create_basic_variables(meta):
    return [orange_variable_map[m.ID]("atr" + str(i), m)
        for i, m in enumerate(meta)]


def create_domain_with_cls(meta, cls_meta):
    l = create_basic_variables(meta)
    l.append(create_nominal_variable("classAttr", cls_meta))
    return orange.Domain(l, True)


def _basic_convert_sample(domain, sample):
    return [orange.Value(dv, v) for dv, v in
        izip(domain, sample.get_values())]


def convert_sample(domain, sample):
    tmp = _basic_convert_sample(domain, sample)
    return orange.Example(domain, tmp + [None])
#this should work if cls is in domain


def convert_sample_with_cls(domain, sample):
    tmp = _basic_convert_sample(domain, sample)
    return orange.Example(domain, tmp + [domain.classVar(sample.get_cls())])


def get_orange_classifier_class(name, module=None):
    if module is None:
        for module in orange_learners_modules:
            try:
                classifier_class = getattr(module, name)
                return classifier_class
            except AttributeError:
                pass
        return None
    else:
        module = __import__(module)
        # TODO i think that this won't work if module contains dot
        return getattr(module, name)


class OrangeClassifier(core.Classifier):

    def __init__(self, name, *args, **kargs):
        self.classifier_class = get_orange_classifier_class(name,
                                        module=kargs.get('module', None))
        if self.classifier_class is None:
            raise ValueError("No %s learner in orange libs", name)
        self.classifier_args = args
        self.classifier_kargs = kargs
        self.domain_with_cls = None
        self._create_new_classifier()

    def _create_new_classifier(self):
        self.classifier = self.classifier_class(*self.classifier_args, \
            **self.classifier_kargs)

    def _extract_value(self, cls):
        return cls.value

    def classify(self, sample):
        if self.domain_with_cls is None:
            return None
        s = convert_sample(self.domain_with_cls, sample)
        return self._extract_value(self.classifier(s))

    # TODO: I think that parent method should be fine
#    def clone(self):
#        return None

    def classify_p_val(self, sample):
        if self.domain_with_cls is None:
            return None, 0.
        s = convert_sample(self.domain_with_cls, sample)
        v, p = self.classifier(s, orange.GetBoth)
        return self._extract_value(v), p[v]

    def class_probabilities(self, sample):
        if self.domain_with_cls is None:
            return {}
        s = convert_sample(self.domain_with_cls, sample)
        probs = self.classifier(s, orange.GetProbabilities)
        d = dict(probs.items())
        return d

    def _prepare_for_train(self, samples):
        if not samples:
            self.domain_with_cls = None
            return None
        meta = samples[0].meta
        cls_meta = samples[0].cls_meta
        self.domain_with_cls = create_domain_with_cls(meta, cls_meta)
        et = orange.ExampleTable(self.domain_with_cls)
        et.extend([convert_sample_with_cls(self.domain_with_cls, s)
                                for s in samples])
        self._create_new_classifier()
        return et

    def train(self, samples):
        """
        Trains classifier with given samples.

        We recreate domain, because new class could be added
        """
        et = self._prepare_for_train(samples)
        if et is None:
            return
        self.classifier = self.classifier(et)

    def train_with_weights(self, samples_with_weights):
        samples = map(lambda x: x[0], samples_with_weights)
        et = self._prepare_for_train(samples)
        if et is None:
            return
        wid = Orange.feature.Descriptor.new_meta_id()
        for example, (sample, weight) in izip(et, samples_with_weights):
            example[wid] = weight
        self.classifier = self.classifier(et, wid)

#        self.classifier = self.classifier_class(et, *self.classifier_args,\
#                                                **self.classifier_kargs)

    def __str__(self):
        return "%s(%s, %s)" % (self.classifier_class.__name__,
            self.classifier_args, self.classifier_kargs)
