#!/usr/bin/env Rscript

library(argparse)

# read in arguments
args = commandArgs(trailingOnly=TRUE)

parser = ArgumentParser(description='Takes true predicted probabilities and shuffeled sequence probabilities for emprical p-Value calculation')

parser$add_argument('-p', '--obs', metavar='<table_prob.csv>')
parser$add_argument('-sp', '--shuff', metavar='<table_shuffeled_prob.csv>')
parser$add_argument('-o', '--output')

args <- parser$parse_args()

emp_p <- function(obs, background) {
  return(sum(background > obs) / length(background))
}

obs.df <- read.table(args$obs, sep=",", header=T)
shuff.df <- read.table(args$shuff, sep=",", header=T)

obs.df$emp_p <- sapply(obs.df$score_0, function(x) emp_p(x, shuff.df$score_0))

write.csv(obs.df, file = args$output, quote = FALSE, row.names = FALSE)