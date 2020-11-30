/******************\
|   Word2Vec JSON  |
| @author Anthony  |
| @version 0.2.1   |
| @date 2016/01/08 |
| @edit 2016/01/08 |
\******************/

var Word2VecDemo = (function() {
  'use strict';

  /**********
   * config */
  var NUM_TO_SHOW = 10;

  /*************
   * constants */
  var WORDS = Object.keys(wordVecs);
  // show a spinner for increased user satisfaction
  var TIMEOUT = 1500;
  var SPINNER =  '<center><i class="fa fa-spinner fa-pulse fa-3x fa-fw"></i><span class="sr-only">Loading...</span></center>';

  /*********************
   * working variables */

  /******************
   * work functions */
  function initWordToVecDemo() {
    $s('#list-sim-btn').addEventListener('click', function() {
      $s('#sim-table').innerHTML = SPINNER;
      var word = $s('#autocomplete-input-similarity').value;
      var simWords = Word2VecUtils.findSimilarWords(NUM_TO_SHOW, word);
      if (simWords[0] === false) {
        $s('#sim-table').innerHTML = 'No results for that food. Try another food!';
      } else {
        setTimeout(function() {
          renderSimilarities('#sim-table', simWords);
        }, TIMEOUT);
      }
    });

    $s('#solve-eqn-btn').addEventListener('click', function() {
      $s('#eqn-table').innerHTML = SPINNER;
      var analogyA = $s('#autocomplete-input-analogyA').value;
      var analogyB = $s('#autocomplete-input-analogyB').value;
      var analogyC = $s('#autocomplete-input-analogyC').value;
      var answers = Word2VecUtils.analogy(
        NUM_TO_SHOW, analogyA, analogyB, analogyC
      );
      if (answers[0] === false) {
        $s('#eqn-table').innerHTML = 'No results for for "'+answers[1]+
          '". Try another food!';
      } else {
        setTimeout(function() {
          renderSimilarities('#eqn-table', answers);
        }, TIMEOUT);
      }
    });

  $s('#solve-rec-btn').addEventListener('click', function() {
    $s('#rec-table').innerHTML = SPINNER;
    var inputDicts = $('#example_objects input.object-tag-input').materialtags('items');
    var words = [];
    for (var ai = 0; ai < inputDicts.length; ai++) {
      words.push(inputDicts[ai]["text"]);
    }
    var simWords = Word2VecUtils.recommendation(NUM_TO_SHOW, words);
    if (simWords[0] === false) {
      $s('#rec-table').innerHTML = 'No results for those ingredients. Try another food!';
    } else {
      setTimeout(function () {
        renderSimilarities('#rec-table', simWords);
      }, TIMEOUT);
    }
  });
  }

  function renderSimilarities(id, sims) {
    $s(id).innerHTML = '';
    sims.forEach(function(sim) {
      var tr = document.createElement('tr');
      tr.innerHTML = '<td>'+sim[0]+'</td>';
      tr.innerHTML += '<td>'+sim[1]+'</td>';
      $s(id).appendChild(tr);
    });
  }

  /********************
   * helper functions */
  function $s(id) { //for convenience
    if (id.charAt(0) !== '#') return false;
    return document.getElementById(id.substring(1));
  }

  return {
    init: initWordToVecDemo
  };
})();

window.addEventListener('load', Word2VecDemo.init);
