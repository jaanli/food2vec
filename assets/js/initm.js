(function($){
  $(function(){

    var window_width = $(window).width();

    // convert rgb to hex value string
    function rgb2hex(rgb) {
      if (/^#[0-9A-F]{6}$/i.test(rgb)) { return rgb; }

      rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);

      if (rgb === null) { return "N/A"; }

      function hex(x) {
          return ("0" + parseInt(x).toString(16)).slice(-2);
      }

      return "#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]);
    }

    $('.dynamic-color .col').each(function () {
      $(this).children().each(function () {
        var color = $(this).css('background-color'),
            classes = $(this).attr('class');
        $(this).html(rgb2hex(color) + " " + classes);
        if (classes.indexOf("darken") >= 0 || $(this).hasClass('black')) {
          $(this).css('color', 'rgba(255,255,255,.9');
        }
      });
    });

    // Floating-Fixed table of contents
    setTimeout(function() {
      var tocWrapperHeight = 260; // Max height of ads.
      var tocHeight = $('.toc-wrapper .table-of-contents').length ? $('.toc-wrapper .table-of-contents').height() : 0;
      var socialHeight = 95; // Height of unloaded social media in footer.
      var footerOffset = $('body > footer').first().length ? $('body > footer').first().offset().top : 0;
      var bottomOffset = footerOffset - socialHeight - tocHeight - tocWrapperHeight;

      if ($('nav').length) {
        $('.toc-wrapper').pushpin({
          top: $('nav').height(),
          bottom: bottomOffset
        });
      }
      else if ($('#index-banner').length) {
        $('.toc-wrapper').pushpin({
          top: $('#index-banner').height(),
          bottom: bottomOffset
        });
      }
      else {
        $('.toc-wrapper').pushpin({
          top: 0,
          bottom: bottomOffset
        });
      }
    }, 100);



    // BuySellAds Detection
    // var $bsa = $(".buysellads"),
    //     $timesToCheck = 3;
    // function checkForChanges() {
    //     if (!$bsa.find('#carbonads').length) {
    //       $timesToCheck -= 1;
    //       if ($timesToCheck >= 0) {
    //         setTimeout(checkForChanges, 500);
    //       }
    //       else {
    //         var donateAd = $('<div id="carbonads"><span><a class="carbon-text" href="#!" onclick="document.getElementById(\'paypal-donate\').submit();"><img src="images/donate.png" /> Help support us by turning off adblock. If you still prefer to keep adblock on for this page but still want to support us, feel free to donate. Any little bit helps.</a></form></span></div>');

    //         $bsa.append(donateAd);
    //       }
    //     }

    // }
    // checkForChanges();


    // BuySellAds Demos close button.
    $('.buysellads.buysellads-demo .close').on('click', function() {
      $(this).parent().remove();
    });


    // Github Latest Commit
    if ($('.github-commit').length) { // Checks if widget div exists (Index only)
      $.ajax({
        url: "https://api.github.com/repos/dogfalo/materialize/commits/master",
        dataType: "json",
        success: function (data) {
          var sha = data.sha,
              date = jQuery.timeago(data.commit.author.date);
          if (window_width < 1120) {
            sha = sha.substring(0,7);
          }
          $('.github-commit').find('.date').html(date);
          $('.github-commit').find('.sha').html(sha).attr('href', data.html_url);
        }
      });
    }

    // Toggle Flow Text
    var toggleFlowTextButton = $('#flow-toggle');
    toggleFlowTextButton.click( function(){
      $('#flow-text-demo').children('p').each(function(){
          $(this).toggleClass('flow-text');
        });
    });

//    Toggle Containers on page
    var toggleContainersButton = $('#container-toggle-button');
    toggleContainersButton.click(function(){
      $('body .browser-window .container, .had-container').each(function(){
        $(this).toggleClass('had-container');
        $(this).toggleClass('container');
        if ($(this).hasClass('container')) {
          toggleContainersButton.text("Turn off Containers");
        }
        else {
          toggleContainersButton.text("Turn on Containers");
        }
      });
    });

    // Detect touch screen and enable scrollbar if necessary
    function is_touch_device() {
      try {
        document.createEvent("TouchEvent");
        return true;
      } catch (e) {
        return false;
      }
    }
    if (is_touch_device()) {
      $('#nav-mobile').css({ overflow: 'auto'});
    }

    // Set checkbox on forms.html to indeterminate
    var indeterminateCheckbox = document.getElementById('indeterminate-checkbox');
    if (indeterminateCheckbox !== null)
      indeterminateCheckbox.indeterminate = true;


    // Pushpin Demo Init
    if ($('.pushpin-demo-nav').length) {
      $('.pushpin-demo-nav').each(function() {
        var $this = $(this);
        var $target = $('#' + $(this).attr('data-target'));
        $this.pushpin({
          top: $target.offset().top,
          bottom: $target.offset().top + $target.outerHeight() - $this.height()
        });
      });
    }

    // Plugin initialization
    $('input.autocomplete').autocomplete({
      data: {'Leaf': null, 'Okra': null, 'Avocado': null, 'Parsley': null, 'Elderberry': null, 'Cherry brandy': null, 'Fig': null, 'Lard': null, 'Yogurt': null, 'Sherry': null, 'Huckleberry': null, 'Roquefort cheese': null, 'Yeast': null, 'Cardamom': null, 'Lemon peel': null, 'Coriander': null, 'Maple syrup': null, 'Feta cheese': null, 'Apricot': null, 'Plum': null, 'Haddock': null, 'Veal': null, 'Apple brandy': null, 'Kale': null, 'Bacon': null, 'Prawn': null, 'Fennel': null, 'Turkey': null, 'Chicory': null, 'Swiss cheese': null, 'Gin': null, 'Orange': null, 'Rice': null, 'Squash': null, 'Sunflower oil': null, 'Bartlett pear': null, 'Pimento': null, 'Corn grit': null, 'Clam': null, 'Berry': null, 'Chive': null, 'Potato chip': null, 'Octopus': null, 'Kohlrabi': null, 'Sour cherry': null, 'Tequila': null, 'Almond': null, 'Ginger': null, 'Lettuce': null, 'Seed': null, 'Palm': null, 'Passion fruit': null, 'Lima bean': null, 'Cayenne': null, 'Middle Eastern': null, 'Macaroni': null, 'Basil': null, 'Quince': null, 'Leek': null, 'Papaya': null, 'Gruyere cheese': null, 'Corn': null, 'Pear': null, 'Liver': null, 'Butter': null, 'Olive oil': null, 'Thyme': null, 'Macadamia nut': null, 'Raisin': null, 'Wheat bread': null, 'Cheese': null, 'Armagnac': null, 'Chervil': null, 'Sage': null, 'Wood': null, 'Champagne wine': null, 'Banana': null, 'Mustard': null, 'Cauliflower': null, 'Southeast Asian': null, 'Munster cheese': null, 'Goat cheese': null, 'Fruit': null, 'Grape brandy': null, 'Northern European': null, 'Cabbage': null, 'Red kidney bean': null, 'Vinegar': null, 'Sumac': null, 'Peppermint': null, 'Blackberry': null, 'Cranberry': null, 'Popcorn': null, 'Dill': null, 'Apple': null, 'Orange flower': null, 'Carrot': null, 'Artichoke': null, 'Juniper berry': null, 'Parsnip': null, 'Mozzarella cheese': null, 'Mandarin': null, 'Blueberry': null, 'Shellfish': null, 'Port wine': null, 'Tangerine': null, 'Bean': null, 'Red wine': null, 'Broccoli': null, 'Oyster': null, 'Cashew': null, 'Hazelnut': null, 'Bay': null, 'Smoked salmon': null, 'Black bean': null, 'Turmeric': null, 'Parmesan cheese': null, 'Coconut': null, 'Chayote': null, 'Squid': null, 'Frankfurter': null, 'Brussels sprout': null, 'Milk': null, 'Rose': null, 'Licorice': null, 'White wine': null, 'Cognac': null, 'Wheat': null, 'Endive': null, 'Cream cheese': null, 'Salmon roe': null, 'Watermelon': null, 'Black sesame seed': null, 'Cereal': null, 'Provolone cheese': null, 'Lobster': null, 'Lovage': null, 'Malt': null, 'Pistachio': null, 'Nutmeg': null, 'Buckwheat': null, 'Egg': null, 'Peanut butter': null, 'Bell pepper': null, 'East Asian': null, 'Seaweed': null, 'Guava': null, 'Lamb': null, 'Western European': null, 'Yam': null, 'Latin American': null, 'Peppermint oil': null, 'Zucchini': null, 'Lime juice': null, 'Orange peel': null, 'Garlic': null, 'Peanut oil': null, 'Date': null, 'Watercress': null, 'Onion': null, 'Shrimp': null, 'Cinnamon': null, 'Milk fat': null, 'Baked potato': null, 'Pear brandy': null, 'Radish': null, 'Nut': null, 'Grape juice': null, 'Roasted pork': null, 'Lime': null, 'Peach': null, 'Cherry': null, 'Shiitake': null, 'Caviar': null, 'Saffron': null, 'Celery': null, 'Savory': null, 'Crab': null, 'Vegetable': null, 'Truffle': null, 'Cottage cheese': null, 'Mushroom': null, 'Concord grape': null, 'Black tea': null, 'Meat': null, 'Oatmeal': null, 'Soy sauce': null, 'Strawberry': null, 'Rosemary': null, 'Star anise': null, 'Scallop': null, 'Bone oil': null, 'Bourbon whiskey': null, 'Herring': null, 'Cassava': null, 'Ham': null, 'Tarragon': null, 'Melon': null, 'Kumquat': null, 'Litchi': null, 'Roasted meat': null, 'Spearmint': null, 'Mandarin peel': null, 'Cucumber': null, 'Whiskey': null, 'Mussel': null, 'Raspberry': null, 'Currant': null, 'Cilantro': null, 'Brown rice': null, 'Buttermilk': null, 'Chinese cabbage': null, 'South Asian': null, 'Pea': null, 'Kiwi': null, 'Rum': null, 'Chickpea': null, 'Roasted peanut': null, 'Ouzo': null, 'Corn flake': null, 'Smoke': null, 'African': null, 'Fish': null, 'Chicken broth': null, 'Sesame oil': null, 'Violet': null, 'Mung bean': null, 'Bitter orange': null, 'Pepper': null, 'Shallot': null, 'Salmon': null, 'Mace': null, 'Pecan': null, 'Cured pork': null, 'Tomato': null, 'Vanilla': null, 'Kelp': null, 'Tamarind': null, 'Sour milk': null, 'Clove': null, 'Sake': null, 'Oat': null, 'White bread': null, 'Roasted beef': null, 'Fenugreek': null, 'Coconut oil': null, 'Tabasco pepper': null, 'Egg noodle': null, 'Lime peel oil': null, 'Carob': null, 'North American': null, 'Black raspberry': null, 'Green bell pepper': null, 'Sassafras': null, 'Orange juice': null, 'Mango': null, 'Cod': null, 'Pineapple': null, 'Root': null, 'Pork': null, 'Matsutake': null, 'Cabernet sauvignon wine': null, 'Smoked sausage': null, 'Mint': null, 'Flower': null, 'Nectarine': null, 'Jasmine': null, 'Pumpkin': null, 'Kidney bean': null, 'Sesame seed': null, 'Celery oil': null, 'Brandy': null, 'Black pepper': null, 'Olive': null, 'Pork sausage': null, 'Rye flour': null, 'Artemisia': null, 'Cheddar cheese': null, 'Potato': null, 'Cumin': null, 'Sweet potato': null, 'Smoked fish': null, 'Condiment': null, 'Wine': null, 'Mackerel': null, 'Japanese plum': null, 'Honey': null, 'Thai pepper': null, 'Rye bread': null, 'Lemon': null, 'Rutabaga': null, 'Beef': null, 'Rhubarb': null, 'Peanut': null, 'Southern European': null, 'Walnut': null, 'Prickly pear': null, 'Beer': null, 'Grapefruit': null, 'Beet': null, 'Catfish': null, 'Coffee': null, 'Black currant': null, 'Citrus': null, 'Wasabi': null, 'Gelatin': null, 'Tomato juice': null, 'Eastern European': null, 'Beef broth': null, 'Vegetable oil': null, 'Roasted sesame seed': null, 'Whole grain wheat flour': null, 'Anise seed': null, 'Lavender': null, 'Cocoa': null, 'Lemon juice': null, 'Turnip': null, 'Lentil': null, 'Porcini': null, 'Beef liver': null, 'Katsuobushi': null, 'Grape': null, 'Sauerkraut': null, 'Camembert cheese': null, 'Anise': null, 'Horseradish': null, 'Barley': null, 'Galanga': null, 'Romano cheese': null, 'Gardenia': null, 'Brassica': null, 'Tuna': null, 'Bread': null, 'Cane molasses': null, 'Asparagus': null, 'Enokidake': null, 'Eel': null, 'Black mustard seed oil': null, 'Marjoram': null, 'Tea': null, 'Cacao': null, 'Cream': null, 'Scallion': null, 'Blue cheese': null, 'Nira': null, 'Starch': null, 'Red bean': null, 'Caraway': null, 'Oregano': null, 'Lingonberry': null, 'Cider': null, 'Chicken liver': null, 'Green tea': null, 'Bergamot': null, 'Soybean': null, 'Chicken': null, 'Lemongrass': null, 'Pork liver': null}
    });

    $('.chips').material_chip();

    $('.chips-initial').material_chip({
      readOnly: true,
      data: [{
        tag: 'Apple',
      }, {
        tag: 'Microsoft',
      }, {
        tag: 'Google',
      }]
    });

    $('.chips-placeholder').material_chip({
      placeholder: 'Enter a tag',
      secondaryPlaceholder: '+Tag',
    });


  }); // end of document ready
})(jQuery); // end of jQuery name space