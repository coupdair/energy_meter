#!/usr/bin/Rscript

args=commandArgs(TRUE)
file_name='log_GentecPlink.txt'
file_name=args[1]

t=read.table(file_name,header=0,sep=';')
colnames(t)=c("head","time","power")
t$time=strptime(t$time,'%d/%m/%Y %H:%M:%S')
summary(t)

pdf()
#par(mfrow=c(1,2))
plot(t$time,t$power, type="l", col="red" )
#plot(t$time,t$power2, type="l", col="green" )
dev.off()

