from factory import Factory
from time import time
from numpy import mean, std, array
import scipy
import scipy.stats

start_time = time()
print('start_time: ' + str(start_time))

#seeds = [204, 555, 359, 923, 172, 413, 498, 849, 130, 702, 985, 743, 525, 288, 965, 222, 601, 572, 807, 321, 248, 223, 287, 669, 252, 119, 417, 763, 307, 349, 361, 740, 449, 153, 894, 551, 749, 730, 857, 910, 680, 343, 820, 792, 937, 443, 160, 324, 833, 752, 193, 766, 173, 465, 669, 451, 216, 950, 956, 511, 367, 315, 738, 179, 355, 591, 428, 294, 550, 170, 522, 232, 306, 350, 401, 508, 429, 620, 862, 251, 482, 975, 337, 843, 908, 901, 375, 499, 184, 827, 305, 675, 407, 945, 410, 368, 958, 308, 876, 229]
seeds = [470, 770, 689, 376, 100, 753, 755, 682, 243, 432, 454, 760, 947, 184, 299, 631, 571, 644, 650, 483]
duration = 2 * 24 * 60 * 60

configuration_space = [20, 40, 200]
configuration_space = [15]


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
            # print('Running {}th simulation at {}'.format(i, str(time() - start_time)))
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
            self.mean_confidence_interval([float(s.total_produced) for s in self.samples])
        )

        self.mean_throughput, self.deviation_throughput, *self.confidence_interval_throughput = (
            self.mean_confidence_interval([float(s.average_throughput) for s in self.samples])
        )

    def __str__(self):
        return 'configuration: {}\nresult: {}\n'.format(
                str((self.batchsize, self.buffersizeA, self.buffersizeB, self.buffersizeC)),
                str((self.mean_produced, self.deviation_produced, self.confidence_interval_produced,
                   self.mean_throughput, self.deviation_throughput, self.confidence_interval_throughput)))

    def __lt__(self, conf2):
        return self.mean_produced < conf2.mean_produced

    @staticmethod
    def mean_confidence_interval(data, confidence=0.95):
        a = 1.0 * array(data)
        n = len(a)
        assert n > 1
        m, s = mean(a), scipy.stats.sem(a)
        h = s * scipy.stats.t._ppf((1 + confidence) / 2., n - 1)
        return m, s, m - h, m + h


def run():
    results = []
    for batchsize in [10, 20, 40]:
        for buffersizeA in configuration_space:
            for buffersizeB in configuration_space:
                for buffersizeC in configuration_space:
                    if batchsize > buffersizeB or batchsize > buffersizeC:
                        continue
                    results.append(Configuration(batchsize, buffersizeA, buffersizeB, buffersizeC))

    print('\n'.join((str(r) for r in sorted(results))))

run()
