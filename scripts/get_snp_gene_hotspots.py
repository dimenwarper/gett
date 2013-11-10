import argparse
import operator
import defaultdict

parser = argparse.ArgumentParser()

parser.add_argument('regression_result_file', type=argparse.FileType('r'))
parser.add_argument('snp_coordinate_file', type=argparse.FileType('r'))
parser.add_argument('refgene_file', type=argparse.FileType('r'))
parser.add_argument('outfile', type=argparse.FileType('w'))

args = parser.parse_args()

snp_list = [l.strip().split('\t')[0] for l in args.regression_result_file.readlines()]

snp_coords = defaultdict(list)
line = args.snp_coordinate_file.readline()
while line:
    fields = line.strip().split('\t')
    try:
        snp_coords[fields[1]].append((fields[0], int(fields[2])))
    except Exception:
        pass
    line = args.snp_coordinate_file.readline()

gene_counts = defaultdict(int)

line = args.refgene_file.readline()
while line:
    fields = line.strip().split('\t')
    chrom = fields[2].replace('chr','')
    start = int(fields[6])
    end = int(fields[7])
    if chrom in snp_coords:
        for snp, coord in snp_coords:
            if coord >= start and coord <= end:
                gene_counts[fields[12]] += 1
    line = args.refgene_file.readline()
sorted_gene_counts = sorted(gene_counts.iteritems(), key=operator.itemgetter(1))

for gene, counts in sorted_gene_counts:
    args.outfile.write('%s\t%s\n' % (gene, counts))



