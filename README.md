# Overview

![](static/images/bengal.png)


<p align="justify">Bengali is the 5th most spoken language in the world with hundreds of milion of speakers.It's the official language of Bangladesh and the second most spoken language in India.Considering its reach,there's significant business and educational interest in developing AI that can optically recognize images of the language handwritten.This challenge hopes to improve on approaches to Bengaili recognition</p>

<p align="justify">Optical character recognition is particularly challenging for Bengali.While Bengali has 49 letters (to be more specific 11 vowels and 38 consonants) in its alphabet,there are also 18 potential diacritics,or accents.This means that there are many more graphemes,or the smallest units in a written language.The added complexity results in ~ 13,000 different grapheme variations (compared to English's 250 graphemic units)</p>

<p align="justify">Bangladesh-based non-profit</p>[bengali.ai](https://bengali.ai/)<p align="justify">is focused on helping to solve this problem.They build and release crowdsourced,metadata-rich datasets and open source them through research competitions.Through this works,Bengali.AI hopes to democratize and accelerate research in Bengali language technologies and to promote machine learning education</p>

<p align="justify">For this competition,you're given the image of a handwritten Bengali grapheme and are challenged to separately classify three constituent elements in the image:grapheme root,vowel diacritics,consonant diacritics</p>

# Dataset
<p align="justify">This dataset contains images of individual hand-written</p>[Bengali characters](https://en.wikipedia.org/wiki/Bengali_alphabet)<p align="justify">.Bengali characters (graphemes) are written by combining three components:a grapheme_root,vowel_diacritic,and consonant_diacritic</p>

# Flask app
- Download model file Bengal_classifier.h5 [here](https://drive.google.com/drive/folders/1ajzVj7lKko367_NOiB9cXwIt5yxnzFi7?usp=sharing)
- Copy Bengal_classifier.h5 into folder models
- create new env called **bengali** `conda create --name bengali python=3.7`
- install requirements `pip install -r requirements.txt`
- run app `python main.py`