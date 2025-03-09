# 清除所有变量
rm(list = ls())

# 加载包
library(psych)
library(ggbiplot)

# 从CSV文件加载数据，使用check.names = FALSE
RE_data <- read.csv("C:\\Users\\a9694\\OneDrive - mail.bnu.edu.cn\\Scientific Research\\2022-Black Soil Area in NE China\\Zhang\\RareEarth.csv", header = TRUE, check.names = FALSE)

# 提取样本列（在PCA中不使用）
specimen <- RE_data$Specimen

# 提取用于PCA的数值列
numeric_data <- RE_data[, -c(1, ncol(RE_data))]  # 排除 'Specimen' 列和 'class' 列

# 计算KMO并输出KMO值
kmo_result <- psych::KMO(numeric_data)
kmo_value <- kmo_result$MSA
cat("\nKMO Value:\n")
print(kmo_value)

# 进行Bartlett球度检验并输出p值
bartlett_test <- psych::cortest.bartlett(numeric_data)
bartlett_p_value <- bartlett_test$p.value
cat("\nBartlett's Test of Sphericity p-value:\n")
print(bartlett_p_value)

# 执行 PCA
pca_result <- prcomp(numeric_data, scale. = TRUE)

# 提取主成分的特征值
eigenvalues <- pca_result$sdev^2
cat("Eigenvalues:\n")
print(eigenvalues)

# 生成碎石图并保存为Scree.png
screeplot(pca_result, type = "lines", main = "Scree Plot")

# 保存碎石图
png("Scree.png")
screeplot(pca_result, type = "lines", main = "Scree Plot")
dev.off()

# 使用 ggbiplot 可视化 PCA
pca_plot <- ggbiplot(
  pca_result,
  groups = RE_data$class,  # 使用 'class' 列作为分组变量
  obs.scale = 1,
  var.scale = 1,
  ellipse = TRUE,
  circle = TRUE,
  labels = rownames(numeric_data),  # 使用样本名作为标签
  varname.size = 2
) +
  ggtitle("PCA Biplot") +
  xlab("PC1") +
  ylab("PC2")

# 保存 PCA Biplot 图
ggsave("PCA_Plot.png", pca_plot, width = 8, height = 6)