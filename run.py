from factory import Factory
from time import time
from numpy import mean, std, array
import scipy
import scipy.stats

start_time = time()
print('start_time: ' + str(start_time))

seeds = [470, 770, 689, 376, 100, 753, 755, 682, 243, 432,
         454, 760, 947, 184, 299, 631, 571, 644, 650, 483]
duration = 24 * 60 * 60

configuration_space = [15, 20, 40]


class Sample:
    def __init__(self, seed, time, total_produced, average_produced, average_throughput):
        self.seed = seed
        self.time = time
        self.total_produced = total_produced
        self.average_produced = average_produced
        self.average_throughput = average_throughput


class Configuration:
    def __init__(self, batchsize, buffersizeA, buffersizeB, buffersizeC):
        self.batchsize = batchsize
        self.buffersizeA = buffersizeA
        self.buffersizeB = buffersizeB
        self.buffersizeC = buffersizeC
        self.samples = []

        for i, seed in enumerate(seeds):
            print('Running {}th simulation at {}'.format(i, str(time() - start_time)))
            factory = Factory(11, 8, self.batchsize, self.buffersizeA,
                              self.buffersizeB, self.buffersizeC, seed, duration, silent=True)
            factory.play()
            factory.start()

            factory.update_stats()
            sample = Sample(seed,
                            factory.stats['time'],
                            factory.stats['total produced'],
                            factory.stats['average produced'],
                            factory.stats['average throughput'])

            self.samples.append(sample)

        self.mean_produced, self.deviation_produced, *self.confidence_interval_produced = (
            mean_confidence_interval(s.total_produced for s in self.samples)
        )

        self.mean_throughput, self.deviation_throughput, *self.confidence_interval_throughput = (
            mean_confidence_interval(s.total_throughput for s in self.samples)
        )

    def __str__(self):
        return str(self.mean_produced, self.deviation_produced, self.confidence_interval_produced,
                   self.mean_throughput, self.deviation_throughput, self.confidence_interval_throughput)

    def __lt__(self, conf2):
        return self.mean_produced < conf2.mean_produced

    @staticmethod
    def mean_confidence_interval(data, confidence=0.95):
        a = 1.0 * array(data)
        n = len(a)
        m, s = mean(a), scipy.stats.sem(a)
        h = s * scipy.stats.t._ppf((1 + confidence) / 2., n - 1)
        return m, s, m - h, m + h


def run():
    results = []
    for batchsize in configuration_space:
        for buffersizeA in configuration_space:
            for buffersizeB in configuration_space:
                for buffersizeC in configuration_space:
                    if batchsize > buffersizeB or batchsize > buffersizeC:
                        continue
                    results.append(Configuration(batchsize, buffersizeA, buffersizeB, buffersizeC))

    print('\n'.join(sorted(results)))

run()
