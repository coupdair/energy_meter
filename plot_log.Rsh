#!/usr/bin/Rscript

args=commandArgs(TRUE)
file_name='log_GentecPlink.txt'
file_name=args[1]

t=read.table(file_name,header=0,sep=';')
colnames(t)=c("head","time","power")
t$time=strptime(t$time,'%d/%m/%Y %H:%M:%S')
#summary(t)

tup=subset(t,subset=head=='UP19K-15S-VR')
#summary(tup)
txlp=subset(t,subset=head=='XLP12-3S-H2-D0')
#summary(txlp)

size=1024
len=length(tup$time)
i0=len-size
i1=len
tims= tup$time[i0:i1]
tups= tup$power[i0:i1]
len=length(txlp$time)
i0=len-size
i1=len
txlps=txlp$power[i0:i1]
ratio=tups/txlps
#summary(ratio)
cat(ratio[length(ratio)],"\n")

pdf()
#par(mfrow=c(1,2))
plot(t$time,t$power, type="l", col="red" )
plot(t$time,t$power, type="l", col="white")
lines( tup$time, tup$power, type="l", col="green")
lines(txlp$time,txlp$power, type="l", col="blue")
lines(tims,ratio*10,   type="l", col="black")
dev.off()

