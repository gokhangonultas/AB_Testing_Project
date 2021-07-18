############################################AB Testing Project#######################################################


############################################Değişkenler##############################################################

#Impression – Reklam görüntüleme sayısı

#Click – Tıklama
#Görüntülenen reklama tıklanma sayısını belirtir

#Purchase – Satın alım
#Tıklanan reklamlar sonrası satın alınan ürün sayısını belirtir.

#Earning – Kazanç
#Satın alınan ürünler sonrası elde edilen kazanç

#####################################################################################################################


#Verinin Hazırlanması

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, \
    f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

control_group = pd.read_excel("ab_testing.xlsx", sheet_name= "Control Group")
test_group = pd.read_excel("ab_testing.xlsx", sheet_name= "Test Group")
control_group.head()
test_group.head()
#Görev 1: A/B testinin hipotezini tanımlayınız.

#H0: Control ve Test Groupları arasında fark yoktur.
#H1: Control ve Test Groupları arasında fark yardır.

#Descriptive Statistics

control_group.describe().T
test_group.describe().T
control_group.isnull().sum() #CONTROL GRUBU İÇİN EKSİK DEĞERLERE BAKIYORUZ#
test_group.isnull().sum() #TEST GRUBU İÇİN EKSİK DEĞERLERE BAKIYORUZ#
control_group["Purchase"].mean() #CONTROL GRUBU İÇİN PURCHASE ORTALAMASINA BAKIYORUZ#
test_group["Purchase"].mean() #TEST GRUBU İÇİN PURCHASE ORTALAMASINA BAKIYORUZ#
#####################Normal Dağılım Varsayım Testi#############################

##Normal Varsayım Sağlanıyorsa Pearson Tesi
##Normal Varsayım Sağlanmıyorsa Spearman Testi

######################
#HİPOTEZ TESTİ
######################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.


test_stat, pvalue = shapiro(control_group["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(test_group["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# H0 reddedilemez. p-value > 0.05.

######################Varyans Homojenliği Testi################################

# Varyans homojenliği
# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir
test_stat, pvalue = levene(control_group["Purchase"],
                           test_group["Purchase"])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# H0 reddilemez. p-value >0.05


#Görev 2:Hipotez testini gerçekleştiriniz. Çıkan sonuçların istatistiksel olarak anlamlı olup olmadığını yorumlayınız.



test_stat, pvalue = ttest_ind(control_group["Purchase"],
                              test_group["Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# H0 reddedilir. Ortalamalar arası fark yoktur.
#True ise (varsayılan), standart bağımsız 2 örnek testi gerçekleştirin eşit grup varyansları varsayar.
#Yanlış ise, eşit kabul etmeyen Welch'in t-testini gerçekleştirin. popülasyon varyansı

#########################Mann-WhitneyU Testi####################################

#Varsayımlar sağlanmadığı için Mann-WhitneyU Testi uyguluyoruz

test_stat, pvalue = mannwhitneyu(control_group["Purchase"],
                                 test_group["Purchase"]

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# H0 reddedilemez. p>0.05( p-value = 0.2308)


#Görev 3:Hangi testi kullandınız, sebeplerini belirtiniz.

# Normallik dağılım testi için shapiro-wilks testi yapılmıştır.Dağılımlar normal dağılıyor.
# Varyans homojenliği için LEVENE testi yapılmıştır.Varyanslar Homojendir.
# Bağımsız  İki örneklem t-test yapılmıştır.


#Görev 4: Görev 2’de verdiğiniz cevaba göre, müşteriye tavsiyeniz nedir?

# iki uygulama arasında fark yoktur.
## Mevcut yöntemle uygulamanın devam edilmesi.
### Belli periyotlarla testin tekrar uygulanması.