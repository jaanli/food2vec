# food2vec
Food vectors.

## Data
Get the data and preprocess it:
```
cd dat
wget http://www.nature.com/article-assets/npg/srep/2011/111215/srep00196/extref/srep00196-s3.zip
unzip srep00196-s3.zip
cd ../src
./preprocess_data.sh
```

## Usage
```
git clone git@github.com:altosaar/food2vec.git
cd food2vec
git submodule update --init
cd food2vec/src/sentence_word2vec
git submodule update --init
./compile_ops.sh
# run word2vec with the recipes as context
python word2vec_optimized.py --train_data ../../dat/recipes --interactive --save_path /tmp --subsample 0 --eval 0 --interactive --embedding_size 50
# make the t-SNE plot
cd ../../
# run t-sne and make the plot for the ingredient embeddings
python plot_ingredients.py
# run t-sne and make the plot for the recipe embeddings
python plot_recipes.py
# make the javascript explorer of analogies and cosine similarity
python make_js_embedding_explorer.py
```
