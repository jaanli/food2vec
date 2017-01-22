/******************\
|  Word2Vec Utils  |
| @author Anthony  |
| @version 0.2.1   |
| @date 2016/01/08 |
| @edit 2016/01/08 |
\******************/

var Word2VecUtils = (function() {
  'use strict';

  /**********
   * config */

  /*************
   * constants */
  var WORDS = Object.keys(wordVecs);

  /*********************
   * working variables */

  /******************
   * work functions */
  function diffN(n, word1, word2) {
    for (var ai = 1; ai < arguments.length; ai++) {
      if (!wordVecs.hasOwnProperty(arguments[ai])) {
        return [false, arguments[ai]];
      }
    }

    return getNClosestMatches(
      n,
      subVecs(wordVecs[word1], wordVecs[word2])
    );
  }

  // analogy: predict a is to b as c is to _
  function analogy(n, analogyA, analogyB, analogyC) {
    var aEmb = wordVecs[analogyA];
    var bEmb = wordVecs[analogyB];
    var cEmb = wordVecs[analogyC];
    var target = addVecs(cEmb, subVecs(bEmb, aEmb));
    var matches = getNClosestMatches(n, target);
    var filteredMatches = [];
    for (var ai = 0; ai < matches.length; ai++) {
      var word = matches[ai][0]
      if ((analogyA !== word) && (analogyB !== word) && (analogyC !== word)) {
        filteredMatches.push(matches[ai]);
      }
    }
    return filteredMatches;
  }

  // recommend: get mean vector of list, recommend top N closest
  function recommendation(n, wordList) {
    var inputVecs = [];
    for (var ai = 0; ai < wordList.length; ai++) {
      inputVecs.push(wordVecs[wordList[ai]]);
    }
    var sumVectors = Word2VecUtils.addVecList(inputVecs);
    var target = Word2VecUtils.mulVec(sumVectors, 1.0 / wordList.length);
    var matches = getNClosestMatches(n, target);
    var filteredMatches = [];
    for (var ai = 0; ai < matches.length; ai++) {
      var word = matches[ai][0]
      if (!wordList.includes(word)) {
        filteredMatches.push(matches[ai]);
      }
    }
    return filteredMatches;
  }

  function composeN(n, word1, word2) {
    for (var ai = 1; ai < arguments.length; ai++) {
      if (!wordVecs.hasOwnProperty(arguments[ai])) {
        return [false, arguments[ai]];
      }
    }

    return getNClosestMatches(
      n,
      addVecs(wordVecs[word1], wordVecs[word2])
    );
  }

  function mixAndMatchN(n, sub1, sub2, add1) {
    for (var ai = 1; ai < arguments.length; ai++) {
      if (!wordVecs.hasOwnProperty(arguments[ai])) {
        return [false, arguments[ai]];
      }
    }

    return getNClosestMatches(
      n,
      addVecs(wordVecs[add1], subVecs(wordVecs[sub1], wordVecs[sub2]))
    );
  }

  function findSimilarWords(n, word) {
    if (!wordVecs.hasOwnProperty(word)) {
      return [false, word];
    }

    return getNClosestMatches(
      n, wordVecs[word]
    );
  }

  function getNClosestMatches(n, vec) {
    var sims = [];
    for (var word in wordVecs) {
      // var sim = getCosSim(vec, wordVecs[word]);
      var sim = getDotProd(vec, wordVecs[word]);
      sims.push([word, sim]);
    }
    sims.sort(function(a, b) {
      return b[1] - a[1];
    });
    var matches = sims.slice(1, n);
    for (var ai = 0; ai < matches.length; ai++) {
      matches[ai][1] = round(matches[ai][1], 3);
    }
    return matches;
  }

  /********************
   * helper functions */
  function getCosSim(f1, f2) {
    return Math.abs(f1.reduce(function(sum, a, idx) {
      return sum + a*f2[idx];
    }, 0)/(mag(f1)*mag(f2))); //magnitude is 1 for all feature vectors
  }

  function getDotProd(f1, f2) {
    return f1.reduce(function(sum, a, idx) {
      return sum + a * f2[idx];
    }, 0)
  }

  function mulVec(a, scalar) {
    return a.map(function(a) { return a * scalar; });
  }

  function mag(a) {
    return Math.sqrt(a.reduce(function(sum, val) {
      return sum + val*val;
    }, 0));
  }

  function norm(a) {
    var mag = mag(a);
    return a.map(function(val) {
      return val/mag;
    });
  }

  function addVecs(a, b) {
    return a.map(function(val, idx) {
      return val + b[idx];
    });
  }

  function addVecList(vecList) {
    var sum = subVecs(vecList[0], vecList[0]);
    for (var ai = 0; ai < vecList.length; ai++) {
      sum = addVecs(sum, vecList[ai]);
    }
    return sum;
  }

  function subVecs(a, b) {
    return a.map(function(val, idx) {
      return val - b[idx];
    });
  }

  function round(value, decimals) {
    return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
  }

  return {
    diffN: diffN,
    composeN: composeN,
    findSimilarWords: findSimilarWords,
    mixAndMatchN: mixAndMatchN,
    addVecs: addVecs,
    subVecs: subVecs,
    getNClosestMatches: getNClosestMatches,
    getCosSim: getCosSim,
    getDotProd: getDotProd,
    analogy: analogy,
    round: round,
    mulVec: mulVec,
    addVecList: addVecList,
    recommendation: recommendation
  };
})();