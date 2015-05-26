#!/usr/bin/Rscript

args=commandArgs(TRUE)
file_name='log_GentecPlink.txt'
file_name=args[1]

t=read.table(file_name,header=0,sep=';')
colnames(t)=c("head","time","power")
t$time=strptime(t$time,'%d/%m/%Y %H:%M:%S')
#summary(t)


len=length(t$time)
size=4096  #crop data
#size=len-1 #full data
i0=len-size
i1=len
if(i0<1) i0=1
t=t[i0:i1,]
#summary(t)

tup=subset(t,subset=head=='UP19K-15S-VR')
summary(tup)
txlp=subset(t,subset=head=='XLP12-3S-H2-D0')
summary(txlp)

size=1024
len=length(tup$time)
i0=len-size
i1=len
if(i0<1) i0=1
tims= tup$time[i0:i1]
tups= tup$power[i0:i1]
len=length(txlp$time)
i0=len-size
i1=len
if(i0<1) i0=1
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
cat('plot raw data\n')
  plot(t$time,t$power, type="l", col="red" )
cat('plot filtered data\n')
  plot(t$time,t$power, type="l", col="white")
 cat('  line high power\n')
  lines( tup$time, tup$power, type="l", col="green")
 cat('  line low  power\n')
  lines(txlp$time,txlp$power, type="l", col="blue")
##energy ratio
# cat('  line ratio\n')
#  lines(tims,ratio*10,   type="l", col="black")
# cat('  line tups\n')
#  lines(tims,tups,  type="l", col="red")
# cat('  line txlps\n')
#  lines(tims,txlps, type="l", col="yellow")
# cat('  line max\n')
#  lines(c(timl,timl),c(0,max(tups)), type="l", col="red")
dev.off()

