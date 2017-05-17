ads_matrix = read.csv("ads.csv", header = FALSE)
terms_matrix = read.csv("terms-ad_text_terms.csv", header = FALSE)
f = read.csv("ads-terms-frequency-ad_text_terms.csv", header = FALSE)

p <- ads_matrix[,2]
plot(p)
p[p >= 20000] <- mean(p)

dic <- terms_matrix[,1]
length(dic)
nrow(f)

n <- trunc(nrow(f)/4*3)
c <- c()
seq<- c()
for (i in 1:ncol(f)) {
  if (sum(f[1:n,i])>7 ){
    c <- c(c,cor(p,f[,i]) )
    seq<-c(seq,i)
  } else {
    c <- c(c,0)
  }
}
plot(c)
length(seq)
dic[seq]

sd(p[(n+1):length(p)]-mean(p[1:n]))

fit <- lm(p[1:n] ~.,data = f[1:n,seq])
a <- summary(fit)
t <- coef(a)[, "Pr(>|t|)"]
t <- t[-1]
#dic[seq[t <0.1]]
length(seq[t <0.1])

pp <- predict(fit, f[(n+1):nrow(f),seq])
sd(p[(n+1):length(p)]-pp)
#seq <- seq[t <0.5]

library(e1071)
sfit <- svm(p[1:n] ~., data = f[1:n,seq])
summary(sfit)
pp <- predict(sfit, f[(n+1):nrow(f),seq])
sd(p[(n+1):nrow(f)]-pp)

# create ranks for all doc
sfit <- svm(p~., data = f[,seq])
pp <- predict(sfit, f[,seq])
which.max(pp/p)
sd(p-pp)
plot(pp/p)
qnorm(0.99)*sd(pp/p)

write.csv(cbind(ads_matrix[,1],pp/p), "text_rank_svm7.csv")

library(caret)
kfit <- knnreg(f[1:n,seq],p[1:n], k = 8)
summary(kfit)
pp <- predict(kfit, f[(n+1):nrow(f),seq])
sd(p[(n+1):nrow(f)]-pp)
length(pp)

library(party)
library(rpart)
tfit <- ctree(p[1:n] ~., data = f[1:n,seq], control = ctree_control(mincriterion = 0.90))
#tfit <- rpart(p[1:n] ~., data = f[1:n,seq], method = "anova",control=rpart.control(minsplit=10, cp=0.001))
summary(tfit)
pp <- predict(tfit, f[(n+1):nrow(f),seq])
sd(p[(n+1):nrow(f)]-pp)
plot(tfit)
print(tfit)

