import argparse
import gett.io

parser = argparse.ArgumentParser()
parser.add_argument('cases_expression', type=args.FileType('r'))
parser.add_argument('controls_expression', type=args.FileType('r'))
parser.add_argument('cases_bootstrap', type=args.FileType('r'))
parser.add_argument('controls_bootstrap', type=args.FileType('r'))
parser.add_argument('cases_communities', type=args.FileType('r'))
parser.add_argument('threshold', type=float)
parser.add_argument('outfile', type=str)

args = parser.parse_args()

patients_controls, genenames_cases, Mexp_cases = gett.io.read_expression_matrix(args.cases_expression)
patients_controls, genenames_controls, Mexp_controls = gett.io.read_expression_matrix(args.controls_expression)
Mcorr_cases = corrcoef(Mexp_cases)
Mcorr_controls = corrcoef(Mexp_controls)
Madj_controls = Mcorr_controls[abs(Mcorr_controls) < args.threshold] = 0
conf_val_cases = gett.io.read_dict(args.cases_bootstrap, numfieldsid=2)
conf_val_controls = gett.io.read_dict(args.controls_bootstrap, numfieldsid=2, apply_for_keys=lambda x: (int(x[0]), int(x[1])), apply_for_values=lambda x:int(x[0]))
nodesbycluster, edgesbycluster = gett.io.read_community(args.cases_communities)
traits = topological_change_trait(Mexp_cases, Mcorr_cases, Mcorr_controls, Madj_controls, conf_val_cases, conf_val_controls, edgesbycluster)
gett.io.write_dict(args.outfile, traits, split_lists=True)
