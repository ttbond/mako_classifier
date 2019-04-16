# Mako_classifier
Mako_classifier is based on LSTM model and designed to classify Mako output to three primary SV types (DUP,DEL,INV).
# Install and run

Mako_classifier requires linux OS and Python (3.5.2) to run.

#### Dependency
* Numpy (>=1.15.0)
* Tensorflow (>=1.12.0): a package used for machine learning applications such as neural networks, install instruction can be found at https://www.tensorflow.org/install

#### Usage
```sh
$ git clone https://github.com/ttbond/mako_classifier.git
```

Open the folder mako_classifier at terminal, files include:

* testData: three vcf files from Mako which can be used to test the script
* src: srcipts
* model: a model trained with HG00514 and HG00733.

In general, this classifier contains two steps, including training and prediction. 
##### Step1: Model training
The model we constructed is a neural network with three layers, including the input layer, the LSTM layer and a dense layer for output. It is trained on the SV datasets with high confidence, including real samples and simulated samples. Three kinds of SV types are used to train the model, including DEL, INS (DUP included) and INV. The details of model training is showed in *mako_classifier/src/scorer_lstm.py* . Current version dose not support customised model training, thus a well trained model is provided at *mako_classifier/model/simuModel.h5* .
##### Step2: Prediction

To predict new samples:
```sh
cd /path/to/mako_classifier/
bash mako_classifier.sh [input] [directory] [output]
```
* input: /path/to/discovered_SV_region.vcf
* directory: the path of the directory where the script saves temporary files and output file
* output: the result will be saved as [directory]/[output].vcf (default is discovered_SV_region_withScore.vcf)
** Note that input and directory both need to be the absolute path

Example
``` sh
bash mako_classifier.sh /path/to/mako_classifier/testData/NA19240.Mako.reproduce.vcf /path/to/work/directory NA19240
```

#### Output format
The SV output file will add two additional information (SVTYPE, CX) to the *.vcf from Mako.
* SVTYPE: the predicted type of the SV, can be DEL,DUP(INS included) and INV
* CX: a score to measure the complexity of local alignment, higher score may indicates regions with multiple breakpoints


