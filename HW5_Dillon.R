install.packages("caTools")
library(caTools)
library(RWeka)

feddf <- read.csv("fedPapers85.csv")

tdf <- feddf[c(1:12),]
sampdf <- feddf[-c(1:12),]




smp_size <- floor(0.75 * nrow(sampdf))

## set the seed to make your partition reproducible
set.seed(10)
train_ind <- sample(seq_len(nrow(sampdf)), size = smp_size)

traindf <- sampdf[train_ind, ]
testdf <- sampdf[-train_ind, ]
View(testdf)
View(traindf)

View(traindf)
View(testdf)
traindf <- with(traindf, traindf[order(traindf$author),])



testdf <- rbind(testdf,tdf)
testdf <- with(testdf, testdf[order(testdf$author),])

#start making decision tree model
m=J48(Author~., data = traindf, control=Weka_control(U=FALSE, M=2, C=0.5))
e <- evaluate_Weka_classifier(m, numFolds = 10, seed = 1, class = TRUE)
pred=predict (m, newdata = testset, type = c("class"))
myids=c("PassengerId")
id_col=testset[myids]
newpred=cbind(id_col, pred)
colnames(newpred)=c("Passengerid", "Survived")
write.csv(newpred, file="H:/Assignments/Grad/IST707/lig.csv", row.names=FALSE)
