#!/usr/bin/Rscript

args=commandArgs(TRUE)
file_name='log_GentecPlink.txt'
file_name=args[1]
size=as.integer(args[2])

t=read.csv(file_name,header=0)
colnames(t)=c("time","power")
t$time=strptime(t$time,'%d/%m/%Y %H:%M:%S')

#tail
tsize=nrow(t)
start=tsize-size
end=tsize
if(start<1) {start=1}
t=t[start:end,]
summary(t)

pdf()
#par(mfrow=c(1,2))
plot(t$time,t$power, type="l", col="red" )
#plot(t$time,t$power2, type="l", col="green" )
dev.off()

