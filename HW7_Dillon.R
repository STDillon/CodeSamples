library(dplyr)
library(tidyverse)
library(rpart)
library(RColorBrewer)
library(gbm)
library(rpart.plot)
library(caret)
library(rattle)
library(keras)
library(matrixStats)
library(grDevices)
library(gridExtra)
library(plotly)
library(readr)
library(randomForest)
library(kernlab)
#install.packages("rmarkdown")
library(rmarkdown)
setwd("C:/School/IST707")


### PREPROCESSING ###
df <- read.csv("kagtrain.csv")
train <- sample_n(df, 1400)
test <- read.csv("kagtest.csv")
test1 <- test
rows <- sample(1:nrow(train), 1000)
labels <- as.factor(train[rows,1])

#leftover code from part 6, left in just in case
train <- train %>% 
  mutate(label = as.factor(label))


control <- trainControl(method = "cv", number = 3)


### END PREPROCESSING/START SVM ###
set.seed(13)
svm<-train(label~.,data=train,method='svmLinear',trControl=control)
#svm

pred.svm <- predict(svm, newdata = test, type = "raw")

svm.preds <- data.frame(ImageId=1:nrow(test[-1000,]), Label=pred.svm)
View(pred.svm)
### END SVM/START KNN ###
knn <- train(label ~.,data = train, method = "knn",trControl = control)
knn

pred.knn <- predict(knn, newdata = test, type = "raw")
as.data.frame(pred.knn)
knn.preds <- data.frame(ImageId = 1:nrow(test[-1000,]), Label = levels(labels)[pred.knn])
###RANDOM FOREST####

rf <- randomForest(label ~., data = train, ntree= 50)
#rf
rf.pred <- predict(rf,test)
rf.preds <- data.frame(ImageId=1:nrow(test), Label=levels(labels)[rf.pred])
view(rf.preds)
#DONE