import ett.preprocessing
import ett.io
import argparse
import ett.models


parser = argparse.ArgumentParser()

parser.add_argument('--traitdata', nargs='+', type=argparse.FileType('r'))
parser.add_argument('--covariatedata', nargs='+', type=argparse.FileType('r'))
parser.add_argument('--genotypematrix', nargs='+', type=argparse.FileType('r'))
parser.add_argument('--correctcovariates', nargs='+', type=str)
parser.add_argument('--clip', action='store_true', default=False)

args = parser.parse_args()

report_matrices = args.clip

#TODO read_trait_matrix
Dtraits = [ett.io.read_trait_matrix(f) for f in args.traitdata]
Dcovariates = [ett.io.read_trait_matrix(f) for f in args.traitdata]

if len(args.correctcovariates):
    Dtraits = [ett.preprocessing.correct_covariates(Dtrait, Dcov, args.correctcovariates) for Dtrait, Dcov in zip(Dtraits, Dcovariates)]

if args.clip:
    clip_model = ett.models.CLIP()
    conc_matrices, comm_vectors, llhood = clip_model(Dtraits)
    weight_matrices = conc_matrices

if report_communities:
    #TODO reports
    ett.reports.community_report(comm_vectors, weight_matrices=weight_matrices)
