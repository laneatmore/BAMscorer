#Giada Ferrari 2020

setwd(<your results directory>)
Loadings <- read.table("<OUT>.SNP.loadings", quote="\"", comment.char="")
hist(Loadings$V4)
density<-density(Loadings$V4)
plot (density)
plot (density, log="y")

