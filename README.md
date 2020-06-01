## Setup guide

Clone folder and initialize submodules

```
git clone https://github.com/lzivadinovic/hmi-bond.git
cd hmi-bond
git submodule init
git submodule update
```
Install python 3.7 interpreter and create virtualenv

Install libraries in following manner

```bash
pip install tensorflow==1.15.3
pip install keras==2.3.1
pip install git+https://www.github.com/keras-team/keras-contrib.git

cd keras-contrib
python convert_to_tf_keras.py
USE_TF_KERAS=1 python setup.py install
cd ../
pip install -r requirements.txt
```


After that you can change harp number in master_wrap and run script again to fetch and process all data.
