# food2vec
Food vectors.

## Data
Get the data and preprocess it:
```
cd dat
./download_data.sh
./preprocess_data.sh
```

## Usage
Train a model on the recipes dataset:
```
git clone git@github.com:altosaar/food2vec.git
cd food2vec
git submodule update --init
cd food2vec/src/sentence_word2vec
git submodule update --init
./compile_ops.sh
# run word2vec with the recipes as context
python word2vec_optimized.py --train_data ../../dat/recipes --interactive --save_path /tmp --subsample 0 --eval 0 --interactive --embedding_size 100
```

## Visualization & embedding exploration tools
```
# make the t-SNE plot
cd ../../
# run t-sne and make the plots for the ingredient embeddings
jupyter notebook ./src/plot_ingredients_recipes.ipynb
# view the analogy tool on a browser
open index.html
```
