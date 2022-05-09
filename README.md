# CS206 Code Repository

A/B Testing Instructions

This project uses Python 3.6.9 and requires Numpy & Pybullet to be installed via pip

1. Make overall folder 
2. Make three folders: VariantA, VariantB, test_data
3. Clone origin master into VariantA; Variant_B into VariantB
4. Copy run.sh from VariantA into folder above VariantA (over-arching folder)
5. run `./run.sh`

If you get a mass of "Module Not Found" errors, it may be because you do not have pyenv installed & Python's module finding ability is awful. I am not sure how pervasive this issue is, I've tried running it on a number of computers, sometimes it Just Works and sometimes it doesn't. 
