#!/usr/bin/Rscript

args=commandArgs(TRUE)
file_name='log_GentecPlink.txt'
file_name=args[1]

t=read.table(file_name,header=0,sep=';')
colnames(t)=c("head","time","power")
t$time=strptime(t$time,'%d/%m/%Y %H:%M:%S')
summary(t)

tup=subset(t,subset=head=='UP19K-15S-VR')
summary(tup)
txlp=subset(t,subset=head=='XLP12-3S-H2-D0')
summary(txlp)

pdf()
#par(mfrow=c(1,2))
plot(t$time,t$power, type="l", col="red" )
plot(t$time,t$power, type="l", col="white")
lines( tup$time, tup$power, type="l", col="green")
lines(txlp$time,txlp$power, type="l", col="blue")
dev.off()

