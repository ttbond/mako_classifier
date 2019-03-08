# Mako_classifier
Mako_classifier can classify the patterns found by Mako into three classes(DEL,DUP,INV) and give scores for complex SVs. Based on LSTM model, Mako_classifier can use the sequential information to classify the patterns.

# Install and run

Mako_classifier requires linux OS and Python (3.5.2) to run.

#### Dependency
* Numpy (>=1.15.0)
* Tensorflow (>=1.12.0)(https://www.tensorflow.org/): a package used for machine learning applications such as neural networks and can be installed by pip

#### Usage
```sh
$ git clone https://github.com/ttbond/mako_classifier.git
```

Open the folder mako_classifier at terminal, files include:

* testData: three vcf files from Mako which can be used to test the script
* src: srcipts
* model: a model trained with NA19240. Current version dose not support customised model training.

To run the script:
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
* CX: a score to measure the posibility of complex SV, high score indicates that this SV may be a complex SV


