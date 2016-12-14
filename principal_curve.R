library(princurve)

point_data <- read.csv("clusters-csv")

f_point_data <- read.csv("clusters-csv")
f_point_data$cluster <- factor(point_data$cluster)

# grouping...
Groups<-levels(factor(f_point_data[[3]]))

fileConn<-file("curves.csv")
writeLines(c("lat,long,cluster"), fileConn)

pointsFrame <- data.frame()

for( i in Groups) {
  if(i != 0) {
    cluster <- as.matrix(subset(point_data, cluster == i))

    try ({
      curve <- principal.curve(cluster, start=NULL, thresh=0.001, plot.true=FALSE, maxit=10, stretch=2, smoother="smooth.spline", trace=FALSE)
      print("finished:")
      print(i)

      pointsFrame <- rbind(pointsFrame, data.frame(curve$s[curve$tag,]))
    })
  }
}

write.csv(pointsFrame, fileConn)

#close(fileConn)