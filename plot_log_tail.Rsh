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
tsize
size
tsize-size
start=tsize-size
end=tsize
start
end
t=t[start:end,]
#t=t[1123:1456,]
summary(t)

pdf()
#par(mfrow=c(1,2))
plot(t$time,t$power, type="l", col="red" )
#plot(t$time,t$power2, type="l", col="green" )
dev.off()

