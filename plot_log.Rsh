#!/usr/bin/Rscript

args=commandArgs(TRUE)
file_name='log_GentecPlink.txt'
file_name=args[1]

t=read.table(file_name,header=0,sep=';')
colnames(t)=c("head","time","power")
t$time=strptime(t$time,'%d/%m/%Y %H:%M:%S')
#summary(t)


size=256
len=length(t$time)
i0=len-size
i1=len
t=t[i0:i1,]
#summary(t)

tup=subset(t,subset=head=='UP19K-15S-VR')
#summary(tup)
txlp=subset(t,subset=head=='XLP12-3S-H2-D0')
#summary(txlp)

size=size/4
len=length(tup$time)
i0=len-size
i1=len
tims= tup$time[i0:i1]
tups= tup$power[i0:i1]
len=length(txlp$time)
i0=len-size
i1=len
txlps=txlp$power[i0:i1]

filter_size=30
moving_average=function(x,n=10){filter(x,rep(1/n,n), sides=1)}
i0=size-filter_size
timl=tims[i0]
tups=moving_average(tups)#,n=filter_size)
txlps=moving_average(txlps)#,n=filter_size)
ratio=tups/txlps
#summary(ratio)
cat(tups[length(tups)],"  ",txlps[length(txlps)],"  ",ratio[length(ratio)],"\n")

pdf()
#par(mfrow=c(1,2))
plot(t$time,t$power, type="l", col="red" )
plot(t$time,t$power, type="l", col="white")
lines( tup$time, tup$power, type="l", col="green")
lines(txlp$time,txlp$power, type="l", col="blue")
lines(tims,ratio*10,   type="l", col="black")
lines(tims,tups,  type="l", col="red")
lines(tims,txlps, type="l", col="yellow")
lines(c(timl,timl),c(0,max(tups)), type="l", col="red")
dev.off()

