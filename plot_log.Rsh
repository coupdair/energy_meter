#!/usr/bin/Rscript

t=read.csv('log_GentecPlink.txt',header=0)
colnames(t)=c("time","power")
t$time=strptime(t$time,'%d/%m/%Y %H:%M:%S')
summary(t)

pdf()
#par(mfrow=c(1,2))
plot(t$time,t$power, type="l", col="red" )
#plot(t$time,t$power2, type="l", col="green" )
dev.off()

