install.packages("hexbin")
library(hexbin)
library(RColorBrewer)
library(ggplot2)

#this is the section where I download the data, change as needed

setwd("H:/internship/Internship-Work")

the <- read.csv("all-data.csv")

#viewed the data just to make sure it works, commented out after
View(the)

#drop non-participants
big <-subset(the, io!="o")

View(big)

big$Total.Grade <- as.numeric(as.character(gsub(",","",big$Total.Grade)))
#scatterplots here show both data points as well as correlation trends
scatter.smooth(x=big$teamSatisfaction, y=big$M1.Grade)
scatter.smooth(x=big$teamSatisfaction, y=big$M2.Grade)
scatter.smooth(x=big$teamSatisfaction, y=big$M3.Grade)
scatter.smooth(x=big$teamSatisfaction, y=big$M4.Grade)
scatter.smooth(x=big$teamSatisfaction, y=big$Grade.Total)

scatter.smooth(x=big$M1FB.Interdependence, y=big$M1.Grade)
scatter.smooth(x=big$M1FB.Inclusion, y=big$M1.Grade)
scatter.smooth(x=big$M1FB.Interaction, y=big$M1.Grade)

scatter.smooth(x=big$M2FB.Interdependence, y=big$M2.Grade)
scatter.smooth(x=big$M2FB.Inclusion, y=big$M2.Grade)
scatter.smooth(x=big$M2FB.Interaction, y=big$M2.Grade)

scatter.smooth(x=big$M2FB.Interdependence, y=big$M3.Grade)
scatter.smooth(x=big$M2FB.Inclusion, y=big$M3.Grade)
scatter.smooth(x=big$M2FB.Interaction, y=big$M3.Grade)

scatter.smooth(x=big$M2FB.Interdependence, y=big$M4.Grade)
scatter.smooth(x=big$M2FB.Inclusion, y=big$M4.Grade)
scatter.smooth(x=big$M2FB.Interaction, y=big$M4.Grade)

scatter.smooth(x=big$adjFactorNoSelf, y=big$Total.Grade)
scatter.smooth(x=big$teamSatisfaction, y=big$Total.Grade)

scatter.smooth(x=big$adjFactorNoSelf, y=big$teamSatisfaction)


#did some boxplots just to see if there were outliers in the data
boxplot(big$Total.Grade)
boxplot(big$teamInterdep)
boxplot(big$teamSatisfaction)
boxplot(big$adjFactorSelf)
boxplot(big$adjFactorNoSelf)


#did some hexagonal plots here to show some loose groupings
a <- hexbin(big$adjFactorNoSelf,big$teamSatisfaction,xbins=20)
plot(a)

b <- hexbin(big$teamSatisfaction,big$Grade.Total,xbins=20)
plot(b)

#update this with all the data
big$Interdependence <- (big$M1FB.Interdependence + big$M2FB.Interdependence + big$M3FB.Interdependence + big$M4FB.Interdependence + big$M5FB.Interdependence + big$M6FB.Interdependence + big$M7FB.Interdependence + big$M8FB.Interdependence)/8
big$Inclusion <- (big$M1FB.Inclusion + big$M2FB.Inclusion + big$M3FB.Inclusion + big$M4FB.Inclusion + big$M5FB.Inclusion + big$M6FB.Inclusion + big$M7FB.Inclusion + big$M8FB.Inclusion)/8
big$Interaction <- (big$M1FB.Interaction + big$M2FB.Interaction + big$M3FB.Interaction + big$M4FB.Interaction + big$M5FB.Interaction + big$M6FB.Interaction + big$M7FB.Interaction + big$M8FB.Interaction)/8
big$Group_Performance <- (big$Interdependence + big$Inclusion + big$Interaction)/3
View(big)

big$Group_Performance <- (big$Interdependence + big$Inclusion + big$Interaction)/3
scatter.smooth(x=big$Group_Performance, y=big$adjFactorNoSelf)
scatter.smooth(x=big$adjFactorNoSelf, y=big$Group_Performance)
scatter.smooth(x=big$teamSatisfaction, y=big$Group_Performance)
scatter.smooth(x=big$teamSatisfaction, y=big$Total.Grade)
scatter.smooth(x=big$Total.Grade, y=big$teamSatisfaction)
scatter.smooth(x=big$Total.Grade, y=big$Group_Performance)
scatter.smooth(x=big$Group_Performance, y=big$Total.Grade)
c <- hexbin(big$Group_Performance,big$Grade.Total,xbins=20)
plot(c)

View(big)


