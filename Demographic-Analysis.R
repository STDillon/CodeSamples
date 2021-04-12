library(hexbin)
library(RColorBrewer)
library(ggplot2)
library(tidyverse)

rm(list = ls())

#this is the section where I download the data, change as needed

setwd("H:/internship/Internship-Work")

the <- read.csv("demographics.csv")

#viewed the data just to make sure it works, commented out after
View(the)

colnames(the)
names(the)[1] <- "io"

#drop non-participants

big <-subset(the, io!="o")

View(big)



h <- which(is.na(big), arr.ind=TRUE)
big[h] <- rowMeans(big[,2:25], na.rm=TRUE)[h[,1]]

big$Interdependence <- (big$M1FB.Interdependence + big$M2FB.Interdependence + big$M3FB.Interdependence + big$M4FB.Interdependence + big$M5FB.Interdependence + big$M6FB.Interdependence + big$M7FB.Interdependence + big$M8FB.Interdependence)/8
big$Inclusion <- (big$M1FB.Inclusion + big$M2FB.Inclusion + big$M3FB.Inclusion + big$M4FB.Inclusion + big$M5FB.Inclusion + big$M6FB.Inclusion + big$M7FB.Inclusion + big$M8FB.Inclusion)/8
big$Interaction <- (big$M1FB.Interaction + big$M2FB.Interaction + big$M3FB.Interaction + big$M4FB.Interaction + big$M5FB.Interaction + big$M6FB.Interaction + big$M7FB.Interaction + big$M8FB.Interaction)/8
big$Group_Performance <- (big$Interdependence + big$Inclusion + big$Interaction)/3

big$Total.Grade <- as.numeric(as.character(gsub(",","",big$Total.Grade)))

ggplot(big, aes(x = ethnicID, y = Group_Performance)) +
  geom_col(position = "dodge")

ggplot(big, aes(x = genderID, y = Group_Performance)) +
  geom_col(position = "dodge")

ggplot(big, aes(x = ethnicID, y = adjFactorNoSelf)) +
  geom_col(position = "dodge")

ggplot(big, aes(x = ethnicID, y = Total.Grade)) +
  geom_col(position = "dodge")

scatter.smooth(x=big$ethnicID , y=big$Group_Performance)
scatter.smooth(x=big$genderID , y=big$Group_Performance)




demoagg <-aggregate(big, by=list(big$ethnicID),FUN=mean, na.rm=TRUE)
View(demoagg)
genderagg <-aggregate(big, by=list(big$genderID),FUN=mean, na.rm=TRUE)
View(genderagg)
write.csv(demoagg,"demoagg.csv")
write.csv(genderagg,"genderagg.csv")
#cleaned up the data manually


######################################################################
#part 2
demographics <- read.csv("demoagg.csv")
gender <- read.csv("genderagg.csv")

#demographics
#show grades in ascending order
ggplot(demographics, aes(reorder(ethnicID, +Total.Grade, sum), Total.Grade)) +
  geom_col()

#show group performance based on TA feedback in ascending order
ggplot(demographics, aes(reorder(ethnicID, +Group_Performance, sum), Group_Performance)) +
  geom_col()


#gender
#show grades based on sections and teams in ascending order
ggplot(gender, aes(reorder(genderID, +Total.Grade, sum), Total.Grade)) +
  geom_col()

#show group performance based on TA feedback in ascending order
ggplot(gender, aes(reorder(genderID, +Group_Performance, sum), Group_Performance)) +
  geom_col()

